from .refresh_usecase import RefreshUsecase
from .refresh_viewmodel import RefreshViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import (
    EnvVarNotFound,
    ForbiddenAction,
    InvalidJwtFormat,
    NoItemsFound,
)
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import (
    BadRequest,
    Forbidden,
    InternalServerError,
    NotFound,
    OK,
)

_REFRESH_COOKIE = (
    "refresh_token={token}; HttpOnly; Secure; SameSite=None; Path=/; Max-Age=604800"
)


def _refresh_token_from_cookie(cookie_header: str | None) -> str | None:
    if not cookie_header or type(cookie_header) is not str:
        return None

    for part in cookie_header.split(";"):
        name, _, value = part.strip().partition("=")
        if name == "refresh_token" and value:
            return value

    return None


class RefreshController:
    def __init__(self, usecase: RefreshUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            refresh_token = request.data.get("refresh_token")
            if refresh_token is None:
                refresh_token = _refresh_token_from_cookie(
                    request.data.get("Cookie") or request.data.get("cookie")
                )

            # TODO valida se veio e se ta no formato string
            #      MissingParameters("refresh_token") / WrongTypeParameter(...)

            access_token, new_refresh_token = self.usecase(refresh_token=refresh_token)
            viewmodel = RefreshViewmodel(access_token=access_token)

            return OK(
                viewmodel.to_dict(),
                headers={
                    "Set-Cookie": _REFRESH_COOKIE.format(token=new_refresh_token),
                },
            )

        except NoItemsFound as err:
            return NotFound(body=err.message)

        except ForbiddenAction as err:
            return Forbidden(body=err.message)

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
