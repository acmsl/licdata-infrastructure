"""
org/acmsl/licdata/infrastructure/github/github_license_repo.py

This file provides a LicenseRepo supported by Github.

Copyright (C) 2023-today ACM S.L. Licdata

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

from org.acmsl.licdata.domain import LicenseRepo
from org.acmsl.licdata.infrastructure.github import GithubRepo

from typing import Dict, List


class GithubLicenseRepo(LicenseRepo):
    """
    A LicenseRepo that uses Github as persistence backend.

    Class name: GithubLicenseRepo

    Responsibilities:
        - Provide all license repository operations using Github as backend.

    Collaborators:
        - GithubRepo: Delegates all persistence operations in it.
    """

    def __init__(self):
        """
        Creates a new instance.
        """
        super().__init__()
        self._githubRepo = GithubRepo("licenses", self._entity_class)

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
        Retrieves the license matching given id.
        :param id: The license id.
        :type id: str
        :return: The license.
        :rtype: License from domain.license
        """
        return self._githubRepo.find_by_id(id)

    def find_by_attribute(self, attributeName: str, attributeValue: str):
        """
        Retrieves the license matching given attribute.
        :param attributeName: The attribute name.
        :type attributeName: str
        :param attributeValue: The attribute value.
        :type attributeValue: str
        :return: The license.
        :rtype: License from domain.license
        """
        return self._githubRepo.find_by_attribute(attribute_name, attribute_value)

    def insert(self, item):
        """
        Inserts a new License.
        :param item: The license.
        :type item: License from domain.license
        """
        return self._githubRepo.insert(item)

    def update(self, item):
        """
        Updates a License.
        :param item: The license to update.
        :type item: License from domain.license
        """
        return self._githubRepo.update(item)

    def delete(self, id: str):
        """
        Deletes a License.
        :param id: The id of the license.
        :type id: str
        :return: True if the license is removed.
        :rtype: bool
        """
        return self._githubRepo.delete(id)

    def find_by_pk(self, pk: Dict):
        """
        Retrieves a License by its primary key.
        :param pk: The primary key attributes.
        :type pk: Dict
        :return: The license matching given criteria.
        :rtype: License from domain.license
        """
        return self._githubRepo.find_by_pk(pk)

    def list(self) -> List:
        """
        Lists all Licenses.
        :return: The list of all licenses.
        :rtype: List
        """
        return self._githubRepo.list()
