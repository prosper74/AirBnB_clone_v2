#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives,
using the function do_clean

Methods:
    do_pack(): packs web_static/ files into .tgz archive
    do_deploy(archive_path): deploys archive to webservers
    deploy(): do_packs && do_deploys
    do_clean(n=0): removes old versions and keeps n (or 1) newest versions only
Usage:
    fab -f 3-deploy_web_static.py do_clean:n=2 -i my_ssh_private_key -u ubuntu
"""

import os.path
from time import strftime
from fabric.api import local, env, put, run
env.hosts = ['100.25.220.109', '100.25.199.2']


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


def deploy():
    """Check the deployment status of the application"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    success = do_deploy(archive_path)
    return success


def do_clean(number=0):
    """Clean up the archive directory to remove outdated files"""
    if number == 0:
        number = 1
    with cd.local('./versions'):
        local("ls -lt | tail -n +{} | rev | cut -f1 -d" " | rev | \
            xargs -d '\n' rm".format(1 + number))
    with cd('/data/web_static/releases/'):
        run("ls -lt | tail -n +{} | rev | cut -f1 -d" " | rev | \
            xargs -d '\n' rm".format(1 + number))
