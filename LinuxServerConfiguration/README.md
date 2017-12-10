i. The IP address and SSH port so your server can be accessed by the reviewer.
ii. The complete URL to your hosted web application.
iii. A summary of software you installed and configuration changes made.
iv. A list of any third-party resources you made use of to complete this project.

Locate the SSH key you created for the grader user.
During the submission process, paste the contents of the grader user's SSH key into the "Notes to Reviewer" field.
# Amazon Lightsail
## About
## Setup
Sign up
Create Instance
Select Platform > Linux/Unix
Select a blueprint > OS Only> Ubuntu
download default key pair
Name your Instance
Ubuntu-512MB-Udacity-1

Wait for it to start up

Once your instance has started up, you can log into it with SSH from your browser.

The public IP address of the instance is displayed along with its name. In the above picture it's 35.154.170.92. The DNS name of this instance is ec2-54-84-49-254.compute-1.amazonaws.com.

Start PuTTYgen (for example, from the Start menu, choose All Programs, PuTTY, PuTTYgen).

Choose Load.

https://lightsail.aws.amazon.com/ls/docs/how-to/article/lightsail-how-to-set-up-putty-to-connect-using-ssh

By default, PuTTYgen displays only files with the .ppk extension. To locate your .pem file, select the option to display files of all types.

Choose lightsailDefaultKey.pem, and then press Open.

PuTTYgen confirms that you successfully imported the key, and then you can choose OK.

Choose Save private key, and then confirm you don't want to save it with a passphrase.

If you choose to create a passphrase as an extra measure of security, remember you will need to enter it every time you connect to your instance using PuTTY.

Specify a name(lightsailPK) and a location to save your private key, and then choose Save.

Close PuTTYgen.

# Installed softwares

# Summary of Configurations

# Installed apps details
## Item Catalog
## About app
## Access Details

### Update available package list
sudo apt-get update

### Upgrade install packages
sudo apt-get upgrade

sudo apt-get install finger
### Add user
sudo adduser grader
fullname: udacity grader user

password: udacitylambda
confirm with finger user

finger grader

### Connect as grader
ssh grader@35.154.170.92 -p 22
