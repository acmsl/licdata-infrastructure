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

import inspect
from org.acmsl.licdata.infrastructure.github import github_adapter
from pythoneda.shared import BaseObject, Entity, Event
from typing import Callable, Dict, List, Tuple, Type, Optional


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
        self._entity_class = entityClass
        self._primary_key = entityClass.primary_key()
        self._filter_attributes = entityClass.filter_attributes()
        self._attributes = entityClass.attributes()
        self._sensitive_attributes = entityClass.sensitive_attributes()

    def __str__(self):
        """
        Provides a text representation of this instance.
        """
        primary_key = ", ".join([f'"{attr}"' for attr in self._primary_key])
        filter_attributes = ", ".join(
            [
                f'"{name}"'
                for name, value in inspect.getmembers(
                    self._entity_class,
                    lambda v: v in self._entity_class.filter_attributes()
                    and isinstance(v, property),
                )
            ]
        )
        attributes = ", ".join(
            [
                f'"{name}"'
                for name, value in inspect.getmembers(
                    self._entity_class,
                    lambda v: v in self._entity_class.attributes()
                    and isinstance(v, property),
                )
            ]
        )
        sensitive_attributes = ", ".join(
            [
                f'"{name}"'
                for name, value in inspect.getmembers(
                    self._entity_class,
                    lambda v: v in self._entity_class.sensitive_attributes()
                    and isinstance(v, property),
                )
            ]
        )
        return f"{{ 'path': '{self._path}', 'primary_key': [ {primary_key} ], 'filter_attributes': [ {filter_attributes} ], 'attributes': [ {attributes} ], 'sensitive_attributes': [ {sensitive_attributes} ] }}"

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

    def insert(
        self,
        newEntityRequested: Event,
        buildNewEntity: Callable[[Event], Tuple[Entity, Event]],
    ) -> Event:
        """
        Inserts a new entity.
        :param newEntityRequested: The event.
        :type newEntityRequested: pythoneda.shared.Event
        :param buildNewEntity: A function to create the new-entity-created e.
        :type buildNewEntity: callable[[pythoneda.shared.Entity], pythoneda.shared.Event]
        :return: The new-entity-created event if the entity gets persisted.
        :rtype: pythoneda.shared.Event
        """
        return github_adapter.insert(
            newEntityRequested=newEntityRequested,
            buildNewEntity=buildNewEntity,
            path=self._path,
            primaryKey=self._primary_key,
            filterKeys=self._filter_attributes,
            attributeNames=self._attributes,
            sensitiveAttributes=self._sensitive_attributes,
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
            self._sensitive_attributes,
        )

    def delete(self, id: str) -> object:
        """
        Deletes an item.
        :param id: The id of the item to delete.
        :type id: str
        :return: The deleted item, if the operation succeeds.
        :rtype: object
        """
        return github_adapter.delete(
            id,
            self._path,
            self._attributes,
            self._sensitive_attributes,
        )

    def delete_by_pk(self, primaryKey: List) -> object:
        """
        Deletes an item.
        :param primaryKey: The primary key of the item to delete.
        :type primaryKey: List
        :return: The deleted item, if the operation succeeds.
        :rtype: object
        """
        return github_adapter.delete(
            primaryKey,
            self._path,
            self._primary_key,
            self._attributes,
            self._sensitive_attributes,
        )

    def find_by_pk(self, pk: Dict) -> Optional[object]:
        """
        Finds the item matching given primary key.
        :param pk: The primary key.
        :type pk: Dict
        :return: The item.
        :rtype: Optional[object]
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
