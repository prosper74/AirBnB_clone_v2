#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
"""
Fabric script method:
    do_deploy: deploys archive to webservers
"""

import os.path
from fabric.api import env, put, run
env.hosts = ['100.25.134.50', '54.87.235.110']


def do_deploy(archive_path):
    """Deploy archive to web server"""
    if os.path.isfile(archive_path) is False:
        return False
    try:
        filename = archive_path.split("/")[-1]
        no_ext = filename.split(".")[0]
        path_no_ext = "/data/web_static/releases/{}/".format(no_ext)
        symlink = "/data/web_static/current"
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(path_no_ext))
        run("tar -xzf /tmp/{} -C {}".format(filename, path_no_ext))
        run("rm /tmp/{}".format(filename))
        run("mv {}web_static/* {}".format(path_no_ext, path_no_ext))
        run("rm -rf {}web_static".format(path_no_ext))
        run("rm -rf {}".format(symlink))
        run("ln -s {} {}".format(path_no_ext, symlink))
        return True
    except (ValueError, IndexError):
        return False
