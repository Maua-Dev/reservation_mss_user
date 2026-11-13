from .refresh_controller import RefreshController
from .refresh_usecase import RefreshUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import (
    LambdaHttpRequest,
    LambdaHttpResponse,
)

session_repo = Environments.get_session_repo_instance()
user_repo = Environments.get_user_repo_instance()
usecase = RefreshUsecase(session_repo=session_repo, user_repo=user_repo)
controller = RefreshController(usecase)


def refresh_presenter(event, context):
    http_request = LambdaHttpRequest(data=event)
    response = controller(http_request)
    http_response = LambdaHttpResponse(
        status_code=response.status_code,
        body=response.body,
        headers=response.headers,
    )
    return http_response.toDict()


def lambda_handler(event, context):
    return refresh_presenter(event, context)
