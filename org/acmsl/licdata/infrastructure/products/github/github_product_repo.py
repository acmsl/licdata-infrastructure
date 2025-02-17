"""
org/acmsl/licdata/infrastructure/github/github_product_repo.py

This file provides a ProductRepo supported by Github.

Copyright (C) 2023-today ACM S.L. Licdata

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public Product as published by
the Free Software Foundation, either version 3 of the Product, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public Product for more details.

You should have received a copy of the GNU General Public Product
along with this program.  If not, see <https://www.gnu.org/products/>.
"""

from org.acmsl.licdata import ProductRepo
from org.acmsl.licdata.infrastructure.github import GithubRepo

from typing import Dict, List


class GithubProductRepo(ProductRepo):
    """
    A ProductRepo that uses Github as persistence backend.

    Class name: GithubProductRepo

    Responsibilities:
        - Provide all product repository operations using Github as backend.

    Collaborators:
        - GithubRepo: Delegates all persistence operations in it.
    """

    def __init__(self):
        """
        Creates a new instance.
        """
        super().__init__()
        self._githubRepo = GithubRepo("products", self._entity_class)

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
        Retrieves the product matching given id.
        :param id: The product id.
        :type id: str
        :return: The product.
        :rtype: Product from domain.product
        """
        return self._githubRepo.find_by_id(id)

    def find_by_attribute(self, attributeName: str, attributeValue: str):
        """
        Retrieves the product matching given attribute.
        :param attributeName: The attribute name.
        :type attributeName: str
        :param attributeValue: The attribute value.
        :type attributeValue: str
        :return: The product.
        :rtype: Product from domain.product
        """
        return self._githubRepo.find_by_attribute(attribute_name, attribute_value)

    def insert(self, item):
        """
        Inserts a new Product.
        :param item: The product.
        :type item: Product from domain.product
        """
        return self._githubRepo.insert(item)

    def update(self, item):
        """
        Updates a Product.
        :param item: The product to update.
        :type item: Product from domain.product
        """
        return self._githubRepo.update(item)

    def delete(self, id: str):
        """
        Deletes a Product.
        :param id: The id of the product.
        :type id: str
        :return: True if the product is removed.
        :rtype: bool
        """
        return self._githubRepo.delete(id)

    def find_by_pk(self, pk: Dict):
        """
        Retrieves a Product by its primary key.
        :param pk: The primary key attributes.
        :type pk: Dict
        :return: The product matching given criteria.
        :rtype: Product from domain.product
        """
        return self._githubRepo.find_by_pk(pk)

    def list(self) -> List:
        """
        Lists all Products.
        :return: The list of all products.
        :rtype: List
        """
        return self._githubRepo.list()
