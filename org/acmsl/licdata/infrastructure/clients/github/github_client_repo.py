"""
org/acmsl/licdata/infrastructure/clients/github/github_client_repo.py

This file provides a ClientRepo supported by Github.

Copyright (C) 2023-today ACM S.L. Licdata-Domain

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from org.acmsl.licdata import Client, ClientRepo
from org.acmsl.licdata.infrastructure.github import GithubRepo

from typing import Dict, List


class GithubClientRepo(ClientRepo):
    """
    A ClientRepo that uses Github as persistence backend.

    Class name: GithubClientRepo

    Responsibilities:
        - Provide all client repository operations using Github as backend.

    Collaborators:
        - GithubRepo: Delegates all persistence operations in it.
    """

    def __init__(self):
        """
        Creates a new instance.
        """
        super().__init__()
        self._githubRepo = GithubRepo("clients", self._entity_class)

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
        Retrieves the client matching given id.
        :param id: The client id.
        :type id: str
        :return: The client.
        :rtype: Client from domain.client
        """
        return self._githubRepo.find_by_id(id)

    def find_by_attribute(self, attributeName: str, attributeValue: str):
        """
        Retrieves the client matching given attribute.
        :param attributeName: The attribute name.
        :type attributeName: str
        :param attributeValue: The attribute value.
        :type attributeValue: str
        :return: The client.
        :rtype: Client from domain.client
        """
        return self._githubRepo.find_by_attribute(attribute_name, attribute_value)

    def filter(self, dictionary: Dict) -> List[Client]:
        """
        Retrieves the entities matching given criteria.
        :param dictionary: The filter.
        :type dictionary: Dict
        :return: The instances of the EntityClass matching given criteria, or an empty list if none found.
        :rtype: List[pythoneda.Entity]
        """
        return self._githubRepo.filter(dictionary)

    def insert(self, item):
        """
        Inserts a new Client.
        :param item: The client.
        :type item: Client from domain.client
        """
        return self._githubRepo.insert(item)

    def update(self, item):
        """
        Updates a Client.
        :param item: The client to update.
        :type item: Client from domain.client
        """
        return self._githubRepo.update(item)

    def delete(self, id: str):
        """
        Deletes a Client.
        :param id: The id of the client.
        :type id: str
        :return: True if the client is removed.
        :rtype: bool
        """
        return self._githubRepo.delete(id)

    def find_by_pk(self, pk: Dict):
        """
        Retrieves a Client by its primary key.
        :param pk: The primary key attributes.
        :type pk: Dict
        :return: The client matching given criteria.
        :rtype: Client from domain.client
        """
        return self._githubRepo.find_by_pk(pk)

    def list(self) -> List:
        """
        Lists all Clients.
        :return: The list of all clients.
        :rtype: List
        """
        return self._githubRepo.list()
