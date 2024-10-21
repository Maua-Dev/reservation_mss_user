import pytest
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.domain_errors import EntityError


class Test_User:

    def test_invalid_name_type(self):
            with pytest.raises(EntityError):
                user = User(name=17, email="24.01460-5@maua.br", role=ROLE.STUDENT, user_id="93bc6ada-c0d1-7054-66ab-e17414c48ae3", ra="24.01460-5", confirm_user = False )