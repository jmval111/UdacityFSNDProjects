# Overview
Goal of this project is to take a baseline installation of a Linux distribution on a virtual machine and prepare it to host WSGI web applications, to include installing updates, securing it from a number of attack vectors and installing/configuring web and database servers.

# Contents
- [Amazon LightSail](#amazon-lightsail)
  - [LightSail Instance Setup](#lightsail-instance-setup)
- [IP address and SSH port](#ip-address-and-ssh-port)
- [Hosted Apps URL](#hosted-apps-url)
- [Software Installed](#software-installed)
- [Configuration Changes](#configuration-changes)
  - [Update software](#update-software)
  - [New Linux User](#new-linux-user)
  - [Generate ssh key](#generate-ssh-key)
  - [Disable password based login](#disable-password-based-login)
  - [Firewall Setup](#firewall-setup)
  - [Clone Projects](#clone-projects)
  - [Setup to host app](#setup-to-host-app)
  - [Additional steps for apps](#additional-steps-for-apps)
  - [Set localtimezone to UTC](#set-localtimezone-to-utc)


# Amazon LightSail
This project uses virtual private server (Ubuntu instance) provided by Amazon LightSail.
[Reference](https://amazonlightsail.com)

## LightSail Instance Setup
1. Sign up
2. Create Instance
3. Select Platform > Linux/Unix
4. Select a blueprint > OS Only> Ubuntu
5. download default key pair
6. Name your Instance
Wait for it to start up <br>
Once your instance has started up, you can log into it with SSH from your browser.<br>
The public IP address of the instance is displayed along with its name.[Lightsail document to connect using putty](https://lightsail.aws.amazon.com/ls/docs/how-to/article/lightsail-how-to-set-up-putty-to-connect-using-ssh)

# IP address and SSH port
Server IP: 35.154.170.92,
SSH PORT: 2200

# Hosted Apps URL
* [Simple home page](http://35.154.170.92/), includes link to other two apps.
* [Item Catalog App](http://35.154.170.92/itemcatalog), Flask Web App
* [Nearby Restaurants](http://35.154.170.92/searchRestaurants]), static single page app

# Software Installed
python3, finger, postgresql, postgresql-contrib, apache2,
libapache2-mod-wsgi-py3,python-pip,flask, packaging, oauth2client, flask-httpauth,sqlalchemy, flask-sqlalchemy, psycopg2, bleach, requests, git, ntp

# Configuration Changes
## Update software
```
sudo apt-get update
sudo apt-get upgrade
```

## New Linux User
Create a new user **grader** with sudo access and forced key authentication.
```
sudo adduser grader
sudo cp /etc/sudoers.d/90-cloud-init-users /etc/sudoers.d/grader
sudo chmod 600 /etc/sudoers.d/grader
sudo vi /etc/sudoers.d/grader
sudo chmod 400 /etc/sudoers.d/grader
```
#### Inside /etc/sodoers.d/grader
grader ALL=(ALL) NOPASSWD:ALL

## Generate ssh key
* Generated ssh keys using `ssh-keygen` in windows cmd.
* Copied the public key file to `/home/grader/.ssh/authorized_keys` on the server.

## Disable password based login
* `sudo vi /etc/ssh/sshd_config`
* Set `PasswordAuthentication no`
* restart ssh service with `sudo service ssh restart`

## Change ssh port
```
sudo vi /etc/ssh/sshd_config
Port 2200
sudo service ssh restart
```

## Disable root login
```
sudo vi /etc/ssh/sshd_config
PermitRootLogin no
/etc/init.d/sshd restart
```
# Firewall Setup
**Note:** Amazon LightSail offers easy way to control port access via Instance Network Management (Networking>Firewall). Following steps are to be taken where such management is not available.
## block all incoming requests
```
sudo ufw default deny incoming
sudo ufw default allow outgoing
```
**warning!** don't activate firewall yet or you will be completely blocked

## allow what we need
```
sudo ufw allow 2200/tcp
sudo ufw allow www
sudo ufw allow 123/tcp
```

## enable firewall
```
sudo ufw enable
sudo ufw status
```

## Postgres database Setup
```
sudo su - postgres
sudo su postgres -c 'createuser -DRSP itemcatalog'
psql
\password itemcatalog
create database catalog with owner itemcatalog;
```

## Clone projects
**Note:** Placing in non-root directory of apache will prevent http access to un-intended files.
```
cd /var/www/
git clone https://github.com/vbhosle/UdacityFSNDProjects.git
```

## Setup to host app
Create .wsgi file: /var/www/itemCatalogApp.wsgi with following details
```
import sys
sys.path.insert(0,'/var/www/html/UdacityFSNDProjects/itemCatalog/')
from finalProject import app as application
application.secret_key = LONG_RANDOM_STRING
```
Add to apache config
```
cd /etc/apache2/sites-enabled
sudo vi 000-default.conf
WSGIScriptAlias /itemcatalog /var/www/itemCatalogApp.wsgi
Alias /searchRestaurants /var/www/UdacityFSNDProjects/NearbyRestaurantsMap
Alias /portfolio /var/www/html/PortfolioCustom
```
restart apache
`sudo apache2ctl restart`

## Additional steps for apps
* At https://console.developers.goolgle.com set **Authorized JavaScript origins** to http://35.154.170.92
* At https://console.developers.google.com set **key restrictions>http referrers** to the server's home page i.e. http://35.154.170.92 for the Google Maps API key.

* Update database connection URI in **itemCatalog/database_setup.py and finalProject.py**
* Replace API key placeholders with valid keys.
* Update the google_client_secret.json load path in **itemCatalog/finalProject.py**

## Set localtimezone to UTC:
**Note:** Amazon lightsail already had UTC
```
 ln -sf /usr/share/zoneinfo/UTC /etc/localtime
 ```
