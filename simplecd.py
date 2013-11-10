import argparse
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

def search(keyword):
    SIMPLE_SEARCH = "http://simplecd.me/search/entry/?%s"
    keyword = '"%s"' % '+'.join(keyword.split())
    query = urllib.parse.urlencode({'query':keyword})
    resp = urllib.request.urlopen(SIMPLE_SEARCH % query)
    soup = BeautifulSoup(resp.read())
    entries = soup.select('table.entry-list td.entry-info')
    results = []
    for entry in entries:
        href = entry.a['href']
        name = entry.a.string
        results.append((name, href))
    return results

def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def get(entry, keyword=None):
    SIMPLE_ENTRY = "http://simplecd.me/%s/"
    resp = urllib.request.urlopen(SIMPLE_ENTRY % entry)
    soup = BeautifulSoup(resp.read())
    entries = soup.select('div.emulemain td.post2')
    results = []
    for entry in entries:
        if entry.input is None:
            continue
        emule_id = entry.input['value']
        filesize = float(entry.input['filesize'])
        fname = entry.a.string
        if keyword is not None and fname.lower().find(keyword.lower()) == -1:
            continue
        results.append((fname, sizeof_fmt(filesize), emule_id))
    return results

def seeds(ids):
    SIMPLE_COPY = "http://simplecd.me/download/?%s"
    query = [('mode', 'copy')]
    for rid in ids:
        query.append(('rid', rid))
    query = '&'.join('='.join(kv) for kv in query)
    resp = urllib.request.urlopen(SIMPLE_COPY % query)
    soup = BeautifulSoup(resp.read())
    entries = soup.select('table#showall td')
    results = []
    for entry in entries:
        seed = entry.string.strip()
        results.append(seed)
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    search_parser = subparsers.add_parser('search')
    search_parser.add_argument('keyword')
    search_parser.set_defaults(func=lambda args: search(args.keyword))

    list_parser = subparsers.add_parser('list')
    list_parser.add_argument('--key')
    list_parser.add_argument('id')
    list_parser.set_defaults(func=lambda args: get(args.id, args.key))

    list_parser = subparsers.add_parser('seeds')
    list_parser.add_argument('id', nargs='+')
    list_parser.set_defaults(func=lambda args: seeds(args.id))

    args = parser.parse_args()
    results = args.func(args)
    for item in results:
        if type(item) == str:
            print(item)
        elif len(item) == 2:
            print('%s : %s' % item)
        elif len(item) == 3:
            print('%s (%s) : %s' % item)
        else:
            raise ValueError(item)
