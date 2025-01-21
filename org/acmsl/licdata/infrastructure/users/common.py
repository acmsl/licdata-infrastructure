"""
org/acmsl/licdata/infrastructure/users/common.py

This file provides some methods used by user-related handlers.

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

from org.acmsl.licdata import User
import org.acmsl.licdata.infrastructure.rest

from typing import Dict


def retrieve_pk(body: Dict, event) -> Dict:
    """
    Retrieves the user's primary key from given body/event.
    :param body: The body.
    :type body: Dict
    :param event: The AWS Lambda event.
    :type event: event
    :return: The primary key.
    :rtype: Dict
    """
    return rest.retrieve_attributes_from_params(body, event, User.primary_key())


def retrieve_attributes(body: Dict, event) -> Dict:
    """
    Retrieves the user's attributes from given body/event.
    :param body: The body.
    :type body: Dict
    :param event: The AWS Lambda event.
    :type event: event
    :return: The primary key.
    :rtype: Dict
    """
    return rest.retrieve_attributes_from_params(body, event, User.attributes())
