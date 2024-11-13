from abc import ABC, abstractmethod
from typing import Optional, List

from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.environments import Environments
from src.shared.infra.dto.user_dynamo_dto import UserDynamoDTO
from src.shared.infra.external.dynamo.datasources.dynamo_datasource import DynamoDatasource


class UserRepositoryDynamo(IUserRepository, ABC):

    @staticmethod
    def partition_key_format():
        return "user"

    @staticmethod
    def sort_key_format(user_id: str) -> str:
        return f"{user_id}"

    def __init__(self):
        self.dynamo = DynamoDatasource(endpoint_url=Environments.get_envs().endpoint_url,
                                       dynamo_table_name=Environments.get_envs().dynamo_table_name,
                                       region=Environments.get_envs().region,
                                       partition_key=Environments.get_envs().dynamo_partition_key,
                                       sort_key=Environments.get_envs().dynamo_sort_key
                                       )

    def get_all_users(self) -> List[User]:

        all_users = []
        all_items = self.dynamo.get_all_items().get('Items')

        for item in all_items:
            all_users.append(UserDynamoDTO.from_dynamo(item).to_entity())

        return all_users

    def create_user(self, new_user: User) -> User:

        user_dto = UserDynamoDTO.from_entity(user=new_user)
        item = user_dto.to_dynamo()

        resp = self.dynamo.put_item(
            partition_key=self.partition_key_format(),
            sort_key=self.sort_key_format(user_id=new_user.user_id),
            item=item,
            is_decimal=True
        )

        return new_user

    def get_user(self, user_id: str) -> Optional[User]:
        user_data = self.dynamo.get_item(
            partition_key=self.partition_key_format(),
            sort_key=self.sort_key_format(user_id=user_id)
        )

        if 'Item' not in user_data:
            return None

        user = UserDynamoDTO.from_dynamo(user_data.get("Item")).to_entity()

        return user

    def update_user(self,
                    user_id: str,
                    new_confirm_user: Optional[bool] = None,  #Default pra False
                    new_role: Optional[ROLE] = None) -> Optional[User]:  #Default pra student

        user_to_update = self.get_user(user_id=user_id)

        if user_to_update is None:
            return None

        new_confirm_user = user_to_update.confirm_user if new_confirm_user is None else new_confirm_user

        new_role = user_to_update.role if new_role is None else new_role

        response = self.dynamo.update_item(
            partition_key=self.partition_key_format(),
            sort_key=self.sort_key_format(user_id=user_id),
            update_dict={"confirm_user": new_confirm_user, "role": new_role.value})

        if "Attributes" not in response:
            return None

        return UserDynamoDTO.from_dynamo(response["Attributes"]).to_entity()

    def delete_user(self, user_id: str) -> Optional[User]:
        deleted_user = self.dynamo.delete_item(
            partition_key=self.partition_key_format(),
            sort_key=self.sort_key_format(user_id=user_id)
        )

        if 'Attributes' not in deleted_user:
            return None

        return UserDynamoDTO.from_dynamo(deleted_user["Attributes"]).to_entity()
