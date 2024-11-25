"""
org/acmsl/licdata/infrastructure/crypt_utils.py

This file provides some cryptographic utilities.

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
from cryptography.fernet import Fernet


def get_key() -> str:
    """
    Retrieves the key from the thread local storage.
    :return: Such value.
    :rtype: str
    """
    local = threading.local()
    if not hasattr(local, "key"):
        local.key = os.environ["KEY"]

    return local.key


def encryption_enabled():
    """
    Checks whether encryption is enabled.
    :return: The encrypted files.
    :rtype: List
    """
    local = threading.local()
    if not hasattr(local, "encryptedFiles"):
        local.encrypted_files = os.environ["ENCRYPTED_FILES"]

    return local.encrypted_files


def encrypt(content: str) -> str:
    """
    Encrypts given text.
    :param content: The content to encrypt.
    :type content: str
    :return: The encypted content.
    :rtype: str
    """
    result = None

    if encryption_enabled():
        fernet = Fernet(get_key())

        try:
            result = fernet.encrypt(content.encode())
        except Exception as e:
            print(f"{content} could not be encrypted: {e}")
    else:
        result = content

    return result


def decrypt(content):
    """
    Decrypts given text.
    :param content: The text to decrypt.
    :type content: str
    :return: The plain-text content.
    :rtype: str
    """
    result = None

    if encryption_enabled():
        fernet = Fernet(get_key())

        try:
            result = fernet.decrypt(content).decode()
        except Exception as e:
            print(f"{content} could not be decrypted: {e}")
    else:
        result = content

    return result


def decrypt_file(file) -> str:
    """
    Decrypts given file.
    :param file: The file.
    :type file: file
    :return: The decrypted contents of the file.
    :rtype: str
    """
    result = None

    if encryption_enabled():
        result = decrypt(file.decoded_content.decode())

    else:
        result = file.decoded_content.decode()

    return result
