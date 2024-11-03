from .get_user_usecase import GetUserUseCase
from .get_user_viewmodel import GetUserViewModel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import BadRequest, NotFound, InternalServerError, OK

class GetUserController:
    def __init__(self, usecase: GetUserUseCase):
        self.usecase = usecase

    def __call__(self, request: IRequest):
        try:
            if request.data.get('user_id') is None:
                raise MissingParameters('user_id')
            
            user_id = request.data.get('user_id')

            if user_id is not None:
                if type(user_id) is not str:
                    raise WrongTypeParameter('user_id', 'str', type(user_id).__name__)
            
            user = self.usecase(
                user_id = request.data.get('user_id')
           )
            
            user_viewmodel = GetUserViewModel(user = user)

            return OK(user_viewmodel.to_dict())
        
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