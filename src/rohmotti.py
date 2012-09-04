#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import pwd
import re
import psycopg2
import cgi
import cgitb
import Cookie
from string import Template

from db.DatabaseObject import DatabaseObject
from util.sessio import Sessio

handler_mapping = [[r'^/ruokaaine$',       'webapp.handlers.ruokaaine'],
                   [r'^/ruokaaine/\d+$',   'webapp.handlers.ruokaaine_1'],
                   [r'^/ruokaaine/\d+/kommentti$', 'webapp.handlers.kommentti'],
                   [r'^/ruokaaine/\d+/kommentti/\d+$', 'webapp.handlers.kommentti'],
                   [r'^/resepti$',         'webapp.handlers.resepti'],
                   [r'^/resepti/\d+$',     'webapp.handlers.resepti_1'],
                   [r'^/resepti/\d+/kommentti$', 'webapp.handlers.kommentti'],
                   [r'^/resepti/\d+/kommentti/\d+$', 'webapp.handlers.kommentti'],
                   [r'^/resepti/\d+/ruokaaine$', 'webapp.handlers.reseptiruokaaine'],
                   [r'^/resepti/\d+/ruokaaine/\d+$', 'webapp.handlers.reseptiruokaaine'],
                   [r'^/kuva',             'webapp.handlers.kuva'],
                   [r'^/kirjautuminen',    'webapp.handlers.kirjautuminen'],
                   [r'^/henkilo',          'webapp.handlers.henkilo'],
                   [r'^/haku',             'webapp.handlers.haku']]
template_mapping = [[r'^/ruokaaine$',      '/html_templates/ruokaaine.html_'],
                    [r'^/ruokaaine/\d+$',  '/html_templates/ruokaaine_1.html_'],
                    [r'^/resepti$',        '/html_templates/resepti.html_'],
                    [r'^/resepti/\d+$',    '/html_templates/resepti_1.html_'],
                    [r'^/kirjautuminen$',  '/html_templates/kirjautuminen.html_'],
                    [r'^/henkilo$',        '/html_templates/henkilo.html_'],
                    [r'^/henkilo/\d+$',    '/html_templates/henkilo_1.html_'],
                    [r'^/kuva/\d+$',       None],
                    [r'^/haku$',           '/html_templates/haku.html_'],
                    [r'^$',                '/html_templates/rohmotti.html_']]

def get_handler_name():
    path = re.sub(r'/[^/]+$', '', os.environ['SCRIPT_FILENAME'])

    for pair in handler_mapping:
        if re.match(pair[0], os.environ.get('PATH_INFO', '')):
            return pair[1]

def get_html_template_filename():
    path = re.sub(r'/[^/]+$', '', os.environ['SCRIPT_FILENAME'])

    for pair in template_mapping:
        if re.match(pair[0], os.environ.get('PATH_INFO', '')):
            if pair[1] is not None:
                return path + pair[1]

def import_module(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def main():
    cgitb.enable()

    form = cgi.FieldStorage()
    dbuser = pwd.getpwuid(os.getuid()).pw_name
    dbname = dbuser
    conn = psycopg2.connect("dbname=%s user=%s" % (dbname, dbuser))

    #
    # Setup database connection for the object model
    #
    DatabaseObject.setDatabaseConnection(conn)

    #
    # PUT, DELETE -tukikikka: jos lomakkeessa on 'method_override'
    # arvolla 'PUT' tai 'DELETE' ja käytetty kyselymetodi on POST,
    # tulkitse kyselymetodiksi 'method_override':n arvo.
    #
    request_method = os.environ.get('REQUEST_METHOD')
    if request_method == 'POST':
        method_override = form.getvalue('method_override')
        if method_override in ['PUT', 'DELETE']:
            request_method = method_override

    script_name = os.environ.get('SCRIPT_NAME', '')
    app_root_uri = re.sub(r'/src/rohmotti.py$', '', script_name)
    path_info = os.environ.get('PATH_INFO', '')
    full_path = script_name + path_info
    request_uri = os.environ.get('REQUEST_URI', '')
    remote_addr = os.environ.get('REMOTE_ADDR')
    http_x_forwarded_for = os.environ.get('HTTP_X_FORWARDED_FOR')

    if http_x_forwarded_for is not None:
        effective_remote_addr = http_x_forwarded_for
    else:
        effective_remote_addr = remote_addr

    conf = { 'request_method': request_method,
             'script_name': script_name,
             'app_root_uri': app_root_uri,
             'path_info': path_info,
             'full_path': full_path,
             'request_uri': request_uri,
             'remote_addr': remote_addr,
             'http_x_forwarded_for': http_x_forwarded_for,
             'effective_remote_addr': effective_remote_addr
             }

    html_template_filename = get_html_template_filename()

    C = Cookie.SimpleCookie()
    C.load(os.environ.get('HTTP_COOKIE', ''))
    sessio = Sessio.new_from_cookie(C)
    conf['sessio'] = sessio

    navigation = """\
        <span class="navigation">
            <ul class="navigation">
                <li class="navigation"><a id="rohmottinav" href="%(script_name)s"></a></li>
                <li class="navigation"><a href="%(script_name)s/resepti">Reseptit</a></li>
                <li class="navigation"><a href="%(script_name)s/ruokaaine">Ruoka-aineet</a></li>
                <li class="navigation"><a href="%(script_name)s/henkilo">Henkilöt</a></li>
                <li class="navigation"><a href="%(script_name)s/kirjautuminen">Kirjautuminen</a></li>
            </ul>
        </span>""" % conf

    render_dict = { 'REQUEST_URI': request_uri,
                    'APP_ROOT_URI': app_root_uri,
                    'FULL_PATH': full_path,
                    'navigation': navigation
                    }

    mode = 'development'

    module_to_load = get_handler_name()
    handler = None
    if module_to_load is not None:
        module = import_module(module_to_load)
        handler = module.Handler(form, conf)

    handler_return = None
    if handler is not None:
        try:
            handler_return = handler.render()
        except Exception:
            if mode == 'production':
                cgi.test()
            else:
                cgitb.handler()

        if handler_return is None:
            return

        render_dict.update(handler_return[1])
        sys.stdout.write('\r\n'.join(handler_return[0]) + '\r\n\r\n')
    else:
        #
        # Oletusotsakkeet
        #
        sys.stdout.write('Content-Type: text/html; charset=UTF-8\r\n\r\n')

    debug = False
    try:
        debug = form.getvalue('debug')
    except Exception:
        pass

    if html_template_filename is not None:
        if debug:
            print cgi.print_environ()

    if html_template_filename is not None:
        f = open(get_html_template_filename(), 'r')
        if f is None:
            print "Ei voinut avata tiedostoa!"
        html_template_string = f.read()
        s = Template(html_template_string)
        print s.safe_substitute(render_dict)

if __name__ == "__main__":
    main()
