"""
org/acmsl/licdata/infrastructure/incidents/github/github_incident_repo.py

This file provides a IncidentRepo supported by Github.

Copyright (C) 2023-today ACM S.L. Licdata-Infrastructure

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

from org.acmsl.licdata import IncidentRepo
from org.acmsl.licdata.infrastructure.github import GithubRepo

from typing import Dict, List


class GithubIncidentRepo(IncidentRepo):
    """
    A IncidentRepo that uses Github as persistence backend.

    Class name: GithubIncidentRepo

    Responsibilities:
        - Provide all incident repository operations using Github as backend.

    Collaborators:
        - GithubRepo: Delegates all persistence operations in it.
    """

    def __init__(self):
        """
        Creates a new instance.
        """
        super().__init__()
        self._githubRepo = GithubRepo("incidents", self._entity_class)

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
        Retrieves the incident matching given id.
        :param id: The incident id.
        :type id: str
        :return: The incident.
        :rtype: Incident from domain.incident
        """
        return self._githubRepo.find_by_id(id)

    def find_by_attribute(self, attributeName: str, attributeValue: str):
        """
        Retrieves the incident matching given attribute.
        :param attributeName: The attribute name.
        :type attributeName: str
        :param attributeValue: The attribute value.
        :type attributeValue: str
        :return: The incident.
        :rtype: Incident from domain.incident
        """
        return self._githubRepo.find_by_attribute(attribute_name, attribute_value)

    def insert(self, item):
        """
        Inserts a new Incident.
        :param item: The incident.
        :type item: Incident from domain.incident
        """
        return self._githubRepo.insert(item)

    def update(self, item):
        """
        Updates an Incident.
        :param item: The incident to update.
        :type item: Incident from domain.incident
        """
        return self._githubRepo.update(item)

    def delete(self, id: str):
        """
        Deletes an Incident.
        :param id: The id of the incident.
        :type id: str
        :return: True if the incident is removed.
        :rtype: bool
        """
        return self._githubRepo.delete(id)

    def find_by_pk(self, pk: Dict):
        """
        Retrieves an Incident by its primary key.
        :param pk: The primary key attributes.
        :type pk: Dict
        :return: The incident matching given criteria.
        :rtype: Incident from domain.incident
        """
        return self._githubRepo.find_by_pk(pk)

    def list(self) -> List:
        """
        Lists all Incidents.
        :return: The list of all incidents.
        :rtype: List
        """
        return self._githubRepo.list()
