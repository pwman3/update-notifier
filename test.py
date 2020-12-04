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
        url = (f"http://localhost:{os.getenv('APP_PORT', '8080')}/is_latest/?"
               f"current_version={version}&os={sys.platform}&hash={client_info}"
               )
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
    info = calculate_client_info()
    assert is_latest_version('0.13.1', info) == (None, True)
    assert is_latest_version('0.9.1', info) == (None, False)

if __name__ == "__main__":
    run()
