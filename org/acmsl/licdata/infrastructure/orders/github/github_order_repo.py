"""
org/acmsl/licdata/infrastructure/github/github_order_repo.py

This file provides a OrderRepo supported by Github.

Copyright (C) 2023-today ACM S.L. Licdata

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public Order as published by
the Free Software Foundation, either version 3 of the Order, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public Order for more details.

You should have received a copy of the GNU General Public Order
along with this program.  If not, see <https://www.gnu.org/orders/>.
"""

from org.acmsl.licdata import OrderRepo
from org.acmsl.licdata.infrastructure.github import GithubRepo

from typing import Dict, List


class GithubOrderRepo(OrderRepo):
    """
    A OrderRepo that uses Github as persistence backend.

    Class name: GithubOrderRepo

    Responsibilities:
        - Provide all order repository operations using Github as backend.

    Collaborators:
        - GithubRepo: Delegates all persistence operations in it.
    """

    def __init__(self):
        """
        Creates a new instance.
        """
        super().__init__()
        self._githubRepo = GithubRepo("orders", self._entity_class)

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
        Retrieves the order matching given id.
        :param id: The order id.
        :type id: str
        :return: The order.
        :rtype: Order from domain.order
        """
        return self._githubRepo.find_by_id(id)

    def find_by_attribute(self, attributeName: str, attributeValue: str):
        """
        Retrieves the order matching given attribute.
        :param attributeName: The attribute name.
        :type attributeName: str
        :param attributeValue: The attribute value.
        :type attributeValue: str
        :return: The order.
        :rtype: Order from domain.order
        """
        return self._githubRepo.find_by_attribute(attribute_name, attribute_value)

    def insert(self, item):
        """
        Inserts a new Order.
        :param item: The order.
        :type item: Order from domain.order
        """
        return self._githubRepo.insert(item)

    def update(self, item):
        """
        Updates an Order.
        :param item: The order to update.
        :type item: Order from domain.order
        """
        return self._githubRepo.update(item)

    def delete(self, id: str):
        """
        Deletes an Order.
        :param id: The id of the order.
        :type id: str
        :return: True if the order is removed.
        :rtype: bool
        """
        return self._githubRepo.delete(id)

    def find_by_pk(self, pk: Dict):
        """
        Retrieves an Order by its primary key.
        :param pk: The primary key attributes.
        :type pk: Dict
        :return: The order matching given criteria.
        :rtype: Order from domain.order
        """
        return self._githubRepo.find_by_pk(pk)

    def list(self) -> List:
        """
        Lists all Orders.
        :return: The list of all orders.
        :rtype: List
        """
        return self._githubRepo.list()
