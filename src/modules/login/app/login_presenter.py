from .login_controller import LoginController
from .login_usecase import LoginUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import (
    LambdaHttpRequest,
    LambdaHttpResponse,
)

repo = Environments.get_user_repo_instance()
usecase = LoginUsecase(repo)
controller = LoginController(usecase)


def login_presenter(event, context):
    http_request = LambdaHttpRequest(data=event)
    response = controller(http_request)
    http_response = LambdaHttpResponse(
        status_code=response.status_code,
        body=response.body,
        headers=response.headers,
    )
    return http_response.toDict()


def lambda_handler(event, context):
    return login_presenter(event, context)
