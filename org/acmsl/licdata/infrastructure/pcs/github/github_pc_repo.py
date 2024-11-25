"""
org/acmsl/licdata/infrastructure/github/github_pc_repo.py

This file provides a PcRepo supported by Github.

Copyright (C) 2023-today ACM S.L. Licdata

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public Pc as published by
the Free Software Foundation, either version 3 of the Pc, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public Pc for more details.

You should have received a copy of the GNU General Public Pc
along with this program.  If not, see <https://www.gnu.org/pcs/>.
"""

from org.acmsl.licdata.domain import PcRepo
from org.acmsl.licdata.infrastructure.github import GithubRepo

from typing import Dict, List


class GithubPcRepo(PcRepo):
    """
    A PcRepo that uses Github as persistence backend.

    Class name: GithubPcRepo

    Responsibilities:
        - Provide all pc repository operations using Github as backend.

    Collaborators:
        - GithubRepo: Delegates all persistence operations in it.
    """

    def __init__(self):
        """
        Creates a new instance.
        """
        super().__init__()
        self._githubRepo = GithubRepo("pcs", self._entity_class)

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
        Retrieves the pc matching given id.
        :param id: The pc id.
        :type id: str
        :return: The pc.
        :rtype: Pc from domain.pc
        """
        return self._githubRepo.find_by_id(id)

    def find_by_attribute(self, attributeName: str, attributeValue: str):
        """
        Retrieves the pc matching given attribute.
        :param attributeName: The attribute name.
        :type attributeName: str
        :param attributeValue: The attribute value.
        :type attributeValue: str
        :return: The pc.
        :rtype: Pc from domain.pc
        """
        return self._githubRepo.find_by_attribute(attribute_name, attribute_value)

    def insert(self, item):
        """
        Inserts a new Pc.
        :param item: The pc.
        :type item: Pc from domain.pc
        """
        return self._githubRepo.insert(item)

    def update(self, item):
        """
        Updates a Pc.
        :param item: The pc to update.
        :type item: Pc from domain.pc
        """
        return self._githubRepo.update(item)

    def delete(self, id: str):
        """
        Deletes a Pc.
        :param id: The id of the pc.
        :type id: str
        :return: True if the pc is removed.
        :rtype: bool
        """
        return self._githubRepo.delete(id)

    def find_by_pk(self, pk: Dict):
        """
        Retrieves a Pc by its primary key.
        :param pk: The primary key attributes.
        :type pk: Dict
        :return: The pc matching given criteria.
        :rtype: Pc from domain.pc
        """
        return self._githubRepo.find_by_pk(pk)

    def list(self) -> List:
        """
        Lists all Pcs.
        :return: The list of all pcs.
        :rtype: List
        """
        return self._githubRepo.list()
