from .create_session_controller import CreateSessionController
from .create_session_usecase import CreateSessionUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo = Environments.get_session_repo_instance()
usecase = CreateSessionUsecase(repo)
controller = CreateSessionController(usecase)


def create_session_presenter(event, context):
    httpRequest = LambdaHttpRequest(data=event)
    httpRequest.data['user_from_authorizer'] = event.get('requestContext', {}).get('authorizer', {}).get('user', None)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()


def lambda_handler(event, context):
    response = create_session_presenter(event, context)

    return response