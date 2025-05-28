from .update_user_usecase import UpdateUserUsecase
from .update_user_viewmodel import UpdateUserViewModel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter, Denied
from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import BadRequest, OK, InternalServerError, NotFound, Forbidden
from src.shared.domain.enums.role_enum import ROLE
import json

class UpdateUserController:
    def __init__(self, usecase: UpdateUserUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest):
        try:
            user_data = request.data.get('user_from_authorizer')

            if user_data is None:
                raise Denied()

            if not isinstance(user_data, dict):
                user_data = json.loads(user_data)

            user_id = user_data.get('id')
            new_role = request.data.get('new_role', None)
            new_confirm_user = request.data.get('new_confirm_user', None)

            if user_id is None:
                raise MissingParameters('user_id')

            if not isinstance(user_id, str):
                raise WrongTypeParameter(fieldName='user_id', fieldTypeExpected=str, fieldTypeReceived=type(user_id))

            if new_role:
                if not isinstance(new_role, str):
                    raise WrongTypeParameter(fieldName='new_role',
                                             fieldTypeExpected=str,
                                             fieldTypeReceived=type(new_role))

            if new_confirm_user:
                if not isinstance(new_confirm_user, bool):
                    raise WrongTypeParameter(fieldName='new_confirm_user',
                                             fieldTypeExpected=bool,
                                             fieldTypeReceived=type(new_confirm_user))

            user = self.usecase(
                user_id=user_id,
                new_role=new_role if new_role is not None else None,
                new_confirm_user=new_confirm_user if new_confirm_user is not None else None
            )

            viewmodel = UpdateUserViewModel(user=user)
            return OK(viewmodel.to_dict())

        except ForbiddenAction as err:
            return Forbidden(body=err.message)
        except NoItemsFound as err:
            return NotFound(body=err.message)
        except MissingParameters as err:
            return BadRequest(body=err.message)
        except WrongTypeParameter as err:
            return BadRequest(body=err.message)
        except EntityError as err:
            return BadRequest(body=err.message)
        except Denied as err:
            return BadRequest(body=err.message)
        except Exception as err:
            return InternalServerError(body=str(err))
