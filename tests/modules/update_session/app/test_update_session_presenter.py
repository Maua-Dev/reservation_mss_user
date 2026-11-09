import os
os.environ['STAGE'] = 'TEST'

import json
import uuid

from src.modules.update_session.app.update_session_presenter import lambda_handler


def build_event(user_id: str = None, new_refresh_token: str = None) -> dict:
    authorizer = {"user": {"id": user_id}} if user_id is not None else {}

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
            "new_refresh_token": new_refresh_token
        }),
        "pathParameters": None,
        "isBase64Encoded": None,
        "stageVariables": None
    }


class Test_UpdateSessionPresenter:

    def test_update_session_presenter(self):
        event = build_event(user_id="00000000-0000-0000-0000-000000000001", new_refresh_token="token_novo")

        response = lambda_handler(event, None)
        body = json.loads(response['body'])

        assert response["statusCode"] == 200
        assert body['message'] == 'the session was updated'
        assert body['updated_session']['user_id'] == "00000000-0000-0000-0000-000000000001"
        assert body['updated_session']['refresh_token'] == "token_novo"

    def test_update_session_presenter_not_found(self):
        event = build_event(user_id=str(uuid.uuid4()), new_refresh_token="token_novo")

        response = lambda_handler(event, None)

        assert response["statusCode"] == 404

    def test_update_session_presenter_denied(self):
        event = build_event(new_refresh_token="token_novo")

        response = lambda_handler(event, None)

        assert response["statusCode"] == 400