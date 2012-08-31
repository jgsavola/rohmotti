#!/usr/bin/python
# -*- coding: utf-8 -*-

from Crypto.Cipher import AES

class _RandomBytes:
    """Apuluokka satunnaisen alustusvektorin luomiseen. Vanhassa pgcryptossa
       ei ole modulia Crypto.Random, joten käytä standardikirjastom random-modulia."""

    #
    # Käytä mahdollisimman isoja sanankokoja satunnaisten bittien
    # generoimiseen.
    #
    _words = [(8, 'Q'), (4, 'I'), (2, 'H'), (1, 'B')]

    def __init__(self):
        try:
            from Crypto import Random
            self._Random = Random
        except ImportError:
            import random
            import struct

            self._random = random
            self._struct = struct

            self.__dict__['get_random_bytes'] = self._get_random_bytes_from_standard_library
        else:
            self.__dict__['get_random_bytes'] = self._get_random_bytes_from_pgcrypto

    def _get_random_bytes_from_pgcrypto(self, num_bytes):
        return self._Random.get_random_bytes(num_bytes)

    def _get_random_bytes_from_standard_library(self, num_bytes):
        """Tätä kömpelöä metodia käytetään, jos pgcrypton
           Crypto.Random.get_random_bytes ei ole olemassa."""

        # Käytä big-endian-järjestystä
        pack_string = '!'
        pack_args = []
        for word in self._words:
            while num_bytes >= word[0]:
                pack_string += word[1]
                pack_args.append(self._random.getrandbits(word[0]*8))
                num_bytes = num_bytes - word[0]
            if num_bytes == 0:
                break

        return self._struct.pack(pack_string, *pack_args)

class Salaus:
    """Salakirjoita ja pura AES:n avulla."""

    BLOCK_SIZE = 16

    def __init__(self, key):
        """Alusta salausluokka. Salaus tapahtuu annetulla avaimella,
        jonka pituuden täytyy olla BLOCK_SIZE."""

        self.key = key
        self.random_bytes = _RandomBytes()

    def encrypt(self, plaintext):
        """Salakirjoita selväteksti käyttäen satunnaista
           alustusvektoria ja palauta saatu salateksti yhdessä
           alustusvektorin kanssa. Alustusvektori on palautusarvon BLOCK_SIZE
           ensimmäistä tavua.

           Selväteksti täydennetään välilyönneillä niin, että sen
           pituus on jaollinen BLOCK_SIZE:lla."""

        iv = self.random_bytes.get_random_bytes(self.BLOCK_SIZE)
        aes = AES.new(self.key, mode=AES.MODE_CFB, IV=iv)

        padded_length = (len(plaintext) + self.BLOCK_SIZE - 1) / self.BLOCK_SIZE * self.BLOCK_SIZE
        padded_plaintext = plaintext.ljust(padded_length)

        ciphertext = aes.encrypt(padded_plaintext)

        return iv + ciphertext

    def decrypt(self, ciphertext):
        """Pura salateksti käyttäen salatekstin ensimmäistä BLOCK_SIZE
           tavua alustusvektorina."""

        iv = ciphertext[0:self.BLOCK_SIZE]
        aes = AES.new(self.key, mode=AES.MODE_CFB, IV=iv)

        plaintext = aes.decrypt(ciphertext[self.BLOCK_SIZE:])

        return plaintext
