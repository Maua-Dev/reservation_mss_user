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
# Aceitar os dois issuers (v2.0 e sts.windows.net) — tokens reais usam um ou outro
_MICROSOFT_ISSUERS = (
    f"https://login.microsoftonline.com/{MICROSOFT_TENANT_ID}/v2.0",
    f"https://sts.windows.net/{MICROSOFT_TENANT_ID}/",
)

_JWT_B64 = re.compile(r"^[A-Za-z0-9_-]+$")
_ACCESS_TOKEN_TTL_SECONDS = 30 * 60


def _is_jwt_shape(token: str) -> bool:
    """
    TODO: validar formato bruto do JWT (sem verificar assinatura).
    - precisa ter exatamente 3 partes separadas por '.'
    - cada parte não-vazia e só com charset base64url (_JWT_B64)
    - cada parte deve conseguir ser base64.urlsafe_b64decode (com padding '=' se precisar)
    Retorna True/False. Olha os imports já disponíveis (re, base64).
    """
    raise NotImplementedError("_is_jwt_shape")


def _b64url(data: bytes) -> str:
    """
    TODO: base64url sem padding ('=').
    Dica: urlsafe_b64encode + rstrip(b'=') → str ascii.
    """
    raise NotImplementedError("_b64url")


def _sign_access_token(payload: dict) -> str:
    """
    TODO: montar e assinar o access token interno com KMS (RS256).
    1. Ler LOGIN_KMS_SIGN_KEY_ARN do env; se faltar → EnvVarNotFound("LOGIN_KMS_SIGN_KEY_ARN")
    2. Header JWT fixo: {"alg": "RS256", "typ": "JWT"}
    3. segments = b64url(header_json) + "." + b64url(payload_json)
       (json compacto: separators=(',', ':'))
    4. boto3 KMS sign:
       - Message = segments.encode("utf-8")
       - MessageType = "RAW"
       - SigningAlgorithm = "RSASSA_PKCS1_V1_5_SHA_256"
    5. Return segments + "." + b64url(Signature)
    NÃO use PyJWT encode aqui — a assinatura vem do KMS.
    """
    raise NotImplementedError("_sign_access_token")


def _verify_microsoft_id_token(id_token: str) -> dict:
    """
    TODO: validar o id_token da Microsoft (OIDC) e devolver as claims.
    1. PyJWKClient(_MICROSOFT_JWKS_URI).get_signing_key_from_jwt(id_token)
    2. jwt.decode com:
       - algorithms=["RS256"]
       - audience=MICROSOFT_CLIENT_ID  (é o id_token do APP, não o access token do Graph)
       - issuer=_MICROSOFT_ISSUERS
       - options require: exp, iss, aud
    Se vier access token do Graph (aud=00000003-...), isso deve falhar — correto.
    """
    raise NotImplementedError("_verify_microsoft_id_token")


def _extract_email(claims: dict) -> str | None:
    """
    TODO: pegar e-mail das claims, na ordem:
    preferred_username → email → upn
    Só aceitar str não-vazia (strip). Se nada servir, None.
    """
    raise NotImplementedError("_extract_email")


class LoginUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, id_token: str) -> Tuple[str, str, User]:
        """
        Fluxo (implementar ~tudo abaixo). Retorno: (access_token, refresh_token, user)

        1. Shape do JWT
           - se _is_jwt_shape falhar → InvalidJwtFormat("id_token")

        2. Verificar assinatura/claims Microsoft
           - chamar _verify_microsoft_id_token
           - qualquer Exception → InvalidJwtFormat("id_token") (encadear com `from err`)

        3. Identificar o usuário no nosso banco
           - microsoft_oid = claims["oid"] ou, fallback, claims["sub"]
           - email = _extract_email(claims)
           - primeiro tenta repo.get_user(user_id=oid) se oid for str válida
           - se não achou e tem email: varre repo.get_all_users() comparando email.lower()
           - se ainda None → NoItemsFound("user")

        4. Emitir tokens nossos
           - access payload: user_id, role (usar .value se Enum), exp = now + _ACCESS_TOKEN_TTL_SECONDS
           - access_token = _sign_access_token(payload)
           - refresh_token = secrets.token_hex(32)  # 64 chars hex
           - NÃO persistir refresh ainda (save_refresh_token fora de escopo)

        5. return access_token, refresh_token, user

        Testes em tests/modules/login/app/test_login_usecase.py — rode e faça passar.
        """
        raise NotImplementedError("LoginUsecase.__call__")
