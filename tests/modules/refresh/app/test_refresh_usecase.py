from unittest.mock import patch

import pytest

from src.modules.refresh.app.refresh_usecase import RefreshUsecase
from src.shared.domain.entities.session import Session
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, InvalidJwtFormat, NoItemsFound
from src.shared.infra.repositories.session_repository_mock import SessionRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestRefreshUsecase:
    def test_refresh_usecase_invalid_jwt_shape(self):
        session_repo = SessionRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = RefreshUsecase(session_repo=session_repo, user_repo=user_repo)

        with pytest.raises(InvalidJwtFormat):
            usecase(refresh_token="not-a-jwt")

    def test_refresh_usecase_session_not_found(self):
        session_repo = SessionRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = RefreshUsecase(session_repo=session_repo, user_repo=user_repo)

        with patch(
            "src.modules.refresh.app.refresh_usecase._verify_kms_jwt",
            return_value={
                "user_id": "00000000-0000-0000-0000-000000000099",
                "typ": "refresh",
            },
        ):
            with pytest.raises(NoItemsFound):
                usecase(refresh_token="aaa.bbb.ccc")

    def test_refresh_usecase_token_mismatch(self):
        session_repo = SessionRepositoryMock()
        user_repo = UserRepositoryMock()
        user = user_repo.users_list[0]
        refresh_token = "aaa.bbb.ccc"

        session_repo.sessions = [
            Session(refresh_token="outro.token.aqui", user_id=user.user_id)
        ]
        usecase = RefreshUsecase(session_repo=session_repo, user_repo=user_repo)

        with patch(
            "src.modules.refresh.app.refresh_usecase._verify_kms_jwt",
            return_value={
                "user_id": user.user_id,
                "typ": "refresh",
            },
        ):
            with pytest.raises(ForbiddenAction):
                usecase(refresh_token=refresh_token)

    def test_refresh_usecase_user_not_found(self):
        session_repo = SessionRepositoryMock()
        user_repo = UserRepositoryMock()
        refresh_token = "aaa.bbb.ccc"
        user_id = "00000000-0000-0000-0000-000000000001"

        session_repo.sessions = [
            Session(refresh_token=refresh_token, user_id=user_id)
        ]
        usecase = RefreshUsecase(session_repo=session_repo, user_repo=user_repo)

        with patch(
            "src.modules.refresh.app.refresh_usecase._verify_kms_jwt",
            return_value={
                "user_id": user_id,
                "typ": "refresh",
            },
        ):
            with pytest.raises(NoItemsFound):
                usecase(refresh_token=refresh_token)

    def test_refresh_usecase_happy_path(self):
        session_repo = SessionRepositoryMock()
        user_repo = UserRepositoryMock()
        user = user_repo.users_list[0]
        refresh_token = "aaa.bbb.ccc"

        session_repo.sessions = [
            Session(refresh_token=refresh_token, user_id=user.user_id)
        ]
        usecase = RefreshUsecase(session_repo=session_repo, user_repo=user_repo)

        with patch(
            "src.modules.refresh.app.refresh_usecase._verify_kms_jwt",
            return_value={
                "user_id": user.user_id,
                "typ": "refresh",
            },
        ), patch(
            "src.modules.refresh.app.refresh_usecase._sign_access_token",
            return_value="signed.access.token",
        ) as sign_access_mock, patch(
            "src.modules.refresh.app.refresh_usecase._sign_refresh_token",
            return_value="signed.refresh.token",
        ):
            access_token, new_refresh_token = usecase(refresh_token=refresh_token)

        assert access_token == "signed.access.token"
        assert new_refresh_token == "signed.refresh.token"
        assert session_repo.get_session(user.user_id).refresh_token == "signed.refresh.token"

        sign_access_mock.assert_called_once()
        payload = sign_access_mock.call_args[0][0]
        assert payload["user_id"] == user.user_id
        assert payload["role"] == user.role.value
        assert "exp" in payload
