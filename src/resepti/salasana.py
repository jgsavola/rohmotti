#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import struct
import binascii
import hashlib
import re

def hash_password(plaintext_password, salt=None):
    if salt is None:
        salt = generate_random_salt()

    hashed_hex = hashlib.sha1(salt + plaintext_password).hexdigest()

    return salt + '$' + hashed_hex

def get_salt_from_hash(hashed_password):
    """Erota ja palauta $-merkillä erotettu suola salasanasta."""

    m = re.match('^([\da-f]+)\\$', hashed_password)

    return m.group(1)

def generate_random_salt():
    """Generate 64 pseudorandom bits and encode them as a hex string.
       This should be probably enough for salting passwords."""

    return binascii.hexlify(struct.pack('!Q', random.getrandbits(64)))
