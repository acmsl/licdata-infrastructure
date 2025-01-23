"""
org/acmsl/licdata/infrastructure/github/github_repo.py

This file defines an abstract class to simplify implementing repositories using Github underneath.

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

from org.acmsl.licdata.infrastructure.github import github_adapter
from pythoneda.shared import BaseObject
from typing import Dict, List, Type


class GithubRepo(BaseObject):
    """
    Abstract class to simplify implementing repositories using Github underneath.

    Class name: GithubRepo

    Responsibilities:
        - Provide the common logic for all github-based repositories.

    Collaborators:
        - GithubAdapter from infrastructure.github.github_adapter: To simplify the use of the Github API.

    """

    def __init__(self, path: str, entityClass: Type):
        """
        Creates a new instance.
        :param path: The path.
        :type path: str
        :param entityClass: The class of the entity associated to this repo.
        :type entityClass: Type
        """
        super().__init__()
        self._path = path
        self._primary_key = entityClass.primary_key()
        self._filter_attributes = entityClass.filter_attributes()
        self._attributes = entityClass.attributes()
        self._sensitive_attributes = entityClass.sensitive_attributes()

    def __str__(self):
        """
        Provides a text representation of this instance.
        """
        return f"{ 'path': '{self._path}', 'primary_key': '{self._primary_key}', 'filter_attributes': '{self._filter_attributes}', 'attributes': '{self._attributes}', 'encrypted_attributes': '{self._encripted_attributes}'}"

    @property
    def path(self):
        """
        Retrieves the relative path in the Github repository.
        """
        return self._path

    @property
    def primary_key(self) -> List:
        """
        Retrieves the attributes participating in the primary key.
        :return: The names of the attributes in the primary key.
        :rtype: List
        """
        return self._primary_key

    @property
    def filter_attributes(self) -> List:
        """
        Retrieves the attributes used to filter.
        :return: The names of the attributes used to filter.
        :rtype: List
        """
        return self._filter_attributes

    @property
    def attributes(self) -> List:
        """
        Retrieves all attributes of the entity.
        :return: The names of the attributes.
        :rtype: List
        """
        return self._attributes

    @property
    def sensitive_attributes(self) -> List:
        """
        Retrieves the sensitive attributes.
        :return: The names of the attributes to encrypt.
        :rtype: List
        """
        return self._sensitive_attributes

    def find_by_id(self, id: str):
        """
        Finds the item matching given id.
        :param id: The id.
        :type id: str
        :return: The specific entity.
        :rtype: object
        """
        return github_adapter.find_by_id(id, self._path)

    def find_by_attribute(self, attributeName: str, attributeValue: str):
        """
        Finds items matching a given attribute.
        :param attributeName: The name of the attribute.
        :type attributeName: str
        :param attributeValue: The name of the attribute.
        :type attributeValue: str
        :return: A tuple with the matching items and the hash.
        :rtype: tuple
        """
        return github_adapter.find_by_attribute(
            attributeValue, attributeName, self._path
        )

    def find_by_attributes(self, filter: Dict):
        """
        Finds items matching given attribute filter.
        :param filter: A dictionary of attribute names and values used to filter.
        :type filte: Dict
        :return: A tuple with the matching items and the hash.
        :rtype: tuple
        """
        return github_adapter.find_by_attributes(filter, self._path)

    def insert(self, item) -> bool:
        """
        Inserts a new item.
        :param item: The item to persist.
        :type item: object
        :return: True if the item gets persisted.
        :rtype: bool
        """
        return github_adapter.insert(
            item,
            self._path,
            self._primary_key,
            self._filter_attributes,
            self._attributes,
            self._encrypted_attributes,
        )

    def update(self, item) -> bool:
        """
        Updates an item.
        :param item: The item to update.
        :type item: object
        :return: True if the item gets updated.
        :rtype: bool
        """
        return github_adapter.update(
            item,
            self._path,
            self._primary_key,
            self._filter_attributes,
            self._attributes,
            self._encrypted_attributes,
        )

    def delete(self, id: str) -> bool:
        """
        Deletes an item.
        :param id: The id of the item to delete.
        :type id: str
        :return: True if the item gets deleted.
        :rtype: bool
        """
        return github_adapter.delete(id, self._path)

    def find_by_pk(self, pk: Dict):
        """
        Finds the item matching given primary key.
        :param pk: The primary key.
        :type pk: Dict
        :return: The item.
        :rtype: object
        """
        return github_adapter.find_by_attributes(pk, self._path)

    def list(self) -> List:
        """
        Retrieves all items.
        :return: The list of items.
        :rtype: List
        """
        return github_adapter.list(self._path)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
