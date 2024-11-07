from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.entities.user import User
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.modules.update_user.app.update_user_viewmodel import UpdateUserViewModel
class TestUpdateUserViewModel:

    def test_update_user_viewmodel(self):
        user_id = "93bc6ada-c0d1-8754-26ab-e17414c48ae7"
        repo = UserRepositoryMock()

        user = repo.get_user(user_id)

        viewmodel = UpdateUserViewModel(user=user)

        expected = {
            'updated_user': {
                'user_id': user.user_id,
                'role': user.role.value,
                'confirm_user': user.confirm_user,
            },
            'message': 'User information was updated successfully.'
        }

        assert viewmodel.to_dict() == expected
