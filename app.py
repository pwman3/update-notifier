"""
Copyright Oz N Tiram <oz.tiram@gmail.com>

This file is distributed under the terms of the

  GNU AFFERO GENERAL PUBLIC LICENSE version 3.

"""

import datetime as dt
import json
import logging
import os
import time

from urllib.request import urlopen

import bottle
from peewee import SqliteDatabase


from bottle import request
from bottle_peewee import PeeweePlugin
from cachetools.func import ttl_cache
from peewee import Model, CharField, DateField


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    fh = logging.StreamHandler()
    fh.setLevel(logging.DEBUG)
    # add fh to logger
    logger.addHandler(fh)
    return logger


logger = get_logger('pwman3')

db = SqliteDatabase(os.getenv("PRODUCTION_DB", 'all.db'))

db_plugin = PeeweePlugin(db)

app = application = bottle.Bottle()


class User(Model):

    hashinfo = CharField()
    os = CharField()
    version = CharField()
    date = DateField()

    class Meta(object):
        database = db


app.install(db)


with db:
    db.create_tables([User], safe=True)


@ttl_cache(maxsize=2, ttl=3600, timer=time.time, typed=False)
def pypi_version():
    """check current version againt latest version"""
    logger.debug(
        "%s fetching ..." % dt.datetime.utcnow().strftime("%Y-%m-%d %H:%m"))
    pypi_url = "https://pypi.org/pypi/pwman3/json"
    try:
        res = urlopen(pypi_url, timeout=0.5)
        if res.status != 200:
            logger.debug("res: %s" % res.status)
            return 'x.x.x'

        info = json.loads(res.read().decode())
        return info['info']['version']
    except Exception as E:
        logger.warn("Exception: %s" % E)
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


if __name__ == "__main__":
    bottle.run(app)

