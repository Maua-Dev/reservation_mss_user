import os
os.environ['STAGE'] = 'TEST'

import json
import uuid

from src.modules.create_session.app.create_session_presenter import lambda_handler


def build_event(user_id: str = None, refresh_token: str = None) -> dict:
    authorizer = {"user": {"id": user_id, "mail": "teste@gmail.com", "displayName": "Usuario Teste"}} if user_id else {}

    return {
        "version": "2.0",
        "routeKey": "$default",
        "rawPath": "/my/path",
        "headers": {
            "header1": "value1"
        },
        "requestContext": {
            "accountId": "123456789012",
            "apiId": "<urlid>",
            "authorizer": authorizer,
            "requestId": "id",
            "routeKey": "$default",
            "stage": "$default"
        },
        "body": json.dumps({
        "refresh_token": refresh_token
        }),
        "pathParameters": None,
        "isBase64Encoded": None,
        "stageVariables": None
    }


class Test_CreateSessionPresenter:

    def test_create_session_presenter(self):
        user_id = str(uuid.uuid4())
        event = build_event(user_id=user_id, refresh_token="novo_token")

        response = lambda_handler(event, None)
        body = json.loads(response['body'])

        assert response["statusCode"] == 201
        assert body['message'] == 'the session was created successfully'
        assert body['session']['user_id'] == user_id
        assert body['session']['refresh_token'] == "novo_token"

    def test_create_session_presenter_denied(self):
        event = build_event(refresh_token="novo_token")

        response = lambda_handler(event, None)

        assert response["statusCode"] == 404