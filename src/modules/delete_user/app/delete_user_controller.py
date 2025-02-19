from src.modules.delete_user.app.delete_user_usecase import DeleteUserUsecase
from src.modules.delete_user.app.delete_user_viewmodel import DeleteUserViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError, NotFound


class DeleteUserController:
    def __init__(self, usecase:  DeleteUserUsecase):
        self.usecase = usecase
        
    def __call__(self, request: IRequest) -> IResponse:
        try:
            user_id = request.data.get('user_id')

            if user_id is None:
                raise MissingParameters('user_id')
            
            if not isinstance(user_id, str):
                raise WrongTypeParameter('user_id', expected_type='str')
            
            user = self.usecase(user_id=user_id)
            viewmodel = DeleteUserViewmodel(user)
            
            return OK(viewmodel.to_dict())

        except MissingParameters as err:
            return BadRequest(body=f"Field user_id is missing")

        except WrongTypeParameter as err:
            return BadRequest(body=f"Field {err.parameter} should be of type {err.expected_type}")
        
        except EntityError as err:
            return BadRequest(body=err.message)

        except NoItemsFound as err:
            return NotFound(body=err.message)

        except Exception as err:
            return InternalServerError(body=err.args[0])