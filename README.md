# Linux Server Configuration Project
 This project takes the Udacity Catalog Project and configures it on an Amazon Lightsail Ubuntu web server. 

# IP Address
34.238.241.124

# URL to access the site 
http://34.238.241.124.xip.io/login
  - note: The website must be access via this xip.io url in order for OAuth to function. 

# Summary of Software installed
  - Python 2.7.12
  - sqlaclhemy
  - sqlalchemy.orm
  - BaseHTTPServer
  - oauth2client.client
  - httplib2
  - json
  - requests
  - PostgreSQL
  - apache2
  - mod_wsgi
  - git



# Summary of configurations made
  - /etc/apache2/sites-enabled/catalog.conf: The apache configuration file that configures the ip address of the server and directories containing site files. 
  - catalog.wsgi: Provides configuration for hosting python application on the server.
  - configured time zone to UTC.
  - configured key-based authentication for ubuntu and grader users on ubuntu server.  Disabled password login.
  - configured ssh port to 2200

# Third party resources used to complete the project
 - Udacity forums
 - Digital Ocean tutorials: 
    - https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps
    - https://www.digitalocean.com/community/tutorials/how-to-configure-the-apache-web-server-on-an-ubuntu-or-debian-vps

