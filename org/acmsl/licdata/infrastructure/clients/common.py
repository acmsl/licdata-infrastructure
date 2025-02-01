"""
org/acmsl/licdata/infrastructure/clients/common.py

This file provides some methods used by client-related handlers.

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

from org.acmsl.licdata import Client
from org.acmsl.licdata.events.infrastructure.http.clients import (
    HttpNewClientCreated,
    HttpInvalidNewClientRequest,
    HttpClientAlreadyExists,
)
import org.acmsl.licdata.infrastructure.rest as rest
from pythoneda.shared import Event
from typing import Dict, List, Type


def retrieve_pk(body: Dict, event) -> List:
    """
    Retrieves the client's primary key from given body/event.
    :param body: The body.
    :type body: Dict
    :param event: The AWS Lambda event.
    :type event: event
    :return: The primary key.
    :rtype: Dict
    """
    return rest.retrieve_attributes_from_params(body, event, Client.primary_key())


def retrieve_attributes(body: Dict, event) -> List:
    """
    Retrieves the client's attributes from given body/event.
    :param body: The body.
    :type body: Dict
    :param event: The AWS Lambda event.
    :type event: event
    :return: The attributes.
    :rtype: Dict
    """
    return rest.retrieve_attributes_from_params(body, event, Client.attributes())


def resource_created_event_class() -> Type[Event]:
    """
    Retrieves the class of the "resource created" event.
    :return: The class.
    :type: Type[Event]
    """
    return HttpNewClientCreated


def invalid_new_resource_request_event_class() -> Type[Event]:
    """
    Retrieves the class of the "invalid creation request" event.
    :return: The class.
    :type: Type[Event]
    """
    return HttpInvalidNewClientRequest


def resource_already_exists_event_class() -> Type[Event]:
    """
    Retrieves the class of the "resource already exists" event.
    :return: The class.
    :type: Type[Event]
    """
    return HttpClientAlreadyExists
