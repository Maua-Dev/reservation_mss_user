import json

from .delete_session_usecase import DeleteSessionUsecase
from .delete_session_viewmodel import DeleteSessionViewmodel
from src.shared.helpers.errors.controller_errors import Denied
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError, NotFound


class DeleteSessionController:
    def __init__(self, usecase: DeleteSessionUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('user_from_authorizer') is None:
                raise Denied()

            user_data = request.data.get('user_from_authorizer')

            if not isinstance(user_data, dict):
                user_data = json.loads(user_data)

            session = self.usecase(user_id=user_data.get('id'))
            viewmodel = DeleteSessionViewmodel(session)

            return OK(viewmodel.to_dict())

        except Denied as err:
            return BadRequest(body=err.message)

        except EntityError as err:
            return BadRequest(body=err.message)

        except NoItemsFound as err:
            return NotFound(body=err.message)

        except Exception as err:
            return InternalServerError(body=str(err))