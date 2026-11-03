import uuid

import pytest

from src.shared.domain.entities.session import Session
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, NoItemsFound
from src.shared.infra.repositories.session_repository_mock import SessionRepositoryMock


class TestSessionRepositoryMock:

    def test_create_session(self):
        repo = SessionRepositoryMock()
        session = Session(refresh_token="novo_token", user_id=str(uuid.uuid4()))

        created = repo.create_session(session)

        assert created is session
        assert len(repo.sessions) == 3
        assert repo.sessions[2].refresh_token == "novo_token"

    def test_create_session_duplicated(self):
        repo = SessionRepositoryMock()
        duplicated = Session(
            refresh_token="outro_token",
            user_id=repo.sessions[0].user_id
        )

        with pytest.raises(DuplicatedItem):
            repo.create_session(duplicated)

    def test_get_session(self):
        repo = SessionRepositoryMock()

        session = repo.get_session("00000000-0000-0000-0000-000000000001")

        assert session.refresh_token == "refresh_token_1"

    def test_get_session_not_found(self):
        repo = SessionRepositoryMock()

        with pytest.raises(NoItemsFound):
            repo.get_session(str(uuid.uuid4()))

    def test_update_session(self):
        repo = SessionRepositoryMock()
        updated = Session(
            refresh_token="token_atualizado",
            user_id="00000000-0000-0000-0000-000000000001"
        )

        result = repo.update_session(updated)

        assert result.refresh_token == "token_atualizado"
        assert repo.sessions[0].refresh_token == "token_atualizado"

    def test_update_session_not_found(self):
        repo = SessionRepositoryMock()
        session = Session(refresh_token="token", user_id=str(uuid.uuid4()))

        with pytest.raises(NoItemsFound):
            repo.update_session(session)

    def test_delete_session(self):
        repo = SessionRepositoryMock()

        deleted = repo.delete_session("00000000-0000-0000-0000-000000000001")

        assert deleted.refresh_token == "refresh_token_1"
        assert len(repo.sessions) == 1

    def test_delete_session_not_found(self):
        repo = SessionRepositoryMock()

        with pytest.raises(NoItemsFound):
            repo.delete_session(str(uuid.uuid4()))