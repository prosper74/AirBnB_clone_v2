#!/usr/bin/env bash
# Sets up a web server for deployment of web_static.
# the frontend of the application

LOCATION="\\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n"

sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y install nginx
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared
echo "Testing Nginx config" | sudo tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -hR ubuntu:ubuntu /data/
sudo sed -i "35i $LOCATION" /etc/nginx/sites-available/default
sudo service nginx start
