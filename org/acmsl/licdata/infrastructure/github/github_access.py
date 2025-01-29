"""
org/acmsl/licdata/infrastructure/github/github_access.py

This file provides some functions to access github repositories and branches.

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

import os
import threading
from github import Auth, Github


def get_repo():
    """
    Retrieves the github repo under the thread-local attribute "repository_name".
    :return: The repository.
    :rtype: object
    """
    local = threading.local()

    if not hasattr(local, "repo"):
        if not hasattr(local, "token"):
            token = os.environ.get("GITHUB_TOKEN", None)
            if token is None:
                print("GITHUB_TOKEN environment variable not set")
                raise ValueError("GITHUB_TOKEN environment variable not set")
            local.token = token

        if not hasattr(local, "github"):
            local.github = Github(auth=Auth.Token(local.token))

        if not hasattr(local, "repository_name"):
            repository_name = os.environ.get("GITHUB_REPO", None)
            if repository_name is None:
                raise ValueError("GITHUB_REPO environment variable not set")
            local.repository_name = repository_name

        local.repo = local.github.get_repo(local.repository_name)

    return local.repo


def get_branch():
    """
    Retrieves the github repo under the thread-local attribute "branch".
    :return: The branch.
    :rtype: str
    """
    local = threading.local()

    if not hasattr(local, "branch"):
        branch = os.environ.get("GITHUB_BRANCH", None)
        if branch is None:
            raise ValueError("GITHUB_BRANCH environment variable not set")
        local.branch = branch

    return local.branch


def get_repo_and_branch():
    """
    Retrieves the github repo and branch using thread-local storage.
    :return: The repository and branch.
    :rtype: tuple
    """
    return (get_repo(), get_branch())


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
