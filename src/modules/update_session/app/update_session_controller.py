import json

from .update_session_usecase import UpdateSessionUsecase
from .update_session_viewmodel import UpdateSessionViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter, Denied
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import BadRequest, OK, InternalServerError, NotFound


class UpdateSessionController:
    def __init__(self, usecase: UpdateSessionUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest):
        try:
            user_data = request.data.get('user_from_authorizer')

            if user_data is None:
                raise Denied()

            if not isinstance(user_data, dict):
                user_data = json.loads(user_data)

            user_id = user_data.get('id')
            new_refresh_token = request.data.get('new_refresh_token', None)

            if user_id is None:
                raise MissingParameters('user_id')

            if not isinstance(user_id, str):
                raise WrongTypeParameter(fieldName='user_id', fieldTypeExpected=str, fieldTypeReceived=type(user_id))

            if new_refresh_token is None:
                raise MissingParameters('new_refresh_token')

            if not isinstance(new_refresh_token, str):
                raise WrongTypeParameter(fieldName='new_refresh_token',
                                         fieldTypeExpected=str,
                                         fieldTypeReceived=type(new_refresh_token))

            session = self.usecase(user_id=user_id, new_refresh_token=new_refresh_token)

            viewmodel = UpdateSessionViewmodel(session=session)
            return OK(viewmodel.to_dict())

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