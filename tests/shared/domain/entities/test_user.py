import pytest

from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.domain_errors import EntityError

class TestCourt:

    def test_user(self):
        userEntity = User(
            name='Leonardo Luiz Seixas Iorio',
            email='50.00800-0@maua.br',
            user_id='1',
            ra='55.00800-0',
            role=ROLE.STUDENT,
            confirm_user=True
        )

        assert userEntity.name == 'Leonardo Luiz Seixas Iorio'
        assert userEntity.email == '50.00800-0@maua.br'
        assert userEntity.user_id == '1'
        assert userEntity.ra == '55.00800-0'
        assert userEntity.role == ROLE.STUDENT
        assert userEntity.confirm_user == True

    def test_invalid_name(self):
        with pytest.raises(EntityError):
            User(
                name=1337,
                email='50.00800-0@gmail.com',
                user_id='1',
                ra='55.00800-0',
                role=ROLE.STUDENT,
                confirm_user=True
            )

    def test_missing_name(self):
        with pytest.raises(TypeError):
            User(
                email='50.00800-0@gmail.com',
                user_id='1',
                ra='55.00800-0',
                role=ROLE.STUDENT,
                confirm_user=True
            )

    def test_invalid_email_format(self):
        with pytest.raises(EntityError):
            User(
                name='Leonardo Luiz Seixas Iorio',
                email='50.00800-0@maua.b',
                user_id='1',
                ra='55.00800-0',
                role=ROLE.STUDENT,
                confirm_user=True
            )

    def test_invalid_email_type(self):
        with pytest.raises(EntityError):
            User(
                name='Leonardo Luiz Seixas Iorio',
                email=1337,
                user_id='1',
                ra='55.00800-0',
                role=ROLE.STUDENT,
                confirm_user=True
            )

    def test_missing_email(self):
        with pytest.raises(TypeError):
            User(
                name='Leonardo Luiz Seixas Iorio',
                user_id='1',
                ra='55.00800-0',
                role=ROLE.STUDENT,
                confirm_user=True
            )

    def test_invalid_user_id(self):
        with pytest.raises(EntityError):
            User(
                name='Leonardo Luiz Seixas Iorio',
                email='50.00800-0',
                user_id=1,
                ra='55.00800-0',
                role=ROLE.STUDENT,
                confirm_user=True
            )

    def test_missing_user_id(self):
        with pytest.raises(TypeError):
            User(
                name='Leonardo Luiz Seixas Iorio',
                email='50.00800-0',
                ra='55.00800-0',
                role=ROLE.STUDENT,
                confirm_user=True
            )

    def test_invalid_ra_format(self):
        with pytest.raises(EntityError):
            User(
                name='Leonardo Luiz Seixas Iorio',
                email='50.00800-0@maua.br',
                user_id='1',
                ra='55.008000',
                role=ROLE.STUDENT,
                confirm_user=True
            )

    def test_missing_ra(self):
        with pytest.raises(TypeError):
            User(
                name='Leonardo Luiz Seixas Iorio',
                email='50.00800-0@maua.br',
                user_id='1',
                role=ROLE.STUDENT,
                confirm_user=True
            )

    def test_invalid_ra_type(self):
        with pytest.raises(EntityError):
            User(
                name='Leonardo Luiz Seixas Iorio',
                email='50.00800-0@maua.br',
                user_id='1',
                ra=55008000,
                role=ROLE.STUDENT,
                confirm_user=True
            )

    def test_invalid_role(self):
        with pytest.raises(EntityError):
            User(
                name='Leonardo Luiz Seixas Iorio',
                email='50.00800-0@maua.br',
                user_id='1',
                ra='55.00800-0',
                role='admin',
                confirm_user=True
            )

    def test_missing_role(self):
        with pytest.raises(TypeError):
            User(
                name='Leonardo Luiz Seixas Iorio',
                email='50.00800-0@maua.br',
                user_id='1',
                ra='55.00800-0',
                confirm_user=True
            )

    def test_invalid_confirm_user(self):
        with pytest.raises(EntityError):
            User(
                name='Leonardo Luiz Seixas Iorio',
                email='50.00800-0@maua.br',
                user_id='1',
                ra='55.00800-0',
                role=ROLE.STUDENT,
                confirm_user='false'
            )

    def test_missing_confirm_user(self):
        with pytest.raises(TypeError):
            User(
                name='Leonardo Luiz Seixas Iorio',
                email='50.00800-0@maua.br',
                user_id='1',
                ra='55.00800-0',
                role=ROLE.STUDENT
            )

