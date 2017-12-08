# Item Catalog [Udacity Project]
## Overview
It is an web application that maintains categories and items for authorized users. It integrates third party OAuth for authentication. Authenticated users can post, edit and delete categories and items they own. Unauthenticated users can only view the categories and items of other users.

## Contents
- [Features](#features)
- [JSON Endpoints](#json-endpoints)
- [Technologies](#technologies)
- [Prerequisite](#prerequisite)
  - [Get Google OAuth Details](#get-google-oauth-details)
  - [Use Preconfigured VM](#use-preconfigured-vm) <br>
  OR
  - [Install required packages](#install-required-packages)
- [Project setup](#project-setup)
  - [Clone The Project](#clone-the-project)
  - [Database setup](#database-setup)
    - [Initialize database](#initialize-database)
    - [Populate database (Optional)](#populate-database)
  - [Place the OAuth details](#place-the-oauth-details)
  - [Change host and port (Optional)](#change-host-and-port)
  - [Start Flask Server](#start-flask-server)
- Attributions

# Features
- View categories and items added by all the users.
- Authentication through Google OAuth API.
- Only authenticated users can perform CRUD operations on the categories and items owned by them.
- All the data is persisted in sqlite database.
- It provides JSON endpoints for the data.

# JSON endpoints
### Get all categories:
GET URL: http://localhost:8100/categories/JSON

  <details>
    <summary>Response JSON</summary>
    <pre>
    {
    "Categories": [
      {
        "description": "Cricket is a bat-and-ball game played between two teams of eleven players",
        "id": 1,
        "name": "Cricket",
        "total_items": 4
      },
      {
        "description": "kicking a ball with the foot to score a goal",
        "id": 2,
        "name": "Soccer",
        "total_items": 2
      },
      {
        "description": "maneuver a ball or a puck into the opponent's goal using a hockey stick",
        "id": 3,
        "name": "Hockey",
        "total_items": 1
      }
    ]
  }
  </pre>
  </details>

### Get category with specific id:
GET URL : `http://localhost:8100/category/<int:category_id>/JSON`<br>
ex. http://localhost:8100/category/1/JSON

  <details>
    <summary>Response JSON</summary>
      <pre>
      {
        "Category": {
          "description": "Cricket is a bat-and-ball game played between two teams of eleven players",
          "id": 1,
          "name": "Cricket",
          "total_items": 4
        }
      }
    </pre>
  </details>

### Get all the items for a category id:
GET URL: `http://localhost:8100/category/<int:category_id>/items/JSON` <br>
ex. http://localhost:8100/category/1/items/JSON

  <details>
    <summary>Response JSON</summary>
      <pre>
        {
          "Items": [
            {
              "category": "Cricket",
              "description": "Cork covered by leather",
              "id": 1,
              "name": "ball"
            },
            {
              "category": "Cricket",
              "description": "thickly padded above the fingers and on the thumb of the hand",
              "id": 2,
              "name": "gloves"
            },
            {
              "category": "Cricket",
              "description": "cane handle attached to aflat - fronted willow - wood blade",
              "id": 3,
              "name": "bat"
            },
            {
              "category": "Cricket",
              "description": "includes webbing between the thumb and index fingers",
              "id": 4,
              "name": "Wicket-keeper's gloves"
            }
          ]
        }
    </pre>
  </details>

  ### Get an item with category_id and item_id:
  GET URL: `http://localhost:8100/category/<int:category_id>/item/<int:item_id>/JSON` <br>
  ex. http://localhost:8100/category/1/item/1/JSON

  <details>
    <summary>Response JSON</summary>
      <pre>
      {
        "Item": {
          "category": "Cricket",
          "description": "Cork covered by leather",
          "id": 1,
          "name": "ball"
        }
      }
      </pre>
  </details>

# Technologies
  **General:** Python, html, css <br>
  **Libraries/frameworks:** Flask, SQLAlchemy <br>
  **Authentication:** Google OAuth API
  **Database:** sqlite

# Prerequisite

## Get Google OAuth Details
1. Visit https://console.developers.google.com
2. Sign in with your Google - i.e. yourname@gmail.com. If you don't have one, you can go to accounts.google.com to create one for free.
3. https://console.developers.google.com lands you on a dashboard. Now create a new project with **Select Project >> + icon**

  <details>
    <summary>Dashboard Screenshot</summary>
    <img alt="dashboard" src="https://vbhosle.github.io/itemCatalogDoc/GoogleDevToolsDashboard.JPG">
  </details>
  
  <details>
    <summary>New Project Screenshot</summary>
    <img alt="new project" src="https://vbhosle.github.io/itemCatalogDoc/GoogleProject.JPG">
  </details>

4. Configure OAuth consent screen for project<br>
   **Credentials >> OAuth Consent Screen**<br>
   **Required fields:** Email address and Product name visbile to users

   <details>
     <summary>OAuth consent Screenshot</summary>
     <img alt="oauth consent" src="https://vbhosle.github.io/itemCatalogDoc/OauthConsent.JPG">
   </details>

5. Get OAuth Client ID<br>
  1. Goto **Credentials>>Create credentials>>OAuth Client ID**<br>
  2. Select **Application type: Web Application**<br>
  3. **Name of the app**<br>
  4. **Authorized Javascript Origins: http://localhost:8100**<br>
  5. **Authorized redirect URIs:http://localhost:8100**<br>
  6. Create!! Save this json as google_client_secret.json

  <details>
    <summary>Create Credentials Screenshot</summary>
    <img alt="create credentials" src="https://vbhosle.github.io/itemCatalogDoc/CreateCredentials.JPG">
  </details>
  
  <details>
    <summary>OAuth ClientID Screenshot</summary>
    <img alt="oauth clientid" src="https://vbhosle.github.io/itemCatalogDoc/OAuthClientID.JPG"><br>
    <img alt="download json" src="https://vbhosle.github.io/itemCatalogDoc/OAuthdownloadJson.JPG">
  </details>
  
  <details>
    <summary>Download JSON Screenshot</summary>
    <img alt="download json" src="https://vbhosle.github.io/itemCatalogDoc/OAuthdownloadJson.JPG">
  </details>



## Use Preconfigured VM

### Installing the Vagrant VM
We use a virtual machine (VM) to run a web server and a web app that uses it. The VM is a Linux system that runs on top of your own machine.  You can share files easily between your computer and the VM.

We're using the Vagrant software to configure and manage the VM. Here are the tools you'll need to install to get it running:

#### Git

If you don't already have Git installed, [download Git from git-scm.com.](http://git-scm.com/downloads) Install the version for your operating system.

On Windows, Git will provide you with a Unix-style terminal and shell (Git Bash).  
(On Mac or Linux systems you can use the regular terminal program.)

You will need Git to install the configuration for the VM. If you'd like to learn more about Git, [take a look at Udacity course about Git and Github](http://www.udacity.com/course/ud775).

#### VirtualBox

VirtualBox is the software that actually runs the VM. [You can download it from virtualbox.org, here.](https://www.virtualbox.org/wiki/Downloads)  Install the *platform package* for your operating system.  You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it.

**Ubuntu 14.04 Note:** If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center, not the virtualbox.org web site. Due to a [reported bug](http://ubuntuforums.org/showthread.php?t=2227131), installing VirtualBox from the site may uninstall other software you need.

#### Vagrant

Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem.  [You can download it from vagrantup.com.](https://www.vagrantup.com/downloads) Install the version for your operating system.

**Windows Note:** The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.

#### Run the virtual machine!
clone VM setup from https://github.com/udacity/fullstack-nanodegree-vm
Using the terminal, change directory to vagrant (**cd vagrant**), then type **vagrant up** to launch your virtual machine.
Now that you have Vagrant up and running type **vagrant ssh** to log into your VM.
When you want to log out, type **exit** at the shell prompt.  To turn the virtual machine off (without deleting anything), type **vagrant halt**. If you do this, you'll need to run **vagrant up** again before you can log into it.
Clone the projects in the shared directory **cd /vagrant**

## Install required packages
**Note:** Preconfigured VM steps takes care of installing following packages, if you are not using Preconfigured VM make sure you have following packages installed on ubuntu machine.

```
apt-get -qqy install python3 python3-pip
pip3 install --upgrade pip
pip3 install flask packaging oauth2client redis passlib flask-httpauth
pip3 install sqlalchemy flask-sqlalchemy psycopg2 bleach requests
```

# Project Setup
## Clone the project
cd into the directory you want to clone the repository. (cd to **/vagrant** directory if you followed Preconfigured VM steps)
Clone the repo with following command:<br>
`git clone https://github.com/vbhosle/UdacityFSNDProjects.git targetDirectory`

cd into `itemCatalog` directory

## Database Setup
cd into the `itemCatalog` project directory, where **database_setup.py** file is located.

### Initialize database
Execute **database_setup.py** file with the command `python database_setup.py` to initialize the database.
**itemcatalog.db** file will be created in the same directory.

### Populate database
**(Optional)**<br>
**Note:** Without this step, there is no data to display. It has to be added by authenticating user and create operation from the web app.<br>
**Note:** As app uses Google OAuth, please use only Google email id.<br>
Edit **populateCatalog.py**, put your Google mail id in place of **xyz@gmail.com**<br>
Execute  **populateCatalog.py** with the command `python populateCatalog.py` to populate the database with categories and items.

## Place the OAuth details
1. Replace existing google_client_secret.json with the json file obtained from Google developers account. Json file name has to be **google_client_secret.json**
2. In templates/login.html replace **CLIENT_ID** with the value of **client_id** field in json.

## Change host and port
**(optional)** <br>
You can edit the default host and port by editing the last line of the **finalProject.py** file. `app.run(host='0.0.0.0', port=8100)`
**Note:** While using vagrant make sure that you have your port set for port forwarding.<br>
ex. In following example, you can access the application using http://127.0.0.1:8180 port on the host machine.
```
Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-16.04-i386"
  config.vm.box_version = "= 2.3.5"
  config.vm.network "forwarded_port", guest: 8100, host: 8180, host_ip: "127.0.0.1"
```

## Start Flask Server
Execute **finalProject.py** with command **python finalProject.py** to run the Flask web server. In your browser visit `http://localhost:<port>` (default is http://localhost:8100) to view the item catalog  app.  You should be able login with your email id and view, add, edit, and delete items and categories.

# Attributions:
OAuth and CRUD code inspired by Udacity's repo https://github.com/udacity/ud330
