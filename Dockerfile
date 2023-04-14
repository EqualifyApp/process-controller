# Install base image
FROM alpine:latest



# Make port available to the world outside this container
# The port number is now set as an environment variable with a default value of 8083
ENV APP_PORT 8083

# Set up the proxy environment variables
ENV http_proxy http://192.168.1.15:18888
ENV https_proxy http://192.168.1.15:18888

EXPOSE $APP_PORT

# Define environment variable
ENV FLASK_APP axe.py