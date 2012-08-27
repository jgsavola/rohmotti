#!/usr/bin/python

import sys
sys.path.insert(0, 'resepti')

import os
import pwd
import re
import psycopg2
import json
import cgi
import cgitb
from string import Template
from Ruokaaine import Ruokaaine, RuokaaineFactory

handler_mapping = [[r'^/ruokaaine',        'ruokaaine'],
                   [r'^/kuva',             'kuva']]
template_mapping = [[r'^/ruokaaine$',      '/resepti/ruokaaine.html_'],
                    [r'^/ruokaaine/\d+$',  '/resepti/ruokaaine_1.html_'],
                    [r'^/kuva/\d+$',       None]]

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

#    return path + '/resepti' + os.environ.get('PATH_INFO', '') + ".html_"
#    return re.sub(r'\.py$', r'.html_', os.environ['SCRIPT_FILENAME'])

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

    debug = form.getvalue('debug')

    path_info = os.environ.get('PATH_INFO', '')
    request_uri = os.environ.get('REQUEST_URI', '')
    #module_to_load = re.sub(r'^/([^/]+).*', r'\1', path_info)
    module_to_load = get_handler_name()

    
    conf = {'path_info': path_info, 'request_uri': request_uri}

    html_template_filename = get_html_template_filename()
    if html_template_filename is not None:
        print "Content-Type: text/html; charset=UTF-8\r\n\r\n"

        if debug:
            print cgi.print_environ()

    # print "path_info: %s" % (path_info)
    # print "handler_name: %s" % (module_to_load)
    # print "template_name: %s" % (get_html_template_filename())

    module = import_module(module_to_load)
    handler = module.Handler(conn, form, conf)

    render_dict = { 'REQUEST_URI': request_uri }

    render_dict.update(handler.render())

    if html_template_filename is not None:
        f = open(get_html_template_filename(), 'r')
        if f is None:
            print "Ei voinut avata tiedostoa!"
        html_template_string = f.read()
        s = Template(html_template_string)
        print s.safe_substitute(render_dict)

if __name__ == "__main__":
    main()
