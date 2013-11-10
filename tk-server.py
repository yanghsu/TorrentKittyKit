#!/usr/bin/python
# -*- coding: utf-8 -*-

import configparser
import os
import subprocess
from bottle import run, route, view, request, redirect
import urllib.parse
import tklib


LX_PATH = "lx"

@route('/')
@view('index.html')
def index():
    return dict(results=[], keyword="")

@route('/search', method='POST')
def search():
    query = request.forms.keyword       # unicode
    redirect('/search?'+urllib.parse.urlencode({'q':query}))

@route('/search', method='GET')
@view('index.html')
def search_get():
    keyword = request.query.q
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
    cmd = ' '.join([LX_PATH, 'add', magnet])
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    error = ''
    output = ''.join(line.decode('utf-8') for line in p.stdout.readlines())
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
        LX_PATH = os.path.expanduser(config.get('lx', 'path'))
    run(host='0.0.0.0', port=8080, debug=True)
