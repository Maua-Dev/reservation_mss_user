import json

from .get_user_usecase import GetUserUsecase
from .get_user_viewmodel import GetUserViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter, Denied
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import BadRequest, NotFound, InternalServerError, OK


class GetUserController:
    def __init__(self, usecase: GetUserUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest):
        try:
            user_from_authorizer = request.data.get('user_from_authorizer')

            if user_from_authorizer is None:
                raise Denied()

            if isinstance(user_from_authorizer, str):
                try:
                    user_from_authorizer = json.loads(user_from_authorizer)
                except json.JSONDecodeError:
                    raise Denied()


            if not isinstance(user_from_authorizer, dict) or 'user_id' not in user_from_authorizer:
                raise MissingParameters('user_id')

            user = self.usecase(user_id=user_from_authorizer['user_id'])
            viewmodel = GetUserViewmodel(user)

            return OK(viewmodel.to_dict())
        
        except Denied as err:
            return BadRequest(body=err.message)
        
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
        
