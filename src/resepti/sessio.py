#!/usr/bin/python
# -*- coding: utf-8 -*-

import base64
import Cookie
import math

from salaus import Salaus

class Sessio:
    """Yksinkertainen istunnonhallinta-toteutus Rohmutti-sovellusta
       varten. Istunnon tilaa hallitaan salakirjoitetun evästeen
       avulla."""

    SECRET_KEY = '2M\x93\x9a \x9d\x86zV\x04\xf3?\x08\x8a\xba7'
    salaus = Salaus(SECRET_KEY)

    def __init__(self, henkilo_id, start_timestamp, remote_addr):
        """Luo uusi istunto annetuilla parametreilla."""

        self.henkilo_id = henkilo_id
        self.start_timestamp = start_timestamp
        self.remote_addr = remote_addr

    def create_cookie(self):
        """Lue salakirjoitettu ja base64-koodattu eväste."""
        cookie_plaintext = str(self)

        C = Cookie.SimpleCookie()
        C["rohmotti"] = base64.b64encode(self.salaus.encrypt(cookie_plaintext))

        return C

    def delete_cookie(self):
        """Luo vanhentunut eväste, jonka asettamalla käyttäjän eväste häviää."""

        cookie_plaintext = str(self)

        C = Cookie.SimpleCookie()
        C["rohmotti"] = 'invalid'
        C["rohmotti"]["expires"] = 0

        return C

    @classmethod
    def new_from_cookie(cls, C):
        """Luo uusi sessio annetusta evästeestä."""

        try:
            encrypted_cookie_text = C['rohmotti']
        except KeyError:
            return

        cookie_text = cls.salaus.decrypt(base64.b64decode(encrypted_cookie_text.value))
        cookie_params = cookie_text.split(' ')

        cookie_dict = {}
        for param in cookie_params:
            kv = param.partition('=')
            cookie_dict[kv[0]] = kv[2]

        henkilo_id = int(cookie_dict['id'])
        start_timestamp = int(cookie_dict['start'])
        remote_addr = cookie_dict['ip']

        rohmotti = cookie_dict['rohmotti']

        return cls(henkilo_id=henkilo_id, start_timestamp=start_timestamp, remote_addr=remote_addr)

    def __str__(self):
        """Luo tekstimuotoinen esitys evästeestä."""

        return "id=%d ip=%s start=%d rohmotti" % (self.henkilo_id, self.remote_addr, self.start_timestamp)


if __name__ == "__main__":
    from sessio import Sessio
    s1 = Sessio(henkilo_id=999, start_timestamp=14135434, remote_addr='131.123.233.123')

    cookie = s1.create_cookie()
    print cookie

    s2 = Sessio.new_from_cookie(cookie)
    print s2
