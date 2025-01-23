# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/infrastructure/github/__init__.py

This file ensures org.acmsl.licdata.infrastructure.clients.github is a namespace.

Copyright (C) 2024-today acmsl's Licdata-Infrastructure

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
__path__ = __import__("pkgutil").extend_path(__path__, __name__)

from .github_access import get_repo, get_branch, get_repo_and_branch
from .github_adapter import (
    new_id,
    find_by_id,
    find_all_by_attributes,
    find_all_by_attribute,
    find_by_attribute,
    find_by_attributes,
    insert,
    update,
    delete,
    list,
)
from .github_raw import get_contents, create_file, update_file, delete_file
from .github_repo import GithubRepo

# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
