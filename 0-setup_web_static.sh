#!/usr/bin/env bash
# This script sets up your web servers for the deployment of web_static.
# It does the following:
# - Install nginx
# - Create some directories
# - Display a test page
# - Create a symbolic link
# - Give the ubuntu user ownership of a directory
# - Update the Nginx configuration to serve the static files
# - Restart the nginx service

# Update and upgrade the system
sudo apt-get -y update && sudo apt-get -y upgrade

# Install nginx
sudo apt-get -y install nginx

# Create required directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Display a test page
sudo bash -c 'echo "Hello from ALX" | tee /data/web_static/releases/test/index.html > /dev/null'

# Create a symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give the ubuntu user ownership of the /data/ directory
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the static files from the /hbnb_static/ location
if ! grep -q "^location /hbnb_static/" /etc/nginx/sites-available/default; then
    sudo sed -i '/^server {/a \ \n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default
fi

# Restart the nginx service
sudo service nginx restart