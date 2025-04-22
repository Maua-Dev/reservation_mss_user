import json
from src.modules.update_user.app.update_user_presenter import lambda_handler


class Test_UpdateMemberPresenter:
    def test_update_user_presenter(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "",
            "cookies": [],
            "headers": {},
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {
                    "user": {
                        "id": "93bc6ada-c0d1-7054-26ab-e17414c48ae3",
                        "ra": "24.01460-5",
                        "name": "Rodas Rodas",
                        "email": "rodas@gmail.com",
                        "confirm_user": False,
                        "role": "STUDENT"
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
            "body": '{"new_role": "STUDENT", "new_confirm_user": true}',
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 200
        parsed_body = json.loads(response["body"])
        assert parsed_body["message"] == "the user was updated"
        assert parsed_body["updated_user"]["user_id"] == "93bc6ada-c0d1-7054-26ab-e17414c48ae3"
        assert parsed_body["updated_user"]["role"] == "STUDENT"
        assert parsed_body["updated_user"]["confirm_user"] == True

    def test_update_user_presenter_invalid(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "",
            "cookies": [],
            "headers": {},
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {
                }
            },
            "body": '{"new_role": "STUDENT", "new_confirm_user": true}',
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 400
        assert json.loads(response["body"]) == "Authorizer denied token, user was not returned from it"
