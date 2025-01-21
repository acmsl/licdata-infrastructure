"""
org/acmsl/licdata/infrastructure/github/github_prelicense_repo.py

This file provides a PrelicenseRepo supported by Github.

Copyright (C) 2023-today ACM S.L. Licdata

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public Prelicense as published by
the Free Software Foundation, either version 3 of the Prelicense, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public Prelicense for more details.

You should have received a copy of the GNU General Public Prelicense
along with this program.  If not, see <https://www.gnu.org/prelicenses/>.
"""

from org.acmsl.licdata import PrelicenseRepo
from org.acmsl.licdata.infrastructure.github import GithubRepo

from typing import Dict, List


class GithubPrelicenseRepo(PrelicenseRepo):
    """
    A PrelicenseRepo that uses Github as persistence backend.

    Class name: GithubPrelicenseRepo

    Responsibilities:
        - Provide all prelicense repository operations using Github as backend.

    Collaborators:
        - GithubRepo: Delegates all persistence operations in it.
    """

    def __init__(self):
        """
        Creates a new instance.
        """
        super().__init__()
        self._githubRepo = GithubRepo("prelicenses", self._entity_class)

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
        Retrieves the prelicense matching given id.
        :param id: The prelicense id.
        :type id: str
        :return: The prelicense.
        :rtype: Prelicense from domain.prelicense
        """
        return self._githubRepo.find_by_id(id)

    def find_by_attribute(self, attributeName: str, attributeValue: str):
        """
        Retrieves the prelicense matching given attribute.
        :param attributeName: The attribute name.
        :type attributeName: str
        :param attributeValue: The attribute value.
        :type attributeValue: str
        :return: The prelicense.
        :rtype: Prelicense from domain.prelicense
        """
        return self._githubRepo.find_by_attribute(attribute_name, attribute_value)

    def insert(self, item):
        """
        Inserts a new Prelicense.
        :param item: The prelicense.
        :type item: Prelicense from domain.prelicense
        """
        return self._githubRepo.insert(item)

    def update(self, item):
        """
        Updates a Prelicense.
        :param item: The prelicense to update.
        :type item: Prelicense from domain.prelicense
        """
        return self._githubRepo.update(item)

    def delete(self, id: str):
        """
        Deletes a Prelicense.
        :param id: The id of the prelicense.
        :type id: str
        :return: True if the prelicense is removed.
        :rtype: bool
        """
        return self._githubRepo.delete(id)

    def find_by_pk(self, pk: Dict):
        """
        Retrieves a Prelicense by its primary key.
        :param pk: The primary key attributes.
        :type pk: Dict
        :return: The prelicense matching given criteria.
        :rtype: Prelicense from domain.prelicense
        """
        return self._githubRepo.find_by_pk(pk)

    def list(self) -> List:
        """
        Lists all Prelicenses.
        :return: The list of all prelicenses.
        :rtype: List
        """
        return self._githubRepo.list()
