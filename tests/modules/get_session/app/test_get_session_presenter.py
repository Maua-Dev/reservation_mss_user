import os
os.environ['STAGE'] = 'TEST'

import json
from src.modules.get_session.app.get_session_presenter import lambda_handler
from src.shared.infra.repositories.session_repository_mock import SessionRepositoryMock

first_session = SessionRepositoryMock().sessions[0]


def build_event(user_id: str) -> dict:
    return {
        "version": "2.0",
        "routeKey": "$default",
        "rawPath": "/my/path",
        "rawQueryString": "parameter1=value1&parameter1=value2&parameter2=value",
        "cookies": [
            "cookie1",
            "cookie2"
        ],
        "headers": {
            "header1": "value1",
            "header2": "value1,value2"
        },
        "requestContext": {
            "accountId": "123456789012",
            "apiId": "<urlid>",
            "authentication": None,
            "authorizer": {
                "user":
                {
                    "id": user_id,
                    "name": "Usuario Teste",
                    "email": "teste@gmail.com"
                }
            },
            "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
            "domainPrefix": "<url-id>",
            "external_interfaces": {
                "method": "POST",
                "path": "/my/path",
                "protocol": "HTTP/1.1",
                "sourceIp": "123.123.123.123",
                "userAgent": "agent"
            },
            "requestId": "id",
            "routeKey": "$default",
            "stage": "$default",
            "time": "12/Mar/2020:19:03:58 +0000",
            "timeEpoch": 1583348638390
        },
        "body": "Hello from client!",
        "pathParameters": None,
        "isBase64Encoded": None,
        "stageVariables": None
    }


class TestGetSessionPresenter:

    def test_get_session_presenter(self):
        event = build_event(user_id=first_session.user_id)

        response = lambda_handler(event, None)
        body = json.loads(response['body'])

        assert response["statusCode"] == 200
        assert body['message'] == 'the session was retrieved'
        assert body['session']['user_id'] == first_session.user_id
        assert body['session']['refresh_token'] == first_session.refresh_token

    def test_get_session_presenter_not_found(self):
        event = build_event(user_id="00000000-0000-0000-0000-000000000099")

        response = lambda_handler(event, None)

        assert response["statusCode"] == 404