#!/usr/bin/python
'''
A basic app to return the latest pwman3 version
'''

import bottle

app = application = bottle.Bottle()

@app.route('/static/<filename:path>')
def static(filename):
    '''
    Serve static files
    '''
    return bottle.static_file(filename, root='./static')

@app.route('/')
def show_version():
    '''
    '''
    return '0.9.0'

