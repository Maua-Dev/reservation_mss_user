import json
from .get_all_users_usecase import GetAllUserUsecase
from .get_all_users_viewmodel import GetAllUsersViewModel
from src.shared.helpers.errors.controller_errors import Denied, MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError, NotFound

class GetAllUserSController:

    def __init__(self, usecase: GetAllUserUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:

        try:
            users = self.usecase()
            viewmodel = GetAllUsersViewModel(users)

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
    