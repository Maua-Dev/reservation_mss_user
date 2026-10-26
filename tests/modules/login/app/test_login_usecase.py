from unittest.mock import MagicMock, patch

import pytest

from src.modules.login.app.login_usecase import LoginUsecase
from src.shared.helpers.errors.usecase_errors import InvalidJwtFormat, NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestLoginUsecase:
    def test_login_usecase_invalid_jwt_shape(self):
        repo = UserRepositoryMock()
        usecase = LoginUsecase(repo=repo)

        with pytest.raises(InvalidJwtFormat):
            usecase(id_token="not-a-jwt")

    def test_login_usecase_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = LoginUsecase(repo=repo)

        with patch(
            "src.modules.login.app.login_usecase._verify_microsoft_id_token",
            return_value={
                "oid": "00000000-0000-0000-0000-000000000000",
                "preferred_username": "missing@maua.br",
            },
        ):
            with pytest.raises(NoItemsFound):
                usecase(id_token="aaa.bbb.ccc")

    def test_login_usecase_happy_path_by_oid(self):
        repo = UserRepositoryMock()
        user = repo.users_list[0]
        usecase = LoginUsecase(repo=repo)

        with patch(
            "src.modules.login.app.login_usecase._verify_microsoft_id_token",
            return_value={
                "oid": user.user_id,
                "preferred_username": user.email,
            },
        ), patch(
            "src.modules.login.app.login_usecase._sign_access_token",
            return_value="signed.access.token",
        ) as sign_mock:
            access_token, refresh_token, returned_user = usecase(id_token="aaa.bbb.ccc")

        assert access_token == "signed.access.token"
        assert len(refresh_token) == 64
        assert returned_user.user_id == user.user_id
        sign_mock.assert_called_once()
        payload = sign_mock.call_args[0][0]
        assert payload["user_id"] == user.user_id
        assert payload["role"] == user.role.value
        assert "exp" in payload

    def test_login_usecase_fallback_lookup_by_email(self):
        repo = UserRepositoryMock()
        user = repo.users_list[0]
        usecase = LoginUsecase(repo=repo)

        with patch(
            "src.modules.login.app.login_usecase._verify_microsoft_id_token",
            return_value={
                "oid": "00000000-0000-0000-0000-000000000099",
                "email": user.email,
            },
        ), patch(
            "src.modules.login.app.login_usecase._sign_access_token",
            return_value="signed.access.token",
        ):
            access_token, refresh_token, returned_user = usecase(id_token="aaa.bbb.ccc")

        assert access_token == "signed.access.token"
        assert returned_user.email == user.email
        assert len(refresh_token) == 64
