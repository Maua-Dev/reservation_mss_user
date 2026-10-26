import os

# Dummies para CI/local — não usam secrets reais.
# STAGE=TEST força UserRepositoryMock (evita Dynamo/rede).
# LOGIN_KMS / GRAPH só precisam existir se algum código ler o env;
# nos testes de login o sign/verify da Microsoft/KMS continua mockado.
os.environ.setdefault("STAGE", "TEST")
os.environ.setdefault(
    "GRAPH_MICROSOFT_ENDPOINT",
    "https://graph.microsoft.com/v1.0/me",
)
os.environ.setdefault(
    "LOGIN_KMS_SIGN_KEY_ARN",
    "arn:aws:kms:us-east-1:000000000000:key/00000000-0000-0000-0000-000000000000",
)
os.environ.setdefault(
    "CORS_ALLOW_ORIGIN",
    "https://reservation.dev.devmaua.com",
)
