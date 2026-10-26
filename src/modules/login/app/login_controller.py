from .login_usecase import LoginUsecase
from .login_viewmodel import LoginViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import EnvVarNotFound, InvalidJwtFormat, NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import (
    BadRequest,
    InternalServerError,
    NotFound,
    OK,
)

_REFRESH_COOKIE = (
    "refresh_token={token}; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=604800"
)


class LoginController:
    def __init__(self, usecase: LoginUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            id_token = request.data.get("id_token")

            if id_token is None:
                raise MissingParameters("id_token")

            if type(id_token) is not str:
                raise WrongTypeParameter(
                    fieldName="id_token",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(id_token).__name__,
                )

            access_token, refresh_token, user = self.usecase(id_token=id_token)
            viewmodel = LoginViewmodel(access_token=access_token, user=user)

            return OK(
                viewmodel.to_dict(),
                headers={
                    "Set-Cookie": _REFRESH_COOKIE.format(token=refresh_token),
                },
            )

        except NoItemsFound as err:
            return NotFound(body=err.message)

        except MissingParameters as err:
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            return BadRequest(body=err.message)

        except EntityError as err:
            return BadRequest(body=err.message)

        except InvalidJwtFormat as err:
            return BadRequest(body=err.message)

        except EnvVarNotFound as err:
            return InternalServerError(body=err.message)

        except Exception as err:
            return InternalServerError(body=err.args[0] if err.args else str(err))
