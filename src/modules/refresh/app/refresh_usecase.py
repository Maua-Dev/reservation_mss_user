import base64
import json
import os
import re
import time
from typing import Tuple

import boto3

from src.shared.domain.entities.session import Session
from src.shared.domain.repositories.session_repository_interface import ISessionRepository
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import (
    EnvVarNotFound,
    ForbiddenAction,
    InvalidJwtFormat,
    NoItemsFound,
)

_JWT_B64 = re.compile(r"^[A-Za-z0-9_-]+$")
_ACCESS_TOKEN_TTL_SECONDS = 30 * 60
_REFRESH_TOKEN_TTL_SECONDS = 7 * 24 * 60 * 60


def _is_jwt_shape(token: str) -> bool:
    split_token = token.split(".")
    if len(split_token) != 3:
        return False

    for partition in split_token:
        if not partition or _JWT_B64.fullmatch(partition) is None:
            return False
        padding = "=" * (-len(partition) % 4)
        try:
            base64.urlsafe_b64decode(partition + padding)
        except Exception:
            return False

    return True


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def _kms_key_arn() -> str:
    key_arn = os.environ.get("LOGIN_KMS_SIGN_KEY_ARN")
    if not key_arn:
        raise EnvVarNotFound("LOGIN_KMS_SIGN_KEY_ARN")
    return key_arn


def _sign_jwt(payload: dict) -> str:
    key_arn = _kms_key_arn()
    header = {"alg": "RS256", "typ": "JWT"}
    header_bytes = json.dumps(header, separators=(",", ":")).encode()
    payload_bytes = json.dumps(payload, separators=(",", ":")).encode()
    segments = _b64url(header_bytes) + "." + _b64url(payload_bytes)

    resp = boto3.client("kms").sign(
        KeyId=key_arn,
        Message=segments.encode("utf-8"),
        MessageType="RAW",
        SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256",
    )
    return segments + "." + _b64url(resp["Signature"])


def _verify_kms_jwt(token: str) -> dict:
    if not _is_jwt_shape(token):
        raise InvalidJwtFormat("refresh_token")

    key_arn = _kms_key_arn()
    header_b64, payload_b64, signature_b64 = token.split(".")
    segments = f"{header_b64}.{payload_b64}"

    try:
        boto3.client("kms").verify(
            KeyId=key_arn,
            Message=segments.encode("utf-8"),
            MessageType="RAW",
            Signature=_b64url_decode(signature_b64),
            SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256",
        )
        payload = json.loads(_b64url_decode(payload_b64))
    except InvalidJwtFormat:
        raise
    except Exception as err:
        raise InvalidJwtFormat("refresh_token") from err

    if not isinstance(payload, dict):
        raise InvalidJwtFormat("refresh_token")

    exp = payload.get("exp")
    if exp is None or int(time.time()) >= int(exp):
        raise InvalidJwtFormat("refresh_token")

    return payload


def _sign_access_token(payload: dict) -> str:
    return _sign_jwt(payload)


def _sign_refresh_token(user_id: str) -> str:
    return _sign_jwt(
        {
            "user_id": user_id,
            "typ": "refresh",
            "exp": int(time.time()) + _REFRESH_TOKEN_TTL_SECONDS,
        }
    )


class RefreshUsecase:
    def __init__(self, session_repo: ISessionRepository, user_repo: IUserRepository):
        self.session_repo = session_repo
        self.user_repo = user_repo

    def __call__(self, refresh_token: str) -> Tuple[str, str]:
        
        claims = # TODO chama a função _verify_kms_jwt pra verificar o token

        if claims.get("typ") != "refresh":
            raise InvalidJwtFormat("refresh_token")
        
        # TODO pega o user_id da variavel claims - claims.get(...)
        # valida se ta e formato string e se ta ali (nao nulo) - raise InvalidJwtFormat se nao tiver

        # TODO chama o session_repo e da um get_session com o user id

        # TODO se o session.refresh_token for diferente do que veio na nossa requisição
        # raise ForbiddenAction("refresh_token")

        user = self.user_repo.get_user(user_id)
        if user is None:
            raise NoItemsFound("user_id")

        role_value = user.role.value if hasattr(user.role, "value") else user.role
        access_token = _sign_access_token(
            {
                "user_id": str(user.user_id),
                "role": role_value,
                "exp": int(time.time()) + _ACCESS_TOKEN_TTL_SECONDS,
            }
        )

        new_refresh_token = _sign_refresh_token(str(user.user_id))
        
        # TODO chama um session_repo.update_session e passa user_id + novo refresh que foi gerado

        return access_token, new_refresh_token
