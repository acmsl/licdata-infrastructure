"""
org/acmsl/licdata/infrastructure/github/github_adapter.py

This file defines the GithubAdapter class.

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
from pythoneda.shared import BaseObject, camel_to_snake, Entity, Event
from uuid import uuid4
from typing import Callable, Dict, List, Tuple


class GithubAdapter(BaseObject):
    """
    Github adapter.

    Class name: GithubAdapter

    Responsibilities:
        - Define functions to interact with Github repositories via HTTP endpoints.

    Collaborators:
        - None
    """

    _singleton = None

    def __init__(self):
        """
        Creates a new GithubAdapter instance.
        """
        super().__init__()

    @classmethod
    def instance(cls) -> "GithubAdapter":
        """
        Retrieves the instance.
        :return: Such instance.
        :rtype: org.acmsl.licdata.infrastructure.github.GithubAdapter
        """
        if cls._singleton is None:
            cls._singleton = cls()
        return cls._singleton

    def new_id(self) -> str:
        """
        Creates a new id.
        :return: The id.
        :rtype: str
        """
        return str(uuid4())

    def find_by_id(
        self, id: str, path: str, buildEntity: Callable[[Dict], Entity]
    ) -> Tuple[Dict, str]:
        """
        Finds an item matching given id (using the path structure in github).
        :param id: The id.
        :type id: str
        :param path: The relative path.
        :type path: str
        :param buildEntity: A function to build the entity.
        :type buildEntity: callable[[Dict], pythoneda.shared.Entity]
        :return: The tuple (item, sha)
        :rtype: Tuple[Dict, str]
        """
        result = None

        data = None
        sha = None

        try:
            (data, sha) = get_contents(f"{path}/{id}/data.json")
        except Exception as err:
            GithubAdapter.logger().error(err)
            data = None

        if data:
            result = buildEntity(json.loads(data))

        return (result, sha)

    def find_all_by_attributes(self, filter: Dict, path: str) -> Tuple[List[Dict], str]:
        """
        Retrieves all items matching given attribute values.
        :param filter: The attribute filter.
        :type filter: Dict
        :param path: The relative path.
        :type path: str
        :return: A tuple of the items and the checksum.
        :rtype: Tuple[List[Dict], str]
        """
        result = []
        sha = None

        try:
            (all_items, sha) = get_contents(f"{path}/data.json")
        except Exception as err:
            GithubAdapter.logger().error(err)
            all_items = None
        if all_items is not None:
            all_items_content = json.loads(all_items)
            item = {}
            for key in filter:
                item[key] = filter[key]
            result = [
                x
                for x in all_items_content
                if self._attributes_match(x, item, filter.keys())
            ]

        return (result, sha)

    def find_all_by_attribute(
        self, attributeValue: str, attributeName: str, path: str
    ) -> Tuple[List[Dict], str]:
        """
        Finds all items matching one attribute filter.
        :param attributeValue: The attribute value.
        :type attributeValue: str
        :param attributeName: The attribute name.
        :type attributeName: str
        :param path: The relative path.
        :type path: str
        :return: The tuple of matching items and the checksum.
        :rtype: Tuple[List[Dict], str]
        """
        filter = {}
        filter[attributeName] = attributeValue
        return self.find_all_by_attributes(filter, path)

    def find_by_attribute(
        self, attributeValue: str, attributeName: str, path
    ) -> Tuple[Dict, str]:
        """
        Finds an item matching one attribute filter.
        :param attributeValue: The attribute value.
        :type attributeValue: str
        :param attributeName: The attribute name.
        :type attributeName: str
        :param path: The relative path.
        :type path: str
        :return: The tuple of matching item and the checksum.
        :rtype: Tuple[Dict, str]
        """
        result = None

        (matches, sha) = self.find_all_by_attribute(attributeValue, attributeName, path)

        if matches:
            result = matches[0]
        else:
            GithubAdapter.logger().debug(
                f"No {path} with {attributeName} {attributeValue}"
            )

        return (result, sha)

    def find_by_attributes(self, filter: Dict, path: str) -> Tuple[List[Dict], str]:
        """
        Finds an item matching given attribute filter.
        :param filter: The attribute filter.
        :type filter: Dict
        :param path: The relative path.
        :type path: str
        :return: The tuple of matching item and the checksum.
        :rtype: Tuple[List[Dict], str]
        """
        result = None

        (matches, sha) = self.find_all_by_attributes(filter, path)

        if matches:
            result = matches[0]
        else:
            GithubAdapter.logger().debug(f"No {path} found matching {filter}")

        return (result, sha)

    def insert(
        self,
        newEntityRequested: Event,
        buildNewEntity: Callable[[Event], Tuple[Entity, Event]],
        path: str,
    ) -> Event:
        """
        Inserts a new entity.
        :param newEntityRequested: The event requesting the new entity.
        :type newEntityRequested: pythoneda.shared.Event
        :param buildNewEntity: A function to create the new-entity-created e.
        :type buildNewEntity: callable[[pythoneda.shared.Event], Tuple[pythoneda.shared.Entity, pythoneda.shared.Event]]
        :param path: The relative path.
        :type path: str
        :return: The event representing the new entity has been created.
        :rtype: pythoneda.shared.Event
        """
        entity, result = buildNewEntity(newEntityRequested)

        data = None
        sha = None
        insert_new_file = False

        try:
            (data, sha) = get_contents(f"{path}/data.json")
        except Exception as err:
            GithubAdapter.logger().error(err)
            data = None
        if data is None:
            content = []
            content.append(entity.to_dict_simplified())
            create_file(
                f"{path}/data.json",
                json.dumps(content),
                result.to_json(),
            )
            insert_new_file = True
        else:
            content = json.loads(data)
            entries = [
                x
                for x in content
                if self._attributes_match(x, entity.to_dict(), primaryKey)
            ]
            if len(entries) == 0:
                content.append(entity.to_dict_simplified())
                update_file(
                    f"{path}/data.json",
                    json.dumps(content),
                    result.to_json(),
                    sha,
                )
                insert_new_file = True
            else:
                GithubAdapter.logger().info(
                    f"Not creating a new entity under {path} since another copy already exists"
                )
                insert_new_file = False

        if insert_new_file:
            create_file(
                f"{path}/{entity.id}/data.json", entity.to_json(), result.to_json()
            )
            entity_name = camel_to_snake(entity.__class__.__name__)
            timestamp = datetime.now().timestamp()
            create_file(
                f"{path}/{entity.id}/_events/{timestamp}-new_{entity_name}_requested.json",
                newEntityRequested.to_json(),
                newEntityRequested.to_json(),
            )
            timestamp = datetime.now().timestamp()
            create_file(
                f"{path}/{entity.id}/_events/{timestamp}-new_{entity_name}_created.json",
                result.to_json(),
                result.to_json(),
            )

        return result

    def get_property_name(self, prop) -> str:
        """
        Retrieves the name of the property.
        :param prop: The property.
        :type prop: property
        :return: The name of the property.
        :rtype: str
        """
        if isinstance(prop, str):
            return prop
        else:
            return prop.fget.__name__

    def _attributes_match(self, item: Dict, target: Dict, attributeNames: List[str]):
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

    def delete(
        self,
        deleteEntityRequested: Event,
        buildEntity: Callable[[Dict], Entity],
        buildInvalidDeleteEntityRequestEvent: Callable[[Event], Event],
        path: str,
    ) -> Dict:
        """
        Deletes an item in the repository.
        :param deleteEntityRequested: The event requesting the removal of an entity.
        :type deleteEntityRequested: pythoneda.shared.Event
        :param buildEntity: A function to build the entity.
        :type buildEntity: callable[[Dict], pythoneda.shared.Entity]
        :param buildInvalidDeleteEntityRequestEvent: A function to build the invalid-delete-entity-request event.
        :type buildInvalidDeleteEntityRequestEvent: Callable[[pythoneda.shared.Event], pythoneda.shared.Event]
        :param path: The relative path.
        :type path: str
        :return: The event representing the new entity has been deleted.
        :rtype: pythoneda.shared.Event
        """
        result = None
        now = datetime.now()
        deleted = now.strftime("%Y-%m-%d %H:%M:%S")
        timestamp = now.timestamp()
        data = None
        update_summary = False

        try:
            entity = None
            sha = None
            if deleteEntityRequested.entity_id is not None:
                (entity, sha) = self.find_by_id(
                    deleteEntityRequested.entity_id, path, buildEntity
                )
            elif deleteEntityRequested.entity_primary_key is not None:
                (entity, sha) = self.find_by_pk(
                    deleteEntityRequested.entity_primary_key, path, buildEntity
                )

            if entity is None:
                result = buildInvalidDeleteEntityRequestEvent(deleteEntityRequested)
            else:
                entity_name = camel_to_snake(entity.__class__.__name__)
                result = entity.delete(deleteEntityRequested)
                if result is not None:
                    update_file(
                        f"{path}/{deleteEntityRequested.entity_id}/data.json",
                        entity.to_json(),
                        result.to_json(),
                        sha,
                    )
                    create_file(
                        f"{path}/{deleteEntityRequested.entity_id}/_events/{timestamp}-{entity_name}_deleted.json",
                        result.to_json(),
                        result.to_json(),
                    )
                    create_file(
                        f"{path}/{deleteEntityRequested.entity_id}.deleted",
                        "",
                        result.to_json(),
                    )
                    update_summary = True
        except Exception as err:
            GithubAdapter.logger().error(err)
            update_summary = False

        if update_summary:
            try:
                (data, sha) = get_contents(f"{path}/data.json")
            except Exception as err:
                GithubAdapter.logger().error(err)
                data = None

            if data is not None:
                content = json.loads(data)
                summary = any(
                    [
                        x
                        for x in content
                        if x.get("id", None) == deleteEntityRequested.entity_id
                    ]
                )
                if summary:
                    update_file(
                        f"{path}/data.json",
                        json.dumps(
                            [
                                x
                                for x in content
                                if x.get("id", None) != deleteEntityRequested.entity_id
                            ]
                        ),
                        result.to_json(),
                        sha,
                    )
                else:
                    GithubAdapter.logger().error(
                        f"{path}/data.json does not contain {deleteEntityRequested.entity_id}"
                    )

        return result

    def delete_by_pk(
        self,
        primaryKey: List,
        path: str,
        primaryKeyNames: List,
        attributeNames: List,
        sensitiveAttributes: List,
    ) -> Dict:
        """
        Deletes an item in the repository.
        :param primaryKey: The primary key of the item to delete.
        :type primaryKey: List
        :param path: The relative path.
        :type path: str
        :param primaryKeyNames: The entity's primary key.
        :type primaryKeyNames: List
        :param attributeNames: The entity's attribute names.
        :type attributeNames: List
        :param sensitiveAttributes: The names of the attributes that need to be encrypted.
        :type sensitiveAttributes: List
        :return: The information about the removed item.
        :rtype: Dict
        """
        result = {}
        now = datetime.now()
        deleted = now.strftime("%Y-%m-%d %H:%M:%S")
        timestamp = now.timestamp()
        data = None
        delete_file = False
        entry = {}
        primary_key = primaryKey.to_dict()
        for attribute in primaryKeyNames:
            value = primary_key.get(attribute, None)
            if attribute in sensitiveAttributes:
                value = encrypt(value)
            result[attribute] = value
        result["id"] = result

        try:
            (data, sha) = get_contents(f"{path}/data.json")
        except Exception as err:
            GithubAdapter.logger().error(err)
            data = None

        if data is not None:
            content = json.loads(data)
            entries = [
                x
                for x in content
                if self._attributes_match(x, primary_key, primaryKeyNames)
            ]
            if len(entries) > 0:
                entry = entries[0]
                update_file(
                    f"{path}/data.json",
                    json.dumps([x for x in entries if x != entry]),
                    f"Deleted {result} in {path} collection",
                    sha,
                )
                delete_file = True
            else:
                GithubAdapter.logger().info(
                    f"Entity {primaryKey} does not exist in {path} collection"
                )

        if delete_file:
            result = {}
            for attribute in attributeNames:
                value = primary_key.get(attribute, None)
                if attribute in sensitiveAttributes:
                    value = encrypt(value)
                result[attribute] = value
            result["id"] = entry.id
            result["_deleted"] = deleted
            delete_file(
                f"{path}/{entry.id}/data.json",
                json.dumps(result),
                f"Deleted {entry.id} in {path} collection",
            )
            create_file(
                f"{path}/{entry.id}/_events/{timestamp}-deleted.json",
                json.dumps(result),
                f"Created a new entry {timestamp}-deleted.json in {path}/{entry.id}/_events/ collection",
            )

        return result

    def list(self, path: str) -> Tuple[List, str]:
        """
        Retrieves all items.
        :param path: The relative path.
        :type path: str
        :return: The list of all items.
        :rtype: List
        """
        (data, sha) = get_contents(f"{path}/data.json")
        return (json.loads(data), sha)

    def update(
        self,
        updateEntityRequested: Event,
        buildEntity: Callable[[Event], Tuple[Entity, Event]],
        buildEntityUpdatedEvent: Callable[[Entity, Event], Event],
        buildInvalidUpdateEntityRequestEvent: Callable[[Event], Event],
        path: str,
    ) -> Event:
        """
        Inserts a new entity.
        :param updateEntityRequested: The event requesting the update of an entity.
        :type updateEntityRequested: pythoneda.shared.Event
        :param buildEntity: A function to create the entity.
        :type buildEntity: callable[[Dict], pythoneda.shared.Entity]
        :param buildEntityUpdatedEvent: A function to create the entity-updated event.
        :type buildEntityUpdatedEvent: Callable[[Entity, Event], Event],
        :param buildInvalidUpdateEntityRequestEvent: A function to build the invalid-update-entity-request event.
        :type buildInvalidUpdateEntityRequestEvent: Callable[[pythoneda.shared.Event], pythoneda.shared.Event]
        :param path: The relative path.
        :type path: str
        :return: The event representing the new entity has been updated.
        :rtype: pythoneda.shared.Event
        """
        result = None
        try:
            entity = None
            sha = None
            if updateEntityRequested.entity_id is not None:
                (entity, sha) = self.find_by_id(
                    id=updateEntityRequested.entity_id,
                    path=path,
                    buildEntity=buildEntity,
                )
            elif updateEntityRequested.entity_primary_key is not None:
                (entity, sha) = self.find_by_pk(
                    updateEntityRequested.entity_primary_key, path, buildEntity
                )

            if entity is None:
                print(f"Entity not found!")
                result = buildInvalidUpdateEntityRequestEvent(updateEntityRequested)
            else:
                result = buildEntityUpdatedEvent()
                entity.apply(result)
                update_file(
                    f"{path}/{entity.id}/data.json",
                    json.dumps(entity.to_dict()),
                    result.to_json(),
                    sha,
                )

                entity_name = camel_to_snake(entity.__class__.__name__)
                timestamp = datetime.now().timestamp()
                create_file(
                    f"{path}/{entity.id}/_events/{timestamp}-update_{entity_name}_requested.json",
                    updateEntityRequested.to_json(),
                    updateEntityRequested.to_json(),
                )
                timestamp = datetime.now().timestamp()
                create_file(
                    f"{path}/{entity.id}/_events/{timestamp}-{entity_name}_updated.json",
                    result.to_json(),
                    result.to_json(),
                )
        except Exception as err:
            GithubAdapter.logger().error(err)

        return result


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
