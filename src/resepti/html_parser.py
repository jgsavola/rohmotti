#!/usr/bin/python

from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint, codepoint2name
import cgi

class CommentHTMLParser(HTMLParser):
    def __init__(self, filename=None):
        HTMLParser.__init__(self)

        self.output = ''
        self.ok_tags = { 'p': 1,
                         'strong': 1,
                         'pre': 1,
                         'em' : 1,
                         'b' : 1,
                         'br' : 1,
                         'i' : 1,
                         'hr' : 1,
                         's' : 1,
                         'sub' : 1,
                         'sup' : 1,
                         'tt' : 1,
                         'u' : 1,
                         }

    def handle_starttag(self, tag, attrs):
        if self.ok_tags.get(tag) is None:
            return

        self.output += "<%s" % (tag,)
        for attr in attrs:
            self.output += " %s" % (attr[0])
            if attr[1] is not None:
                self.output += "=\"%s\"" % (cgi.escape(attr[1], True))

        self.output += ">"
    def handle_endtag(self, tag):
        if self.ok_tags.get(tag) is None:
            return

        self.output += "</%s>" % (tag,)
    def handle_data(self, data):
        self.output += data
    def handle_comment(self, data):
        pass
    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        self.output += "&%s;" % (name)
    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        print "Num ent  :", c
    def handle_decl(self, data):
        pass
