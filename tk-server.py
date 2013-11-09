#!/usr/bin/python

import os
from bottle import run, route, view, request, redirect
import tklib

@route('/')
@view('index.html')
def index():
    return dict(results=[], keyword="")

@route('/search', method='POST')
def search():
    keyword = request.forms.keyword
    redirect('/search/'+keyword.encode('utf8'))

@route('/search/<keyword>')
@view('index.html')
def search_get(keyword):
    results = tklib.tk_search(keyword)
    return dict(results=results, keyword=keyword)

if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True)