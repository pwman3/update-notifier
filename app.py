"""
Copyright Oz N Tiram <oz.tiram@gmail.com>

This file is distributed under the terms of the

  GNU AFFERO GENERAL PUBLIC LICENSE version 3.

"""
    
import bottle
from bottle import request
import os
import datetime as dt
import logging

logging.basicConfig(filename='log.txt', format=logging.BASIC_FORMAT)

from bottle_peewee import PeeweePlugin
from peewee import Model, CharField, DateField
import peewee

db = PeeweePlugin('sqlite:///all.db')
app = application = bottle.Bottle()


class User(Model):

    hashinfo = CharField()
    os = CharField()
    version = CharField()
    date = DateField()

    class Meta(object):
        database = db.proxy

app.install(db)

try:
    db.database.create_table(User)
except peewee.OperationalError:
    pass


@app.route('/static/<filename:path>')
def static(filename):
    '''
    Serve static files
    '''
    return bottle.static_file(filename, root='./static')


@app.route('/is_latest/')
def show_version():
    '''
    '''
    hashinfo = request.GET.get("hash", "")
    user_os = request.GET.get("os", "")
    pwman_version = request.GET.get("current_version", "")
    date = dt.date.today()
    User.create(hashinfo=hashinfo, os=user_os, version=pwman_version, date=date)

    return '0.9.0'
