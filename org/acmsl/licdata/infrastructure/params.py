"""
org/acmsl/licdata/infrastructure/params.py

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
import base64


def load_body(event):
    """
    Parses given event.
    :param event: The event to process.
    :type event: Event
    :return: A tuple with the body and the error, if any.
    :rtype: tuple
    """
    body = None
    respBody = {}
    error = True

    body_entry = event.get("body", event)

    if body_entry is None:
        body = {"error": "Missing 'body'"}
    else:
        if type(body_entry) is dict:
            body = body_entry
            error = False
        elif type(body_entry) is str:
            try:
                body = json.loads(body_entry)
                error = False
            except Exception as encoding_error:
                try:
                    body = json.loads(base64.decodebytes(str.encode(body_entry)))
                    error = False
                except Exception as giving_up:
                    body = {
                        "error": "Not json, not base64-encoded",
                        "errors": [giving_up, encoding_error],
                    }
        else:
            body = {"error": "Unknown input"}

    return (body, error)


def retrieve_param(paramName: str, body, event, defaultValue) -> str:
    """
    Retrieves the value of given parameter.
    :param paramName: The name of the parameter.
    :type paramName: str
    :param event: The AWS Lambda event.
    :type event: object
    :param defaultValue: The default value if the parameter is missing.
    :type defaultValue: str
    :return: The value of the parameter.
    :rtype: str
    """
    result = None

    if body:
        result = body.get(paramName, None)

    if result is None:
        query_string_parameters = event.get("queryStringParameters", {})
        result = query_string_parameters.get(paramName, None)

    if result is None:
        path_parameters = event.get("pathParameters", {})
        result = path_parameters.get(paramName)

    if result is None:
        result = event.get(paramName, defaultValue)

    return result


def retrieve_id(body, event) -> str:
    """
    Retrieves the value of the 'id' parameter.
    :param body: The body.
    :type body: Dict
    :param event: The AWS Lambda event.
    :type event: object
    :return: The id.
    :rtype: str
    """
    return retrieve_param("id", body, event, None)


def retrieve_client_id(body, event):
    """
    Retrieves the value of the 'client id' parameter.
    :param body: The body.
    :type body: Dict
    :param event: The AWS Lambda event.
    :type event: object
    :return: The client id.
    :rtype: str
    """
    return retrieve_param("clientId", body, event, None)


def retrieve_installation_code(body, event):
    """
    Retrieves the value of the 'installation code' parameter.
    :param body: The body.
    :type body: Dict
    :param event: The AWS Lambda event.
    :type event: object
    :return: The installation code.
    :rtype: str
    """
    return retrieve_param("installationCode", body, event, None)


def retrieve_product(body, event):
    """
    Retrieves the value of the 'product' parameter.
    :param body: The body.
    :type body: Dict
    :param event: The AWS Lambda event.
    :type event: object
    :return: The product.
    :rtype: str
    """
    return retrieve_param("product", body, event, None)


def retrieve_product_version(body, event):
    """
    Retrieves the value of the 'product version' parameter.
    :param body: The body.
    :type body: Dict
    :param event: The AWS Lambda event.
    :type event: object
    :return: The product version.
    :rtype: str
    """
    return retrieve_param("productVersion", body, event, "1")


def retrieve_description(body, event):
    """
    Retrieves the value of the 'description' parameter.
    :param body: The body.
    :type body: Dict
    :param event: The AWS Lambda event.
    :type event: object
    :return: The description.
    :rtype: str
    """
    return retrieve_param("description", body, event, "1")


def retrieve_duration(body, event):
    """
    Retrieves the value of the 'duration' parameter.
    :param body: The body.
    :type body: Dict
    :param event: The AWS Lambda event.
    :type event: object
    :return: The duration.
    :rtype: str
    """
    return retrieve_param("duration", body, event, 7)


def retrieve_bundle(body, event):
    """
    Retrieves the value of the 'bundle' parameter.
    :param body: The body.
    :type body: Dict
    :param event: The AWS Lambda event.
    :type event: object
    :return: The bundle.
    :rtype: str
    """
    return retrieve_param("bundle", body, event, None)


def retrieve_email(body, event):
    """
    Retrieves the value of the 'email' parameter.
    :param body: The body.
    :type body: Dict
    :param event: The AWS Lambda event.
    :type event: object
    :return: The email.
    :rtype: str
    """
    return retrieve_param("email", body, event, None)


def retrieve_address(body, event):
    """
    Retrieves the value of the 'address' parameter.
    :param body: The body.
    :type body: Dict
    :param event: The AWS Lambda event.
    :type event: object
    :return: The address.
    :rtype: str
    """
    return retrieve_param("address", body, event, None)


def retrieve_contact(body, event):
    """
    Retrieves the value of the 'contact' parameter.
    :param body: The body.
    :type body: Dict
    :param event: The AWS Lambda event.
    :type event: object
    :return: The contact.
    :rtype: str
    """
    return retrieve_param("contact", body, event, None)


def retrieve_phone(body, event):
    """
    Retrieves the value of the 'phone' parameter.
    :param body: The body.
    :type body: Dict
    :param event: The AWS Lambda event.
    :type event: object
    :return: The phone.
    :rtype: str
    """
    return retrieve_param("phone", body, event, None)
