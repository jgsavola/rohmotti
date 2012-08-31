#!/usr/bin/python

from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint, codepoint2name
import cgi

class CommentHTMLParser(HTMLParser):
    def __init__(self, ok_tags=[]):
        HTMLParser.__init__(self)

        self.output = ''
        self.ok_tags = dict(map(lambda tag: (tag, True), ok_tags))

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
    def handle_decl(self, data):
        pass

if __name__ == "__main__":
    ok_tags1 = []
    ok_tags2 = ['p', 'strong', 'pre', 'em', 'b', 'br', 'i', 'hr', 's', 'sub', 'sup', 'tt', 'u']

    html1 = '<p>Huippuvaarallinen <strong>tagisoppa</strong> <script>bad()</script></a>'
    expected1 = 'Huippuvaarallinen tagisoppa bad()'

    html2 = '<p>Huippuvaarallinen <strong>tagisoppa</strong> <script>bad()</script></a>'
    expected2 = '<p>Huippuvaarallinen <strong>tagisoppa</strong> bad()'

    parser1 = CommentHTMLParser(ok_tags1)
    parser1.feed(html1)
    output1 = parser1.output
    if output1 != expected1:
        print "fail1! output '%s', expected '%s'" % (output1, expected1)
    else:
        print "success1"

    parser2 = CommentHTMLParser(ok_tags2)
    parser2.feed(html2)
    output2 = parser2.output
    if output2 != expected2:
        print "fail2! output '%s', expected '%s'" % (output2, expected2)
    else:
        print "success2"
