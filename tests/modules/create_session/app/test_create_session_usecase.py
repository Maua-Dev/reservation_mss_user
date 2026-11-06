import pytest

from src.modules.create_session.app.create_session_usecase import CreateSessionUsecase
from src.shared.domain.entities.session import Session
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.infra.repositories.session_repository_mock import SessionRepositoryMock


class TestCreateSessionUsecase:

    def test_create_session_usecase(self):
        repo = SessionRepositoryMock()
        usecase = CreateSessionUsecase(repo)

        session = usecase(user_id="00000000-0000-0000-0000-000000000003", refresh_token="novo_token")

        created = repo.sessions[-1]

        assert isinstance(session, Session)
        assert created.user_id == "00000000-0000-0000-0000-000000000003"
        assert created.refresh_token == "novo_token"
        assert len(repo.sessions) == 3

    def test_create_session_usecase_duplicated(self):
        repo = SessionRepositoryMock()
        usecase = CreateSessionUsecase(repo)

        with pytest.raises(DuplicatedItem):
            usecase(user_id="00000000-0000-0000-0000-000000000001", refresh_token="novo_token")

    def test_create_session_usecase_invalid_refresh_token(self):
        repo = SessionRepositoryMock()
        usecase = CreateSessionUsecase(repo)

        with pytest.raises(EntityError):
            usecase(user_id="00000000-0000-0000-0000-000000000003", refresh_token=1)

    def test_create_session_usecase_invalid_user_id(self):
        repo = SessionRepositoryMock()
        usecase = CreateSessionUsecase(repo)

        with pytest.raises(EntityError):
            usecase(user_id="not-a-uuid", refresh_token="novo_token")