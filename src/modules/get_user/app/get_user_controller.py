import json

from .get_user_usecase import GetUserUseCase
from .get_user_viewmodel import GetUserViewModel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter, Denied
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import BadRequest, NotFound, InternalServerError, OK


class GetUserController:
    def __init__(self, usecase: GetUserUseCase):
        self.usecase = usecase

    def __call__(self, request: IRequest):
        try:
            if request.data.get('user_from_authorizer') is None:
                raise Denied()

            if isinstance(request.data.get('user_from_authorizer'), str):

                user_to_get = json.loads(request.data.get('user_from_authorizer'))

            else:

                user_to_get = request.data.get('user_from_authorizer')

            user = self.usecase(
                user_id=user_to_get['id'],
            )

            viewmodel = GetUserViewModel(user)

            return OK(viewmodel.to_dict())
        
        except MissingParameters as err:
            return BadRequest(body = err.message)
        
        except WrongTypeParameter as err:
            return BadRequest(body = err.message)
        
        except NoItemsFound as err:
            return NotFound(body = err.message)
        
        except EntityError as err:
            return InternalServerError(body = err.message)
        
        except Exception as err:
            return InternalServerError(body = str(err))