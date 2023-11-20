## How it works
Tailscale is a very easy to setup VPN that lets you connect all of your devices together. I use Tailscale on all of my computers and wanted a way to easily connect to any of them remotely. I created a simple python script that uses the Tailscale API to get a list of devices and check if they are online, there are currently a lot of issues with the script and this is very basic and needs to be built out more.

## Setup / Install
* Click the green **Code** button at the top of the screen
* Extract the **zip** file that is downloaded
* Open a command prompt in that folder
* Execute `pip install -r requirements.txt`
* Execute `python main.py`
* A new window should open that looks like this

 ![image](https://github.com/Verminfate/Tailscale-remote-access/assets/72428571/ad3f2896-4658-4eac-944f-b42e39cec368)

* Click on **Settings**
* Open this url in your web browser https://login.tailscale.com/admin/settings/oauth
* Click **Generate OAuth Client**
* Give the client Read permissions to everything
* Copy the Client ID and Client Secret into the Settings window
* Your Tailnet name will show on the top left of the admin panel (example)
 ![image](https://github.com/Verminfate/Tailscale-remote-access/assets/72428571/2169a42d-8d36-4a2c-8351-365b70c8457f)

* Click **Ok**
* Close the app and run the same python command `python main.py` to re-open the program
* The program should be working now
