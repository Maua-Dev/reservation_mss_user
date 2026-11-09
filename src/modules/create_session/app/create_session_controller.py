import json

from .create_session_usecase import CreateSessionUsecase
from .create_session_viewmodel import CreateSessionViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, Denied
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import BadRequest, InternalServerError, Created, NotFound


class CreateSessionController:

    def __init__(self, usecase: CreateSessionUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('user_from_authorizer') is None:
                raise Denied()

            user_from_authorizer = request.data.get('user_from_authorizer')

            if not isinstance(user_from_authorizer, dict):
                user_from_authorizer = json.loads(user_from_authorizer)

            if request.data.get('refresh_token') is None:
                raise MissingParameters('refresh_token')

            session = self.usecase(
                user_id=user_from_authorizer.get('id'),
                refresh_token=request.data.get('refresh_token')
            )

            viewmodel = CreateSessionViewmodel(session)

            return Created(viewmodel.to_dict())

        except DuplicatedItem as err:
            return BadRequest(body = err.message)

        except MissingParameters as err:
            return BadRequest(body = err.message)

        except EntityError as err:
            return BadRequest(body = err.message)

        except Denied as err:
            return NotFound(body = err.message)

        except Exception as err:
            return InternalServerError(body = err.args[0])