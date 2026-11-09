from .delete_session_controller import DeleteSessionController
from .delete_session_usecase import DeleteSessionUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo = Environments.get_session_repo_instance()
usecase = DeleteSessionUsecase(repo)
controller = DeleteSessionController(usecase)


def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data=event)
    httpRequest.data['user_from_authorizer'] = event.get('requestContext', {}).get('authorizer', {}).get('user', None)
    response = controller(request=httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()