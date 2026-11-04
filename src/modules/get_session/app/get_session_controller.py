import json

from .get_session_usecase import GetSessionUsecase
from .get_session_viewmodel import GetSessionViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter, Denied
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import BadRequest, NotFound, InternalServerError, OK


class GetSessionController:
    def __init__(self, usecase: GetSessionUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest):
        try:

            if request.data.get('user_from_authorizer') is None:
                raise Denied()

            user_to_get = request.data.get('user_from_authorizer')

            if not isinstance(user_to_get, dict):
                user_to_get = json.loads(user_to_get)

            session = self.usecase(user_id=user_to_get.get('id'))
            viewmodel = GetSessionViewmodel(session)

            return OK(viewmodel.to_dict())

        except Denied as err:
            return BadRequest(body=err.message)

        except MissingParameters as err:
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            return BadRequest(body=err.message)

        except NoItemsFound as err:
            return NotFound(body=err.message)

        except EntityError as err:
            return InternalServerError(body=err.message)

        except Exception as err:
            return InternalServerError(body=str(err))