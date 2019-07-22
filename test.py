import os
import sys
import urllib.request

from pkg_resources import parse_version


def calculate_client_info():  # pragma: no cover
    import hashlib
    import socket
    from getpass import getuser
    hashinfo = hashlib.sha256((socket.gethostname() + getuser()).encode())
    hashinfo = hashinfo.hexdigest()
    return hashinfo


def is_latest_version(version, client_info):  # pragma: no cover
    """check current version againt latest version"""
    try:
        url = ("http://localhost:8080/is_latest/?"
               "current_version={}&os={}&hash={}".format(
                version, sys.platform, client_info))
        res = urllib.request.urlopen(url, timeout=0.5)
        data = res.read()  # This will return entire content.

        if res.status != 200:
            return None, True
        if parse_version(data.decode()) > parse_version(version):
            return None, False
        else:
            return None, True
    except Exception as E:
        return E, True


def run():
    print(is_latest_version(os.getenv("VERSION"), calculate_client_info()))


if __name__ == "__main__":
    run()
