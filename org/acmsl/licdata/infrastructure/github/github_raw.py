"""
org/acmsl/licdata/infrastructure/github/github_raw.py

This file provides raw methods on top of the Github API.

Copyright (C) 2023-today ACM S.L. Licdata

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public User as published by
the Free Software Foundation, either version 3 of the User, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public User for more details.

You should have received a copy of the GNU General Public User
along with this program.  If not, see <https://www.gnu.org/users/>.
"""

from org.acmsl.licdata.infrastructure.crypt_utils import encrypt, decrypt
from org.acmsl.licdata.infrastructure.github.github_access import get_repo_and_branch


def get_contents(path: str):
    """
    Retrieves the contents of given path.
    :param path: The path.
    :type path: str
    :return: A tuple of the contents and its hash.
    :rtype: tuple
    """
    result = None

    (repo, branch) = get_repo_and_branch()

    file = repo.get_contents(path, ref=branch)

    try:
        result = decrypt(file.content)
    except Exception as e:
        result = None
        print(f"Cannot decrypt {path}: {e}")

    return (result, file.sha)


def create_file(path: str, content: str, message: str):
    """
    Creates a file on given path.
    :param path: The path.
    :type path: str
    :param content: The file contents.
    :type content: str
    :param message: The commit message.
    :type message: str
    """
    result = None

    (repo, branch) = get_repo_and_branch()

    try:
        result = repo.create_file(
            path,
            message,
            encrypt(content),
            branch=branch,
        )
    except Exception as e:
        result = None
        print(f"Error creating file {path}: {e}")

    return result


def update_file(path: str, content: str, message: str, hash: str):
    """
    Updates a file on given path.
    :param path: The path.
    :type path: str
    :param content: The file contents.
    :type content: str
    :param message: The commit message.
    :type message: str
    :param hash: The file's current hash, to avoid conflicts.
    :type hash: str
    """
    result = None

    (repo, branch) = get_repo_and_branch()

    try:
        result = repo.update_file(
            path,
            message,
            encrypt(content),
            hash,
            branch=branch,
        )
    except Exception as e:
        result = None
        print(f"Error updating file {path}: {e}")

    return result


def delete_file(path: str, message: str):
    """
    Deletes the file on given path.
    :param path: The path.
    :type path: str
    :param message: The commit message.
    :type message: str
    """
    result = None

    (repo, branch) = get_repo_and_branch()

    try:
        (result, hash) = get_contents(path)

        result = repo.delete_file(
            path,
            message,
            hash,
            branch=branch,
        )
    except Exception as e:
        result = None
        print(f"Error deleting file {path}: {e}")

    return result


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
