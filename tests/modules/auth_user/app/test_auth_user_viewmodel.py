from src.modules.auth_user.app.auth_user_viewmodel import AuthUserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE


class TestAuthUserViewmodel:

    def test_auth_user_viewmodel_professor(self):
        user = User(
            user_id="93ee6ada-c0d1-7054-66ab-e17414c48ae3",
            name="Rodrigo",
            email="rodrigo.morales@maua.br",
            ra=None,
            role=ROLE.PROFESSOR,
            confirm_user=True
        )

        user_viewmodel = AuthUserViewmodel(user=user, created=False).to_dict()

        expected = {
            "user": {
                "user_id": "93ee6ada-c0d1-7054-66ab-e17414c48ae3",
                "name": "Rodrigo",
                "email": "rodrigo.morales@maua.br",
                "ra": None,
                "role": 'PROFESSOR',
                "confirm_user": True
            },
            'created': False,
            'message': 'the user was authenticated successfully'
        }

        assert user_viewmodel == expected

    def test_auth_user_viewmodel_student(self):
        user = User(
            user_id="93ee6ada-c0d1-7054-66ab-e17414c48ae3",
            name="Rodrigo",
            email="23.00847-4@maua.br",
            ra='23.00847-4',
            role=ROLE.STUDENT,
            confirm_user=True
        )

        user_viewmodel = AuthUserViewmodel(user=user, created=True).to_dict()

        expected = {
            "user": {
                "user_id": "93ee6ada-c0d1-7054-66ab-e17414c48ae3",
                "name": "Rodrigo",
                "email": "23.00847-4@maua.br",
                "ra": '23.00847-4',
                "role": 'STUDENT',
                "confirm_user": True
            },
            'created': True,
            'message': 'the user was created successfully'
        }

        assert user_viewmodel == expected
