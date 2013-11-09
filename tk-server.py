#!/usr/bin/python

import os
import subprocess
from bottle import run, route, view, request, redirect

import tklib

LX_EXEC = 'lx'

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
    magnet = request.forms.magnet_link     # unicode
    anchor = request.forms.anchor          # unicode
    refer_url = request.get_header('referer') # unicode
    if anchor:
        refer_url = refer_url + '#' + anchor

    output = ''
    retval = '0'
    lx_cmd = LX_EXEC + ' add ' + magnet.encode('utf8')
    p = subprocess.Popen(lx_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        output = output + line
    retval = p.wait()
    return dict(retval=retval, output=output, referer=refer_url, environ=os.environ)
    


if __name__ == '__main__':
    lx_exec = os.environ.get('LX_EXEC', None)
    if lx_exec is None:
        print "WARN: $LX_EXEC isn't properly set. Use default value ["+LX_EXEC+"]"
    else:
        LX_EXEC = lx_exec

    run(host='0.0.0.0', port=8080, debug=True)