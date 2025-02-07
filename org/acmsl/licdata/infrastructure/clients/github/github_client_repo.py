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
from org.acmsl.licdata.events.clients import (
    DeleteClientRequested,
    ClientDeleted,
    InvalidDeleteClientRequest,
    NewClientCreated,
    NewClientRequested,
)
from org.acmsl.licdata.infrastructure.github import GithubRepo

from typing import Dict, List, Optional, Tuple


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
        self._github_repo = GithubRepo("clients", self._entity_class)

    @property
    def path(self):
        """
        Retrieves the Github path.
        :return: The path.
        :rtype: str
        """
        return self._github_repo.path

    def find_by_id(self, id: str):
        """
        Retrieves the client matching given id.
        :param id: The client id.
        :type id: str
        :return: The client.
        :rtype: Client from domain.client
        """
        return self._github_repo.find_by_id(id, buildEntity=self.build_entity_from_dict)

    def build_entity_from_dict(self, dict: Dict) -> Client:
        """
        Builds a Client from a dictionary.
        :param dict: The dictionary.
        :type dict: Dict
        :return: The Client instance.
        :rtype: org.acmsl.licdata.Client
        """
        return Client.from_dict(dict)

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
        return self._github_repo.find_by_attribute(attribute_name, attribute_value)

    def filter(self, dictionary: Dict) -> List[Client]:
        """
        Retrieves the entities matching given criteria.
        :param dictionary: The filter.
        :type dictionary: Dict
        :return: The instances of the EntityClass matching given criteria, or an empty list if none found.
        :rtype: List[pythoneda.Entity]
        """
        return self._github_repo.filter(dictionary)

    def insert(self, newClientRequested: NewClientRequested) -> NewClientCreated:
        """
        Inserts a new Client.
        :param newClientRequested: The event.
        :type newClientRequested: org.acmsl.licdata.events.clients.NewClientRequested
        """
        return self._github_repo.insert(newClientRequested, self._build_new_client)

    def _build_new_client(
        self, newClientRequested: NewClientRequested
    ) -> Tuple[Client, NewClientCreated]:
        """
        Builds a new Client.
        :param newClientRequested: The event.
        :type newClientRequested: org.acmsl.licdata.events.clients.NewClientRequested
        :return: The new client and the event.
        :rtype: Tuple[org.acmsl.licdata.Client, org.acmsl.licdata.events.clients.NewClientCreated]
        """
        new_client = Client.create_from(newClientRequested)
        return (new_client, new_client.created_event)

    def update(self, item):
        """
        Updates a Client.
        :param item: The client to update.
        :type item: Client from domain.client
        """
        return self._github_repo.update(item)

    def delete(
        self,
        deleteClientRequested: DeleteClientRequested,
    ) -> ClientDeleted:
        """
        Deletes a Client.
        :param deleteClientRequested: The event requesting the removal of the client.
        :type deleteClientRequested: org.acmsl.licdata.events.clients.DeleteClientRequested
        :return: The entity-deleted event if the client gets removed.
        :rtype: org.acmsl.licdata.events.clients.ClientDeleted
        """
        return self._github_repo.delete(
            deleteEntityRequested=deleteClientRequested,
            buildEntity=self.build_entity_from_dict,
            buildInvalidDeleteEntityRequestEvent=self.build_invalid_delete_entity_request_event,
        )

    def _create_client_deleted_event(
        self, deleteClientRequested: DeleteClientRequested
    ) -> ClientDeleted:
        """
        Creates a new ClientDeleted event.
        :param deleteClientRequested: The event requesting the removal of the client.
        :type deleteClientRequested: org.acmsl.licdata.events.clients.DeleteClientRequested
        :param clientData: The client data.
        :type clientData
        :return: The event.
        :rtype: org.acmsl.licdata.events.clients.ClientDeleted
        """
        client = self.find_by_id(deleteClientRequested)
        return client.delete()

    def build_invalid_delete_entity_request_event(
        self, deleteClientRequested: DeleteClientRequested
    ) -> InvalidDeleteClientRequest:
        """
        Builds an InvalidDeleteClientRequest event.
        :param deleteClientRequested: The event requesting the removal of the client.
        :type deleteClientRequested: org.acmsl.licdata.events.clients.DeleteClientRequested
        :return: The event.
        :rtype: org.acmsl.licdata.events.clients.InvalidDeleteClientRequest
        """
        return InvalidDeleteClientRequest(
            deleteClientRequested.entity_id,
            deleteClientRequested.previous_event_ids + [deleteClientRequested.id],
        )

    def find_by_pk(self, pk: Dict) -> Optional[Client]:
        """
        Retrieves a Client by its primary key.
        :param pk: The primary key attributes.
        :type pk: Dict
        :return: The client matching given criteria.
        :rtype: Optional[org.acmsl.licdata.Client]
        """
        result = None

        match = self._github_repo.find_by_pk(pk)

        if match is not None:
            result = Client.from_dict(match)

        return result

    def list(self) -> List:
        """
        Lists all Clients.
        :return: The list of all clients.
        :rtype: List
        """
        return self._github_repo.list()
