#!/usr/bin/python
# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
#from Crypto import Random
import random
import struct

class Sessio:
    def __init__(self, key):
        self.key = key

    def get_random_bytes(self):
        #return Random.get_random_bytes(16)
        return struct.pack('!QQ', random.getrandbits(64), random.getrandbits(64))

    def encrypt(self, plaintext):
        iv = self.get_random_bytes()
        aes = AES.new(self.key, mode=AES.MODE_CFB, IV=iv)

        padded_plaintext = plaintext.ljust((len(plaintext) + 15) / 16 * 16)

        ciphertext = aes.encrypt(padded_plaintext)

        return iv + ciphertext

    def decrypt(self, ciphertext):
        iv = ciphertext[0:16]
        aes = AES.new(self.key, mode=AES.MODE_CFB, IV=iv)

        plaintext = aes.decrypt(ciphertext[16:])

        return plaintext
