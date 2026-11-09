import os
os.environ['STAGE'] = 'TEST'

import json
import uuid

from src.modules.delete_session.app.delete_session_presenter import lambda_handler


def build_event(user_id: str = None) -> dict:
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
        "body": "Hello from client!",
        "pathParameters": None,
        "isBase64Encoded": None,
        "stageVariables": None
    }


class Test_DeleteSessionPresenter:

    def test_delete_session_presenter(self):
        event = build_event(user_id="00000000-0000-0000-0000-000000000001")

        response = lambda_handler(event, None)
        body = json.loads(response['body'])

        assert response["statusCode"] == 200
        assert body['message'] == 'the session was deleted successfully'
        assert body['session']['user_id'] == "00000000-0000-0000-0000-000000000001"

    def test_delete_session_presenter_not_found(self):
        event = build_event(user_id=str(uuid.uuid4()))

        response = lambda_handler(event, None)

        assert response["statusCode"] == 404

    def test_delete_session_presenter_denied(self):
        event = build_event()

        response = lambda_handler(event, None)

        assert response["statusCode"] == 400