import json
from src.modules.delete_user.app.delete_user_usecase import DeleteUserUsecase
from src.modules.delete_user.app.delete_user_viewmodel import DeleteUserViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter, Denied
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError, NotFound

class DeleteUserController:
    def __init__(self, usecase: DeleteUserUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('user_from_authorizer') is None:
                raise Denied()

            user_data = request.data.get('user_from_authorizer')

            if not isinstance(user_data, dict):
                user_data = json.loads(user_data)

            user_id = user_data.get('id')

            if not isinstance(user_id, str):
                raise WrongTypeParameter('user_id', expected_type='str')

            user = self.usecase(user_id=user_id)
            viewmodel = DeleteUserViewmodel(user)

            return OK(viewmodel.to_dict())

        except Denied as err:
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            return BadRequest(body=f"Field {err.parameter} should be of type {err.expected_type}")

        except EntityError as err:
            return BadRequest(body=err.message)

        except NoItemsFound as err:
            return NotFound(body=err.message)

        except Exception as err:
            return InternalServerError(body=str(err))
