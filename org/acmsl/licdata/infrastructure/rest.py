"""
org/acmsl/licdata/infrastructure/rest.py

This file provides some REST methods.

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

from pythoneda.shared import Repo

from .params import load_body, retrieve_param, retrieve_id
from .resp import build_response
import inspect
from datetime import datetime
from typing import Dict, Callable, List


def retrieve_attributes_from_params(body: Dict, event, attributeNames: List) -> Dict:
    """
    Given a list of attribute names, retrieves their values from the body/event.
    :param body: The event body.
    :type body: Dict
    :param event: The AWS Lambda event.
    :type event: event
    :param attributeNames: The list of attribute names.
    :type attributeNames: List
    :return: A dictionary with key-value entries for each attribute.
    :rtype: Dict
    """
    result = {}

    for attribute in attribute_names:
        result[attribute] = retrieve_param(attribute, body, event, None)

    return result


def find_by_id(event, context, repo):
    """
    Finds an entity by its id in given repository.
    :param event: The AWS Lambda event.
    :type event: event
    :param context: The AWS Lambda context.
    :type context: context
    :param repo: The entity repository.
    :type repo: pythoneda.Repo
    :return: The matching entity.
    :rtype: pythoneda.Entity
    """
    status = 200

    (body, error) = load_body(event)
    if error:
        status = 500
        resp_body = {"error": "Cannot parse body"}
        response = build_response(status, resp_body, event, context)
    else:
        id = retrieve_id(body, event)

        print(f"Finding by {id}")
        (item, sha) = repo.find_by_id(id)
        print(f"Retrieved {item}")
        if item:
            status = 200
            resp_body = item
            response = build_response(status, resp_body, event, context)
        else:
            status = 404
            resp_body = {"error": "not found"}
            response = build_response(status, resp_body, event, context)

    return response


def create(
    event, context, retrievePk: Callable, retrieveAttributes: Callable, repo: Repo
) -> Dict:
    """
    Creates a new entity using given repo.
    :param event: The AWS Lambda event.
    :type event: event
    :param context: The AWS Lambda context.
    :type context: context
    :param retrievePk: The function to retrieve the primary key.
    :type retrievePk: Callable
    :param retrieveAttributes: The function to retrieve the attributes.
    :type retrieveAttributes: Callable
    :param repo: The entity repository.
    :type repo: pythoneda.Repo
    :return: The response.
    :rtype: Dict
    """
    status = 200

    (body, error) = load_body(event)
    if error:
        status = 500
        resp_body = {"error": "Cannot parse body"}
        response = build_response(status, resp_body, event, context)
    else:
        pk = retrievePk(body, event)
        attributes = retrieveAttributes(body, event)

        (item, sha) = repo.find_by_pk(pk)
        if item:
            status = 409
            resp_body = {}
            resp_body.update(attributes)
            resp_body.update({"id": item["id"]})
            if "_created" in item:
                resp_body.update({"_created": item["_created"]})
            response = build_response(status, resp_body, event, context)
        else:
            attributes["_created"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            attributes.pop("_updated", None)
            id = repo.insert(attributes)
            headers = event.get("headers", {})
            host = headers.get("host", event.get("host", ""))
            status = 201
            resp_body = {}
            resp_body.update(attributes)
            resp_body.update({"id": id})
            response = build_response(status, resp_body, event, context)
            response["headers"].update(
                {"Location": f"https://{host}/{repo.path()}/{id}"}
            )

    return response


def update(event, context, retrieveAttributes: Callable, repo: Repo):
    """
    Updates an existing entity using given repo.
    :param event: The AWS Lambda event.
    :type event: event
    :param context: The AWS Lambda context.
    :type context: context
    :param retrieveAttributes: The function to retrieve the attributes.
    :type retrieveAttributes: Callable
    :param repo: The entity repository.
    :type repo: pythoneda.Repo
    :return: The response.
    :rtype: Dict
    """
    status = 200

    (body, error) = load_body(event)
    if error:
        status = 500
        resp_body = {"error": "Cannot parse body"}
        response = build_response(status, resp_body, event, context)
    else:
        id = retrieve_id(body, event)
        attributes = retrieveAttributes(body, event)
        attributes["id"] = id
        (item, sha) = repo.find_by_id(id)
        if item:
            attributes["_created"] = item["_created"]
            resp_body = repo.update(attributes)
            status = 200
            response = build_response(status, resp_body, event, context)
        else:
            status = 404
            resp_body = {"error": "not found"}
            response = build_response(status, resp_body, event, context)

    return response


def delete(event, context, repo):
    """
    Deletes an existing entity using given repo.
    :param event: The AWS Lambda event.
    :type event: event
    :param context: The AWS Lambda context.
    :type context: context
    :param repo: The entity repository.
    :type repo: pythoneda.Repo
    :return: The response.
    :rtype: Dict
    """
    status = 200

    (body, error) = load_body(event)
    if error:
        status = 500
        resp_body = {"error": "Cannot parse body"}
        response = build_response(status, resp_body, event, context)
    else:
        id = retrieve_id(body, event)

        (item, sha) = repo.find_by_id(id)
        if item:
            repo.delete(id)
            status = 200
            resp_body = {"id": item["id"]}
            response = build_response(status, resp_body, event, context)
        else:
            status = 404
            resp_body = {"error": "not found"}
            response = build_response(status, resp_body, event, context)

    return response


def list(event, context, repo):
    """
    List all items, using given repo.
    :param event: The AWS Lambda event.
    :type event: event
    :param context: The AWS Lambda context.
    :type context: context
    :param repo: The entity repository.
    :type repo: pythoneda.Repo
    :return: The response.
    :rtype: Dict
    """
    status = 200

    (body, error) = load_body(event)
    if error:
        status = 500
        resp_body = {"error": "Cannot parse body"}
        response = build_response(status, resp_body, event, context)
    else:
        try:
            (items, sha) = repo.list()
            if items:
                resp_body = items
                response = build_response(status, resp_body, event, context)
            else:
                resp_body = []
                response = build_response(status, resp_body, event, context)
        except Exception as e:
            print(e)
            status = 500
            resp_body = {"error": str(e)}
            response = build_response(status, resp_body, event, context)

    return response
