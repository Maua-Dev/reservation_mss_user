from typing import Any
from .update_user_usecase import UpdateUserUsecase
from .update_user_viewmodel import UpdateUserViewModel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import BadRequest, OK, InternalServerError, NotFound
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.domain_errors import EntityParameterError

class UpdateUserController:

    def __init__(self, usecase: UpdateUserUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest):
        try:
            user_id = request.data.get('user_id')
            if user_id is None:
                raise MissingParameters('user_id')

            if not isinstance(user_id, str):
                raise WrongTypeParameter('user_id', 'str', type(user_id).__name__)

            confirm_user = request.data.get('confirm_user')
            if confirm_user is None:
                raise MissingParameters('confirm_user')

            if not isinstance(confirm_user, bool):
                raise WrongTypeParameter('confirm_user', 'bool', type(confirm_user).__name__)

            role_str = request.data.get('role')
            if role_str is None:
                raise MissingParameters('role')

            if not isinstance(role_str, str) or role_str not in [role.value for role in ROLE]:
                raise EntityParameterError('Field role is not valid')

            updated_user = self.usecase(user_id=user_id, confirm_user=confirm_user, role=ROLE[role_str])

            viewmodel = UpdateUserViewModel(updated_user)
            return OK(viewmodel.to_dict())
        
        except EntityError as err:  
            if "User not found" in str(err): 
                return NotFound(body="User not found")  
            return BadRequest(body=err.message)

        except NoItemsFound as err:
            return NotFound(body=err.message)

        except MissingParameters as err:
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            return BadRequest(body=err.message)

        except EntityParameterError as err:
            return BadRequest(body=err.message)

        except EntityError as err:
            return BadRequest(body=err.message)

        except Exception as err:
            return InternalServerError(body=err.args[0])
