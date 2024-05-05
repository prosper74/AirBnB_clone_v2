#!/usr/bin/python3
# Fabfile to generates a .tgz archive from the contents of web_static.
"""
Fabric script generates .tgz archive of all in web_static/ using func 'do_pack'
File name: web_static_<year><month><day><hour><minute><second>.tgz
"""

from time import strftime
from fabric.api import local


def do_pack():
    """generate .tgz archive of web_static/ folder"""
    timenow = strftime("%Y%M%d%H%M%S")
    try:
        local("mkdir -p versions")
        filename = "versions/web_static_{}.tgz".format(timenow)
        local("tar -cvzf {} web_static/".format(filename))
        return filename
    except (ValueError, IndexError):
        return None
