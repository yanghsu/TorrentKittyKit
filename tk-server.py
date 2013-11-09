#!/usr/bin/python

try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import os
import subprocess
from bottle import run, route, view, request, redirect
import tklib


LX_PATH = "lx"

@route('/')
@view('index.html')
def index():
    return dict(results=[], keyword="")

@route('/search', method='POST')
def search():
    keyword = request.forms.keyword       # unicode
    redirect('/search/'+keyword.encode('utf8'))

@route('/search/<keyword>')
@view('index.html')
def search_get(keyword):
    results = tklib.tk_search(keyword)
    return dict(results=results, keyword=keyword)

@route('/xunlei-lixian', method='POST')
@view('lixian.html')
def xunlei_lixian():
    name = request.forms.name
    magnet = request.forms.magnet_link     # unicode
    anchor = request.forms.anchor          # unicode
    refer_url = request.get_header('referer') # unicode
    if anchor:
        refer_url = refer_url + '#' + anchor
    cmd = ' '.join([XL_PATH, 'add', magnet.encode('utf8')])
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    error = ''
    output = ''.join(p.stdout.readlines())
    if p.wait():
        error, output = output, error
    return dict(referer=refer_url, name=name, error=error, output=output)

if __name__ == '__main__':
    config = configparser.ConfigParser()
    try:
        config.read([os.path.expanduser(os.path.join('~', '.tk.conf'))])
    except configparser.Error:
        pass
    else:
        XL_PATH = os.path.expanduser(config.get('xl', 'path'))
    run(host='0.0.0.0', port=8080, debug=True)
