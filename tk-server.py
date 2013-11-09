#!/usr/bin/python

import os
from bottle import run, route, view, request
import tklib

@route('/')
@view('index.html')
def index():
    return dict(results=[], keyword="")

@route('/search', method='POST')
@view('index.html')
def search():
    keyword = request.forms.keyword
    results = tklib.tk_search(keyword)
    return dict(results=results, keyword=keyword)

if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True)