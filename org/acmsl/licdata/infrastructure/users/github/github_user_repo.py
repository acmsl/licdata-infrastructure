"""
org/acmsl/licdata/infrastructure/github/github_user_repo.py

This file provides a UserRepo supported by Github.

Copyright (C) 2023-today ACM S.L. Licdata

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public User as published by
the Free Software Foundation, either version 3 of the User, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public User for more details.

You should have received a copy of the GNU General Public User
along with this program.  If not, see <https://www.gnu.org/users/>.
"""

from org.acmsl.licdata import UserRepo
from org.acmsl.licdata.infrastructure.github import GithubRepo

from typing import Dict, List


class GithubUserRepo(UserRepo):
    """
    A UserRepo that uses Github as persistence backend.

    Class name: GithubUserRepo

    Responsibilities:
        - Provide all user repository operations using Github as backend.

    Collaborators:
        - GithubRepo: Delegates all persistence operations in it.
    """

    def __init__(self):
        """
        Creates a new instance.
        """
        super().__init__()
        self._githubRepo = GithubRepo("users", self._entity_class)

    @property
    def path(self):
        """
        Retrieves the Github path.
        :return: The path.
        :rtype: str
        """
        return self._githubRepo.path

    def find_by_id(self, id: str):
        """
        Retrieves the user matching given id.
        :param id: The user id.
        :type id: str
        :return: The user.
        :rtype: User from domain.user
        """
        return self._githubRepo.find_by_id(id)

    def find_by_attribute(self, attributeName: str, attributeValue: str):
        """
        Retrieves the user matching given attribute.
        :param attributeName: The attribute name.
        :type attributeName: str
        :param attributeValue: The attribute value.
        :type attributeValue: str
        :return: The user.
        :rtype: User from domain.user
        """
        return self._githubRepo.find_by_attribute(attribute_name, attribute_value)

    def insert(self, item):
        """
        Inserts a new User.
        :param item: The user.
        :type item: User from domain.user
        """
        return self._githubRepo.insert(item)

    def update(self, item):
        """
        Updates an User.
        :param item: The user to update.
        :type item: User from domain.user
        """
        return self._githubRepo.update(item)

    def delete(self, id: str):
        """
        Deletes an User.
        :param id: The id of the user.
        :type id: str
        :return: True if the user is removed.
        :rtype: bool
        """
        return self._githubRepo.delete(id)

    def find_by_pk(self, pk: Dict):
        """
        Retrieves an User by its primary key.
        :param pk: The primary key attributes.
        :type pk: Dict
        :return: The user matching given criteria.
        :rtype: User from domain.user
        """
        return self._githubRepo.find_by_pk(pk)

    def list(self) -> List:
        """
        Lists all Users.
        :return: The list of all users.
        :rtype: List
        """
        return self._githubRepo.list()
