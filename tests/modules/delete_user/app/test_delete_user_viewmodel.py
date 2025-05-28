from src.modules.delete_user.app.delete_user_viewmodel import DeleteUserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE


class TestDeleteUserViewmodel:

    def test_delete_user_viewmodel_professor(self):
        user = User(
            user_id="93ee6ada-c0d1-7054-66ab-e17414c48ae3",
            name="Rodrigo",
            email="rodrigo.morales@maua.br",
            ra=None,
            role=ROLE.PROFESSOR,
            confirm_user=True
        )

        user_viewmodel = DeleteUserViewmodel(user=user).to_dict()

        expected = {
            "user": {
                "user_id": "93ee6ada-c0d1-7054-66ab-e17414c48ae3",
                "name": "Rodrigo",
                "email": "rodrigo.morales@maua.br",
                "ra": None,
                "role": 'PROFESSOR',
                "confirm_user": True
            },
            'message': 'the user was deleted successfully'
        }
        
        assert user_viewmodel == expected

    def test_delete_user_viewmodel_student(self):
        user = User(
            user_id="93ee6ada-c0d1-7054-66ab-e17414c48ae3",
            name="Rodrigo",
            email="23.00847-4@maua.br",
            ra='23.00847-4',
            role=ROLE.STUDENT,
            confirm_user=True
        )

        user_viewmodel = DeleteUserViewmodel(user=user).to_dict()

        expected = {
            "user": {
                "user_id": "93ee6ada-c0d1-7054-66ab-e17414c48ae3",
                "name": "Rodrigo",
                "email": "23.00847-4@maua.br",
                "ra": '23.00847-4',
                "role": 'STUDENT',
                "confirm_user": True
            },
            'message': 'the user was deleted successfully'
        }

        assert user_viewmodel == expected