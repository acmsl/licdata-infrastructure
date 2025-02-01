"""
org/acmsl/licdata/infrastructure/github/github_adapter.py

This file provides some functions to use github as domain repository.

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

from datetime import datetime
from .github_raw import get_contents, create_file, update_file, delete_file
import json
from org.acmsl.licdata.infrastructure.crypt_utils import encrypt
from pythoneda.shared import Entity
from uuid import uuid4
from typing import Dict, List


def new_id() -> str:
    """
    Creates a new id.
    :return: The id.
    :rtype: str
    """
    return str(uuid4())


def find_by_id(id: str, path: str):
    """
    Finds an item matching given id (using the path structure in github).
    :param id: The id.
    :type id: str
    :param path: The relative path.
    :type path: str
    :return: The tuple (item, sha)
    :rtype: tuple
    """
    result = None

    data = None

    try:
        (data, _) = get_contents(f"{path}/{id}/data.json")
    except:
        data = None

    if data:
        result = json.loads(data)

    return result


def find_all_by_attributes(filter: Dict, path: str):
    """
    Retrieves all items matching given attribute values.
    :param filter: The attribute filter.
    :type filter: Dict
    :param path: The relative path.
    :type path: str
    :return: A tuple of the items and the checksum.
    :rtype: tuple
    """
    result = []

    try:
        (all_items, _) = get_contents(f"{path}/data.json")
    except:
        all_items = None
    if all_items:
        all_items_content = json.loads(all_items)
        item = {}
        for key in filter:
            item[key] = filter[key]
        result = [
            x for x in all_items_content if _attributes_match(x, item, filter.keys())
        ]

    return result


def find_all_by_attribute(attributeValue: str, attributeName: str, path: str):
    """
    Finds all items matching one attribute filter.
    :param attributeValue: The attribute value.
    :type attributeValue: str
    :param attributeName: The attribute name.
    :type attributeName: str
    :param path: The relative path.
    :type path: str
    :return: The tuple of matching items and the checksum.
    :rtype: tuple
    """
    filter = {}
    filter[attributeName] = attributeValue
    return find_all_by_attributes(filter, path)


def find_by_attribute(attributeValue: str, attributeName: str, path):
    """
    Finds an item matching one attribute filter.
    :param attributeValue: The attribute value.
    :type attributeValue: str
    :param attributeName: The attribute name.
    :type attributeName: str
    :param path: The relative path.
    :type path: str
    :return: The tuple of matching item and the checksum.
    :rtype: tuple
    """
    result = None

    matches = find_all_by_attribute(attributeValue, attributeName, path)

    if matches:
        result = matches[0]
    else:
        print(f"No {path} with {attributeName} {attributeValue}")

    return result


def find_by_attributes(filter: Dict, path: str) -> List:
    """
    Finds an item matching given attribute filter.
    :param filter: The attribute filter.
    :type filter: Dict
    :param path: The relative path.
    :type path: str
    :return: The tuple of matching item and the checksum.
    :rtype: tuple
    """
    result = None

    matches = find_all_by_attributes(filter, path)

    if matches:
        result = matches[0]
    else:
        print(f"No {path} found matching {filter}")

    return result


def insert(
    event: Entity,
    path: str,
    primaryKey: List,
    filterKeys: List,
    attributeNames: List,
    encryptedAttributes: List,
):
    """
    Inserts a new entity.
    :param entity: The entity to persist.
    :type entity: pythoneda.shared.Entity
    :param path: The relative path.
    :type path: str
    :param primaryKey: The entity's primary key.
    :type primaryKey: List
    :param filterKeys: The entity's filter keys.
    :type filterKeys: List
    :param attributeNames: The entity's attribute names.
    :type attributeNames: List
    :param encryptedAttributes: The names of the attributes that need to be encrypted.
    :type encryptedAttributes: List
    :return: The id of the persisted entity.
    :rtype: str
    """
    result = event.id
    now = datetime.now()
    created = now.strftime("%Y-%m-%d %H:%M:%S")
    timestamp = now.timestamp()
    data = None
    insert_new_file = False
    item = {}
    entity_attrs = event.to_dict()
    for attribute in primaryKey + filterKeys:
        value = entity_attrs.get(attribute, None)
        if attribute in encryptedAttributes:
            value = encrypt(value)
        item[attribute] = value
    item["id"] = result

    try:
        (data, sha) = get_contents(f"{path}/data.json")
    except:
        data = None
    if data is None:
        content = []
        content.append(item)
        create_file(
            f"{path}/data.json",
            json.dumps(content),
            f"First instance in {path} collection: {result}",
        )
        insert_new_file = True
    else:
        content = json.loads(data)
        entries = [x for x in content if _attributes_match(x, entity_attrs, primaryKey)]
        if len(entries) == 0:
            content.append(item)
            update_file(
                f"{path}/data.json",
                json.dumps(content),
                f"Updated {result} in {path} collection",
                sha,
            )
            insert_new_file = True
        else:
            print(f"Entity {entity} already exists in {path} collection")
            insert_new_file = False

    if insert_new_file:
        item = {}
        for attribute in attributeNames:
            value = entity_attrs.get(attribute, None)
            if attribute in encryptedAttributes:
                value = encrypt(value)
            item[attribute] = value
        item["id"] = result
        item["_created"] = created
        item.pop("_updated", None)
        create_file(
            f"{path}/{result}/data.json",
            json.dumps(item),
            f"Created a new entry {result} in {path} collection",
        )
        item = event.to_dict()
        item["_type"] = "org.acmsl.licdata.events.client.NewClientCreated"
        create_file(
            f"{path}/{result}/_events/{timestamp}-new_client_created.json",
            json.dumps(item),
            f"Created a new entry {timestamp}-new_client_created.json in {path}/{result}/_events/ collection",
        )

    return result


def get_property_name(property) -> str:
    """
    Retrieves the name of the property.
    :param property: The property.
    :type property: property
    :return: The name of the property.
    :rtype: str
    """
    if isinstance(property, str):
        return property
    else:
        return property.fget.__name__


def _attributes_match(item: Dict, target: Dict, attributeNames: List[str]):
    """
    Checks if two entities share the same attributes.
    :param item: The first entity.
    :type item: Dict
    :param target: The second entity.
    :type target: Dict
    :param attributeNames: The attributes to check.
    :type attributeNames: List[str]
    :return: True if they share the same attributes.
    :rtype: bool
    """
    result = True

    for attribute_name in attributeNames:
        if item.get(attribute_name, None) != target.get(attribute_name, None):
            result = False
            break

    return result


def update(
    entity,
    path: str,
    primaryKey: List,
    filterKeys: List,
    attributeNames: List,
    encryptedAttributes: List,
):
    """
    Updates given entity.
    :param entity: The entity to update.
    :type entity: ValueObject from pythoneda.value_object
    :param path: The relative path.
    :type path: str
    :param primaryKey: The entity's primary key.
    :type primaryKey: List
    :param filterKeys: The entity's filter keys.
    :type filterKeys: List
    :param attributeNames: The entity's attribute names.
    :type attributeNames: List
    :param encryptedAttributes: The names of the attributes that need to be encrypted.
    :type encryptedAttributes: List
    """
    id = entity.get("id")
    item = {}
    item["id"] = id
    for attribute in primaryKey + filterKeys:
        value = entity.get(attribute)
        if attribute in encryptedAttributes:
            value = encrypt(value)
        item[attribute] = value
    try:
        (data, sha) = get_contents(f"{path}/data.json")
    except:
        data = None
    if data:
        content = json.loads(data)
        existing = [x for x in content if x.get("id") == id]
        if existing and not _attributes_match(existing[0], entity, attributeNames):
            remaining = [x for x in content if x.get("id") != id]
            remaining.append(item)
            update_file(
                f"{path}/data.json",
                json.dumps(remaining),
                f"Updated {id} in {path}/data.json",
                sha,
            )
    try:
        (old_item, oldSha) = get_contents(f"{path}/{id}/data.json")
    except:
        old_item = None
    if old_item:
        for attribute in attributeNames:
            value = entity.get(attribute)
            if attribute in encryptedAttributes:
                value = encrypt(value)
            item[attribute] = value
        item["id"] = id
        item["_created"] = entity.get("_created")
        item["_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        update_file(
            f"{path}/{id}/data.json",
            json.dumps(item),
            f"Updated {path}/{id}/data.json",
            oldSha,
        )
    else:
        print(f"{path}/{id}/data.json not found")

    return item


def delete(id: str, path: str):
    """
    Deletes an item in the repository.
    :param id: The id.
    :type id: str
    :param path: The relative path.
    :type path: str
    :return: True if the item gets removed.
    :rtype: bool
    """
    result = False

    try:
        (data, _) = get_contents(f"{path}/data.json")
    except:
        data = None
    if data:
        content = json.loads(data)
        existing = [x for x in content if x.get("id") != id]
        update_file(
            f"{path}/data.json",
            json.dumps(existing),
            f"Deleted {id} from {path}/data.json",
            sha,
        )

        delete_file(f"{path}/{id}/data.json", f"Deleted {path}/{id}/data.json")
        result = True

    return result


def list(path: str) -> List:
    """
    Retrieves all items.
    :param path: The relative path.
    :type path: str
    :return: The list of all items.
    :rtype: List
    """
    (data, _) = get_contents(f"{path}/data.json")
    return json.loads(data)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
