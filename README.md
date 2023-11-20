# How it works
Tailscale is a very easy to setup VPN that lets you connect all of your devices together. I use Tailscale on all of my computers and wanted a way to easily connect to any of them remotely. I created a simple python script that uses the Tailscale API to get a list of devices and check if they are online, there are currently a lot of issues with the script and this is very basic and needs to be built out more.

# Setup/Install
Download all code as a .zip
Open a command prompt window and navigate to the files you downloaded
execute "pip install -r requirements.txt"
after that finishes execute "python main.py"
After the window opens it should look just like this

![image](https://github.com/Verminfate/Tailscale-remote-access/assets/72428571/eb96e62b-0645-4003-86e9-fa081108749e)

Next navigate to https://login.tailscale.com/admin/settings/oauth
Click on "Generate OAuth Client"
The client only needs Read permissions for Devices but I prefer to give it all permissions to avoid possible issues
Back in the program that you opened click "Settings"
Fill out the Client ID and Client Secret with the information from the Tailscale webpage
The Tailnet Name field also needs to be filled out, the name of your tailnet is located at the top of the admin webpage
For example my tailnet name is vcx0.com

![image](https://github.com/Verminfate/Tailscale-remote-access/assets/72428571/1632b14e-f9dd-4b67-961f-9f174903c310)

Click "Ok"
Close the app and run the same python command to open it again
After opening it should look something like this, Note the red rectangle is to protect my machines IP's and hostnames

![image](https://github.com/Verminfate/Tailscale-remote-access/assets/72428571/0d4a9c1a-2b17-45ea-97f5-d95c2fffad6d)
