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

MICROSOFT_TENANT_ID = os.environ.get("MICROSOFT_TENANT_ID")
MICROSOFT_CLIENT_ID = os.environ.get("MICROSOFT_CLIENT_ID")

# URL pública onde a Microsoft publica as chaves para validar a assinatura do id_token.
_MICROSOFT_JWKS_URI = (
    f"https://login.microsoftonline.com/{MICROSOFT_TENANT_ID}/discovery/v2.0/keys"
)

# Quem "emitiu" o token. Em produção o campo "iss" do JWT pode vir em um destes dois formatos.
# Por isso a lista tem os dois — o jwt.decode aceita tupla/lista de issuers.
_MICROSOFT_ISSUERS = (
    f"https://login.microsoftonline.com/{MICROSOFT_TENANT_ID}/v2.0",
    f"https://sts.windows.net/{MICROSOFT_TENANT_ID}/",
)

# Regex: caracteres permitidos em cada pedaço do JWT (base64url).
_JWT_B64 = re.compile(r"^[A-Za-z0-9_-]+$")

# Access token nosso vale 30 minutos.
_ACCESS_TOKEN_TTL_SECONDS = 30 * 60


def _is_jwt_shape(token: str) -> bool:
    """
    TODO — só checa se a STRING parece um JWT. Não valida assinatura nem conteúdo.

    Um JWT parece: "aaaa.bbbb.cccc" (três partes separadas por ponto).

    Faça assim, em ordem:
    1. Separe o token com token.split(".")
    2. Se NÃO tiver exatamente 3 partes → return False
    3. Se alguma parte for string vazia → return False
    4. Para CADA parte:
       a) Use _JWT_B64.fullmatch(parte). Se não bater → return False
       b) Tente decodificar com base64.urlsafe_b64decode.
          Se o tamanho não for múltiplo de 4, complete com "=" no final
          (ex.: pad = "=" * (-len(parte) % 4), depois decode parte+pad).
          Se o decode lançar Exception → return False
    5. Se passou por tudo → return True

    Imports já no topo: base64, e a regex _JWT_B64.
    """
    raise NotImplementedError("_is_jwt_shape")


def _b64url(data: bytes) -> str:
    """
    TODO — helper para montar JWT: transforma bytes em string base64url SEM o "=" no final.

    Passos:
    1. encoded = base64.urlsafe_b64encode(data)   # devolve bytes
    2. tire o padding: encoded.rstrip(b"=")
    3. transforme em str: .decode("ascii")
    4. return essa string

    Exemplo de uso depois: _b64url(b'{"alg":"RS256"}')
    """
    raise NotImplementedError("_b64url")


def _sign_access_token(payload: dict) -> str:
    """
    TODO — cria o access token DA NOSSA API e assina com a chave KMS da AWS.

    Contexto: depois do login Microsoft, a gente gera um JWT nosso (user_id, role, exp).
    A assinatura NÃO é feita com PyJWT — é o AWS KMS que assina (chave RSA já criada no CDK).

    Passos:
    1. key_arn = os.environ.get("LOGIN_KMS_SIGN_KEY_ARN")
       Se vier None/vazio → raise EnvVarNotFound("LOGIN_KMS_SIGN_KEY_ARN")

    2. Monte o header do JWT como dict:
       header = {"alg": "RS256", "typ": "JWT"}

    3. Transforme header e payload em JSON compacto (sem espaços):
       json.dumps(..., separators=(",", ":")).encode()   # vira bytes

    4. Codifique cada um com _b64url e junte com ponto:
       segments = _b64url(header_bytes) + "." + _b64url(payload_bytes)
       (isso é a parte "header.payload" do JWT, ainda sem assinatura)

    5. Chame o KMS:
       resp = boto3.client("kms").sign(
           KeyId=key_arn,
           Message=segments.encode("utf-8"),   # assina a string header.payload
           MessageType="RAW",
           SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256",
       )
       A assinatura vem em resp["Signature"] (bytes).

    6. Return o JWT completo:
       segments + "." + _b64url(resp["Signature"])

    Não use jwt.encode do PyJWT aqui.
    """
    raise NotImplementedError("_sign_access_token")


def _verify_microsoft_id_token(id_token: str) -> dict:
    """
    TODO — valida o id_token que o front mandou (emitido pela Microsoft) e devolve as claims (dict).

    Contexto: o front faz login no Microsoft e nos envia um id_token.
    Precisamos:
      - baixar a chave pública da Microsoft (JWKS)
      - verificar se a assinatura do token é válida
      - garantir que o token é pro nosso app (audience) e veio do tenant certo (issuer)
      - garantir que não expirou (exp)

    Passos:
    1. Crie o client de chaves:
       jwks_client = PyJWKClient(_MICROSOFT_JWKS_URI)

    2. Pegue a chave que assinou ESTE token:
       signing_key = jwks_client.get_signing_key_from_jwt(id_token)
       (a chave pública fica em signing_key.key)

    3. Decode e valide:
       return jwt.decode(
           id_token,
           signing_key.key,
           algorithms=["RS256"],
           audience=MICROSOFT_CLIENT_ID,   # tem que ser o Client ID do nosso app
           issuer=_MICROSOFT_ISSUERS,       # um dos dois issuers da constante acima
           options={"require": ["exp", "iss", "aud"]},
       )

    Importante:
    - Use o id_token (audience = nosso CLIENT_ID).
    - NÃO use o access token do Microsoft Graph (audience começa com 00000003-...).
      Esse outro token NÃO passa nessa validação — e não deve passar.

    Se der errado, deixe a Exception subir — o __call__ do usecase vai tratar.
    """
    raise NotImplementedError("_verify_microsoft_id_token")


def _extract_email(claims: dict) -> str | None:
    """
    TODO — tenta achar o e-mail do usuário dentro das claims do token Microsoft.

    A Microsoft às vezes manda o e-mail em campos diferentes. Tente nesta ordem:
      1) "preferred_username"
      2) "email"
      3) "upn"

    Para cada chave:
      - value = claims.get(chave)
      - se value for str e value.strip() não for vazio → return value.strip()

    Se nenhum campo servir → return None
    """
    raise NotImplementedError("_extract_email")


class LoginUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, id_token: str) -> Tuple[str, str, User]:
        """
        TODO — orquestra o login. Recebe o id_token Microsoft e devolve:
          (access_token_nosso, refresh_token, user_do_banco)

        Tipo de retorno: Tuple[str, str, User]

        ------------------------------------------------
        PASSO 1 — formato do token
        ------------------------------------------------
        Se _is_jwt_shape(id_token) for False:
            raise InvalidJwtFormat("id_token")
        (ainda não falamos com a Microsoft; só rejeita string malformada)

        ------------------------------------------------
        PASSO 2 — validar com a Microsoft
        ------------------------------------------------
        Tente:
            claims = _verify_microsoft_id_token(id_token)
        Se qualquer Exception acontecer:
            raise InvalidJwtFormat("id_token") from err
        (use try/except; o "from err" preserva o erro original no traceback)

        "claims" é um dict com dados do usuário Microsoft (oid, email, etc.).

        ------------------------------------------------
        PASSO 3 — achar o usuário no NOSSO banco
        ------------------------------------------------
        Pegue o id Microsoft:
            microsoft_oid = claims.get("oid") or claims.get("sub")
        Pegue o e-mail:
            email = _extract_email(claims)

        Comece com user = None

        3a) Se microsoft_oid for str e strip() não vazio:
                user = self.repo.get_user(user_id=microsoft_oid.strip())
            (get_user devolve o User ou None se não existir)

        3b) Se ainda user is None E email não for None:
                - normalize: email_lower = email.lower()
                - percorra self.repo.get_all_users()
                - para cada candidate, se candidate.email existir e
                  candidate.email.lower() == email_lower → user = candidate e pare o loop

        3c) Se depois disso user ainda for None:
                raise NoItemsFound("user")

        ------------------------------------------------
        PASSO 4 — gerar nossos tokens
        ------------------------------------------------
        role pode ser Enum; se tiver .value, use o .value, senão use o próprio role:
            role_value = user.role.value if hasattr(user.role, "value") else user.role

        Monte o payload do access token:
            {
              "user_id": str(user.user_id),
              "role": role_value,
              "exp": int(time.time()) + _ACCESS_TOKEN_TTL_SECONDS,
            }

        access_token = _sign_access_token(esse_payload)

        refresh_token = secrets.token_hex(32)
        (gera 32 bytes em hex → string com 64 caracteres)

        NÃO chame save_refresh_token — persistir refresh fica fora do escopo por enquanto.

        ------------------------------------------------
        PASSO 5 — retorno
        ------------------------------------------------
        return access_token, refresh_token, user

        ------------------------------------------------
        Como saber se está certo
        ------------------------------------------------
        Rode: pytest tests/modules/login/app/test_login_usecase.py -q
        Os 4 testes precisam passar (jwt inválido, user não encontrado, happy path por oid,
        fallback por e-mail).
        """
        raise NotImplementedError("LoginUsecase.__call__")
