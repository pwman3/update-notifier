"""
Copyright Oz N Tiram <oz.tiram@gmail.com>

This file is distributed under the terms of the

  GNU AFFERO GENERAL PUBLIC LICENSE version 3.

"""

import datetime as dt
import json
import logging
import time

from urllib.request import urlopen

import bottle
import peewee


from bottle import request
from bottle_peewee import PeeweePlugin
from cachetools.func import ttl_cache
from peewee import Model, CharField, DateField


logging.basicConfig(filename='log.txt', format=logging.BASIC_FORMAT)


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


@ttl_cache(maxsize=2, ttl=3600, timer=time.time, typed=False)
def pypi_version():
    """check current version againt latest version"""
    print("fetching...")
    pypi_url = "https://pypi.org/pypi/pwman3/json"
    try:
        res = urlopen(pypi_url, timeout=0.5)
        if res.status != 200:
            return 'x.x.x'

        info = json.loads(res.read())
        return info['info']['version']
    except Exception as E:
        return 'x.x.x'


@app.route('/')
def index():
    return """
<!DOCTYPE html>
    <head>
        <meta charset="utf-8">
        <title>Pwman3 Web</title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">
   </head>


<main>
</main>
<script type="text/javascript">
window.location.href="https://github.com/pwman3/pwman3";
</script>
</html>"""


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
    User.create(hashinfo=hashinfo, os=user_os, version=pwman_version,
                date=date)

    return pypi_version()
