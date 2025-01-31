from .update_user_usecase import UpdateUserUsecase
from .update_user_viewmodel import UpdateUserViewModel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import BadRequest, OK, InternalServerError, NotFound
from src.shared.domain.enums.role_enum import ROLE

class UpdateUserController:

    def __init__(self, usecase: UpdateUserUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest):
        try:

            if request.data.get('user_id') is None:
                raise MissingParameters('user_id')
            
            if type(request.data.get('user_id')) is not str:
                raise WrongTypeParameter(fieldName='user_id', fieldTypeExpected=str,
                                         fieldTypeReceived=type(request.data.get('user_id')))
            
            role_str = request.data.get('new_role')

            if role_str:
                if role_str not in [role_type.value for role_type in ROLE]:
                    raise EntityError('new_role')

            confirm_user_bool = request.data.get('new_confirm_user')

            if confirm_user_bool is not None:
                if type(confirm_user_bool) is not bool:
                    raise WrongTypeParameter(
                        fieldName='confirm_user',
                        fieldTypeExpected=bool,
                        fieldTypeReceived=type(confirm_user_bool))

                
            user = self.usecase(
                user_id=request.data.get('user_id') or request.data.get('authorizer', {}).get('claims', {}).get('user_id'),
                role=ROLE[role_str] if role_str is not None else None,
                confirm_user=confirm_user_bool
            )
            viewmodel = UpdateUserViewModel(user=user)

            return OK(viewmodel.to_dict())
        
        except NoItemsFound as err:
            return NotFound(body=err.message)
        
        except MissingParameters as err:
            return BadRequest(body=err.message)
        
        except WrongTypeParameter as err:
            return BadRequest(body=err.message)
        
        except EntityError as err:
            return BadRequest(body=err.message)
        
        except Exception as err:
            return InternalServerError(body=err.args[0])