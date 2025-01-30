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

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hmac, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import struct
import threading
from typing import Tuple


AES_KEY_LEN = 32
HMAC_KEY_LEN = 64

HEADER_FIELD_END = 0
HEADER_FIELD_KEY_NAME = 1
KEY_FIELD_END = 0
KEY_FIELD_VERSION = 1
KEY_FIELD_AES_KEY = 3
AES_KEY_LEN = 32
KEY_FIELD_HMAC_KEY = 5
HMAC_KEY_LEN = 64
MAX_FIELD_LEN = 1 << 20


def get_key() -> Tuple[bytes, bytes]:
    """
    Retrieves the key from the thread local storage, or from the environment variable.
    :return: The AES and HMAC pieces of the key.
    :rtype: Tuple[bytes, bytes]
    """
    local = threading.local()
    if not hasattr(local, "key"):
        b64_key = os.environ.get("CRYPT_KEY", None)
        if b64_key is None:
            raise ValueError("CRYPT_KEY environment variable not set")
        else:
            key = base64.b64decode(b64_key)
        local.key = key

        local.aes, local.hmac = read_key(key)

    return (local.aes, local.hmac)


def encryption_enabled():
    """
    Checks whether encryption is enabled.
    :return: The encrypted files.
    :rtype: List
    """
    local = threading.local()
    if not hasattr(local, "encryptionEnabled"):
        encryption_enabled = os.environ.get("ENCRYPTION_ENABLED", None)
        if encryption_enabled is None:
            raise ValueError("ENCRYPTION_ENABLED environment variable not set")
        local.encryption_enabled = encryption_enabled

    return local.encryption_enabled


def read_be(input: bytes, index: int, size: int = 4) -> Tuple[bytes, int]:
    """
    Reads a big-endian X-bytes integer from a byte array.
    :param input: The byte array.
    :type input: bytes
    :param index: The index to start reading from.
    :type index: int
    :param size: The size of the chunk to read.
    :type size: int
    :return: A tuple with the chunk read, and the integer and the next chunk.
    :rtype: Tuple[bytes, int]
    """
    bResult = None
    iResult = None
    if len(input) < index + size:
        bResult = int.from_bytes(input[index:], byteorder="big")
        iResult = len(input)
    else:
        bResult = int.from_bytes(input[index : index + size], byteorder="big")
        iResult = index + size

    return (bResult, iResult)


def read_key(bKey: bytes) -> Tuple[bytes, bytes]:
    """
    Reads the key header from a byte array.
    :param bKey: The key.
    :type bKey: bytes
    :return: The AES and HMAC pieces of the key.
    :rtype: Tuple[bytes, bytes]
    """
    if bKey[0:12] != b"\x00GITCRYPTKEY":
        raise ValueError(f"Invalid key: invalid preamble ({bKey[0:12]})")
    if bKey[12:16] != b"\x00\x00\x00\x02":  # version
        raise ValueError(f"Invalid key: invalid version ({bKey[12:16]})")
    key_name, header_size = read_key_header(bKey[16:])
    entries_section = bKey[16 + header_size :]
    entries = []
    pending_entries = True
    index = 0
    while True:
        aes_key, hmac_key, index = read_key_entry(entries_section, index)
        if aes_key is None:
            break
        else:
            entries.append((aes_key, hmac_key))
    result = (None, None)
    if len(entries) != 0:
        result = entries[0]

    return result


def read_key_header(bKey: bytes) -> Tuple[str, int]:
    """
    Reads the key header from a byte array.
    :param bKey: The key.
    :type bKey: bytes
    :return: A tuple with the key name and the index of the rest of the key.
    :rtype: Tuple[str, int]
    """
    iteration = 0
    offset = 0
    key_name = None
    while True:
        field_id, offset = read_be(bKey, offset)
        if field_id is None:
            raise ValueError(
                f"Invalid key: error reading 'field id' at offset {offset}"
            )
        if field_id == HEADER_FIELD_END:
            break
        field_len, offset = read_be(bKey, offset)
        if field_id == HEADER_FIELD_KEY_NAME:
            if field_len > KEY_NAME_MAX_LEN:
                raise ValueError(f"Invalid key: invalid key name length {field_len}")
            if field_len != 0:
                key_name, offset = read_be(bKey, offset, field_len)
        elif field_id & 1:
            raise ValueError(f"Invalid key: unknown field id {field_id}")
        else:
            _, offset = read_be(bKey, offset, field_len)
        iteration += 1

    return (key_name, offset)


def read_key_entry(bKey: bytes, offset: int) -> Tuple[bytes, bytes, int]:
    """
    Reads the key entry from a byte array.
    :param bKey: The key.
    :type bKey: bytes
    :param offset: The initial offset.
    :type offset: int
    :return: The AES and HMAC pieces of the key, and the next offset.
    :rtype: Tuple[bytes, bytes, int]
    """
    iteration = 0
    index = offset
    aes_key = None
    hmac_key = None
    version = None
    while True:
        field_id, index = read_be(bKey, index)
        if index is None:
            return (None, None, None)
        if field_id is None:
            raise ValueError(f"Invalid key: error reading 'field id' at offset {index}")
        if field_id == KEY_FIELD_END:
            break
        field_len, index = read_be(bKey, index)
        if field_len is None:
            raise ValueError(
                f"Invalid key: error reading 'field len' at offset {index}"
            )
        if field_id == KEY_FIELD_VERSION:
            if field_len != 4:
                raise ValueError(f"Invalid key: invalid version length {field_len}")
            version, index = read_be(bKey, index)
        elif field_id == KEY_FIELD_AES_KEY:
            if field_len != AES_KEY_LEN:
                raise ValueError(f"Invalid key: invalid AES key length {field_len}")
            aes_key = bKey[index : index + field_len]
            index += field_len
        elif field_id == KEY_FIELD_HMAC_KEY:
            if field_len != HMAC_KEY_LEN:
                raise ValueError(f"Invalid key: invalid HMAC key length {field_len}")
            hmac_key = bKey[index : index + field_len]
            index += field_len
        elif field_id & 1:
            raise ValueError(f"Invalid key: unknown field id {field_id}")
        else:
            if field_len > MAX_FIELD_LEN:
                raise ValueError(f"Invalid key: field too long {field_len}")
            index += field_len

    return (aes_key, hmac_key, index)


def compute_nonce(input: str, hmacKey: bytes) -> bytes:
    """
    Compute the deterministic nonce using HMAC-SHA1 of the file contents.
    :param input: The contents of the file as bytes.
    :type input: bytes
    :param hmacKey: The key for HMAC-SHA1.
    :type hmacKey: bytes
    :return: The first 16 bytes of the HMAC-SHA1 output as the nonce.
    :rtype: bytes
    """
    hmac_state = HmacSha1State(hmacKey)
    hmac_state.add(input)
    full_hmac = hmac_state.get()  # 20 bytes (HMAC-SHA1 output)
    return full_hmac[:12]  # First 16 bytes for AES-CTR nonce


def is_base64_encoded(s: str) -> bool:
    """
    Checks if a given string is valid base64-encoded data.
    :param s: The string to check.
    :type s: str
    :return: True if it's valid base64, False otherwise.
    :rtype: bool
    """
    try:
        # Decode and check if re-encoding matches the original (ignoring padding)
        decoded = base64.b64decode(s, validate=True)
        return base64.b64encode(decoded).decode().strip("=") == s.strip("=")
    except Exception:
        return False


def decrypt(encryptedText: str) -> str:
    """
    Decrypts a base64-encoded encrypted string.
    :param encryptedText: The base64-encoded ciphertext.
    :type encryptedText: str
    :return: The decrypted plaintext.
    :rtype: str
    """
    aes_key, hmac_key = get_key()

    encrypted_data = base64.b64decode(encryptedText)

    preamble = encrypted_data[:10]
    nonce = encrypted_data[10:22]

    aes = AesCtrDecryptor(aes_key, nonce + b"\x00\x00\x00\x00")
    hmac_state = HmacSha1State(hmac_key)

    actual_encrypted_data = encrypted_data[22:]

    plaintext = aes.process(actual_encrypted_data)
    hmac_state.add(plaintext)

    # Verify the HMAC against the stored nonce
    computed_nonce = compute_nonce(plaintext, hmac_key)
    if computed_nonce != nonce:
        raise ValueError(
            "Decryption failed: HMAC mismatch! ({nonce} != {computed_nonce})"
        )

    return plaintext.decode("utf-8")


def encrypt(plaintext: str) -> str:
    """
    Encrypts a plaintext string.
    :param plaintext: The plaintext to encrypt.
    :type plaintext: str
    :return: The encrypted text in base64 format.
    :rtype: str
    """
    aes_key, hmac_key = get_key()  # Get AES and HMAC keys

    # Convert plaintext to bytes
    plaintext_bytes = plaintext.encode("utf-8")

    # Compute nonce (first 12 bytes of HMAC-SHA1 of plaintext)
    nonce = compute_nonce(plaintext_bytes, hmac_key)

    # AES-CTR requires a 16-byte nonce, so extend it with four zero bytes
    extended_nonce = nonce + b"\x00\x00\x00\x00"

    # Initialize AES-CTR encryptor
    aes = AesCtrEncryptor(aes_key, extended_nonce)
    hmac_state = HmacSha1State(hmac_key)

    # Encrypt the plaintext
    ciphertext = aes.process(plaintext_bytes)

    # Compute HMAC of plaintext for verification
    hmac_state.add(plaintext_bytes)

    # Construct encrypted data: preamble + nonce + ciphertext
    return b"\x00GITCRYPT\x00" + nonce + ciphertext


class AesCtrDecryptor:
    def __init__(self, key, nonce):
        """
        Initialize the AES-CTR decryptor with the given key and nonce.
        :param key: AES key (bytes)
        :param nonce: Nonce for AES-CTR (bytes)
        """
        self.cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
        self.decryptor = self.cipher.decryptor()

    def process(self, data):
        """
        Decrypt data using AES-CTR.
        :param data: The ciphertext to decrypt (bytes)
        :return: Decrypted plaintext (bytes)
        """
        return self.decryptor.update(data)


class AesCtrEncryptor:
    def __init__(self, key, nonce):
        """
        Initialize the AES-CTR encryptor with the given key and nonce.
        :param key: AES key (bytes)
        :param nonce: Nonce for AES-CTR (bytes)
        """
        self.cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
        self.encryptor = self.cipher.encryptor()

    def process(self, data):
        """
        Decrypt data using AES-CTR.
        :param data: The ciphertext to decrypt (bytes)
        :return: Decrypted plaintext (bytes)
        """
        return self.encryptor.update(data)


class HmacSha1State:
    LEN = 20  # SHA-1 digest length (160 bits)

    def __init__(self, key):
        """
        Initialize the HMAC-SHA1 state with the given key.
        :param key: HMAC key
        :type key: bytes
        """
        self.hmac = hmac.HMAC(key, hashes.SHA1())

    def add(self, data: bytes):
        """
        Add data to the HMAC calculation.
        :param data: Data to add to HMAC
        :type data: bytes
        """
        self.hmac.update(data)

    def get(self) -> bytes:
        """
        Finalize and return the HMAC digest.
        :return: HMAC digest.
        :rtype: bytes
        """
        return self.hmac.finalize()
