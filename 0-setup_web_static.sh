#!/usr/bin/env bash
# This script sets up your web servers for the deployment of web_static.

# Update and upgrade the system
sudo apt-get update
sudo apt-get -y upgrade

# Install nginx
sudo apt-get -y install nginx

# Create necessary directories
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create a test index.html file
echo "Hello World Test!" > /data/web_static/releases/test/index.html

# Create a symbolic link to make 'test' the current version
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user and group
chown -R ubuntu:ubuntu /data/

# Configure Nginx to serve the static content
echo "server {
    listen 80;
    listen [::]:80;
    server_name _;
    location /hbnb_static {
        alias /data/web_static/current/;
        index index.html index.htm;
    }
}" > /etc/nginx/sites-available/default

# Restart nginx to apply new modifications
service nginx restart
