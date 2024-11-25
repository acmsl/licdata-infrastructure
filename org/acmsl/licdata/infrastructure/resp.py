"""
org/acmsl/licdata/infrastructure/resp.py

This file provides some utilities for parsing parameters in AWS Lambda events.

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

import json
from typing import Dict


def build_response(status: int, body: Dict, event, context) -> Dict:
    """
    Builds a response.
    :param status: The status code.
    :type status: int
    :param body: The event body.
    :type body: Dict
    :param event: The AWS Lambda event.
    :type event: event
    :param context: THe AWS Lambda context.
    :type context: context
    :return: A dictionary with the response.
    :rtype: Dict
    """
    return {
        "headers": {"Content-Type": "application/json"},
        "event": str(event),
        "context": str(context),
        "statusCode": status,
        "body": json.dumps(body, indent=4, sort_keys=True, default=str),
    }
