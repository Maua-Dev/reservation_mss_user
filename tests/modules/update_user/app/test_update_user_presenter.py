import json
from src.modules.update_user.app.update_user_presenter import lambda_handler


class Test_UpdateMemberPresenter:
    def test_update_user_presenter(self):
        event = {
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
                    "claims":
                        {
                            "ra": "24.01460-5",
                            "name":"Rodas Rodas",
                            "email": "rodas@gmail.com",
                            "user_id": "93bc6ada-c0d1-7054-26ab-e17414c48ae3",
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
            "body": {"user_id" : "93bc6ada-c0d1-7054-26ab-e17414c48ae3", "new_role": "STUDENT","confirm_user": True},
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }
        
        response = lambda_handler(event, None)
        
        assert response["statusCode"] == 200
        assert json.loads(response["body"])
        assert json.loads(response["body"])["message"] == "User information was updated successfully."
        assert json.loads(response["body"])["updated_user"]["user_id"] == "93bc6ada-c0d1-7054-26ab-e17414c48ae3"
        assert json.loads(response["body"])["updated_user"]["role"] == "STUDENT"
        assert json.loads(response["body"])["updated_user"]["confirm_user"] == True
    
    def test_update_user_presenter_invalid(self):
        event = {
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
                    "claims":
                        {
                            "ra": "24.01460-5",
                            "name":"Rodas Rodas",
                            "email": "rodas@gmail.com",
                            "user_id": "93bc6ada-c0d1-7054-26ab-e17414c48ae3",
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
            "body": '{"new_role": "STUDENT","new_confirm_user": True}',
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }
        
        response = lambda_handler(event, None)

        
        assert response["statusCode"] == 400
        assert json.loads(response["body"]) == 'Field user_id is missing'
