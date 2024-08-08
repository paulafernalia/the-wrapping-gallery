# Dockerfile
FROM jwilder/nginx-proxy

# Copy the default virtual host configuration file
COPY vhost.d/default /etc/nginx/vhost.d/default

# Copy the custom nginx configuration file
COPY custom.conf /etc/nginx/conf.d/custom.conf