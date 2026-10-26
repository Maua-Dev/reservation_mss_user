import base64
import json
import os
import re
import secrets
import time
from typing import Tuple

import boto3
import jwt
from jwt import PyJWKClient

from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import EnvVarNotFound, InvalidJwtFormat, NoItemsFound

# Hardcoded temporário — owner remove depois
MICROSOFT_CLIENT_ID = "e74fec3c-2662-483f-878d-9d690f973bf4"
MICROSOFT_TENANT_ID = "c49e1939-4b53-4738-bb64-41fb2990e41c"

_MICROSOFT_JWKS_URI = (
    f"https://login.microsoftonline.com/{MICROSOFT_TENANT_ID}/discovery/v2.0/keys"
)
_MICROSOFT_ISSUERS = (
    f"https://login.microsoftonline.com/{MICROSOFT_TENANT_ID}/v2.0",
    f"https://sts.windows.net/{MICROSOFT_TENANT_ID}/",
)

_JWT_B64 = re.compile(r"^[A-Za-z0-9_-]+$")
_ACCESS_TOKEN_TTL_SECONDS = 30 * 60


def _is_jwt_shape(token: str) -> bool:
    parts = token.split(".")
    if len(parts) != 3 or not all(parts):
        return False
    for part in parts:
        if not _JWT_B64.fullmatch(part):
            return False
        pad = "=" * (-len(part) % 4)
        try:
            base64.urlsafe_b64decode(part + pad)
        except Exception:
            return False
    return True


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _sign_access_token(payload: dict) -> str:
    key_arn = os.environ.get("LOGIN_KMS_SIGN_KEY_ARN")
    if not key_arn:
        raise EnvVarNotFound("LOGIN_KMS_SIGN_KEY_ARN")

    header = {"alg": "RS256", "typ": "JWT"}
    segments = (
        f"{_b64url(json.dumps(header, separators=(',', ':')).encode())}"
        f".{_b64url(json.dumps(payload, separators=(',', ':')).encode())}"
    )
    resp = boto3.client("kms").sign(
        KeyId=key_arn,
        Message=segments.encode("utf-8"),
        MessageType="RAW",
        SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256",
    )
    return f"{segments}.{_b64url(resp['Signature'])}"


def _verify_microsoft_id_token(id_token: str) -> dict:
    jwks_client = PyJWKClient(_MICROSOFT_JWKS_URI)
    signing_key = jwks_client.get_signing_key_from_jwt(id_token)

    return jwt.decode(
        id_token,
        signing_key.key,
        algorithms=["RS256"],
        audience=MICROSOFT_CLIENT_ID,
        issuer=_MICROSOFT_ISSUERS,
        options={"require": ["exp", "iss", "aud"]},
    )


def _extract_email(claims: dict) -> str | None:
    for key in ("preferred_username", "email", "upn"):
        value = claims.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


class LoginUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, id_token: str) -> Tuple[str, str, User]:
        if not _is_jwt_shape(id_token):
            raise InvalidJwtFormat("id_token")

        try:
            claims = _verify_microsoft_id_token(id_token)
        except Exception as err:
            raise InvalidJwtFormat("id_token") from err

        microsoft_oid = claims.get("oid") or claims.get("sub")
        email = _extract_email(claims)

        user = None
        if isinstance(microsoft_oid, str) and microsoft_oid.strip():
            user = self.repo.get_user(user_id=microsoft_oid.strip())

        if user is None and email:
            email_lower = email.lower()
            for candidate in self.repo.get_all_users():
                if candidate.email and candidate.email.lower() == email_lower:
                    user = candidate
                    break

        if user is None:
            raise NoItemsFound("user")

        role_value = user.role.value if hasattr(user.role, "value") else user.role
        access_payload = {
            "user_id": str(user.user_id),
            "role": role_value,
            "exp": int(time.time()) + _ACCESS_TOKEN_TTL_SECONDS,
        }
        access_token = _sign_access_token(access_payload)
        refresh_token = secrets.token_hex(32)

        # self.repo.save_refresh_token(user.user_id, refresh_token) — fora de escopo

        return access_token, refresh_token, user
