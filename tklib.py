#!/usr/bin/python

from html.parser import HTMLParser
import urllib.request, urllib.error, urllib.parse
import sys

__all__ = ["tk_search"]

def tk_search(keyword):
    TK_URL = 'http://www.torrentkitty.com/search/'
    parser = TorrentKittyParser()

    uri = urllib.parse.urljoin(TK_URL,urllib.parse.quote(keyword))
    request = urllib.request.Request(uri)
    opener = urllib.request.build_opener(SmartRedirectHandler())
    opener.addheaders = [('User-agent', 'Mozilla')]
    f = opener.open(request)
    parser.feed(str(f.read(), "utf8"))

    nn = len(parser.names)
    nl = len(parser.links)
    n = max(nn, nl)

    results = list()
    for i in range(n):
        name = parser.names[i] if i<nn else None
        link = parser.links[i] if i<nl else None
        results.append((name, link))
    return results


# create a subclass and override the handler methods
class TorrentKittyParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)

        self.nameStart = False
        self.names = list()
        self.links = list()

    def handle_starttag(self, tag, attrs):
        if tag == "td":
            for k, v in attrs:
                if k == "class" and v == "name":
                    self.nameStart = True
                    break
        elif tag == "a":
            href = ""
            found = False
            for k, v in attrs:
                if k == "rel" and v=="magnet":
                    found = True
                elif k == "href":
                    href = v
            if found and href:
                self.links.append(href)

    def handle_endtag(self, tag):
        if self.nameStart:
            self.nameStart = False

    def handle_data(self, data):
        if self.nameStart:
            self.names.append(data)

class SmartRedirectHandler(urllib.request.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        result = urllib.request.HTTPRedirectHandler.http_error_301(
            self, req, fp, code, msg, headers)
        result.status = code
        return result

    def http_error_302(self, req, fp, code, msg, headers):
        result = urllib.request.HTTPRedirectHandler.http_error_302(
            self, req, fp, code, msg, headers)
        result.status = code
        return result

if __name__ == "__main__":
    # for test
    # f = file("MIDD-962.html")

    keyword = ""
    if len(sys.argv)>=2:
        keyword = sys.argv[1]

    results = tk_search(keyword)

    for _, link in results:
        print(link)
        break
