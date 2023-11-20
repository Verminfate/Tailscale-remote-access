## How it works
Tailscale is a very easy to setup VPN that lets you connect all of your devices together. I use Tailscale on all of my computers and wanted a way to easily connect to any of them remotely. I created a simple python script that uses the Tailscale API to get a list of devices and check if they are online, there are currently a lot of issues with the script and this is very basic and needs to be built out more.

## Setup / Install
* Click the green **Code** button at the top of the screen
* Click **Download ZIP**
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
* Copy the **Client ID** and **Client Secret** into the Settings window
* Your Tailnet name will show on the top left of the admin panel, for instance my Tailnet name is vcx0.com
 
  ![image](https://github.com/Verminfate/Tailscale-remote-access/assets/72428571/2169a42d-8d36-4a2c-8351-365b70c8457f)

* Click **Ok**
* Close the app and run the same python command `python main.py` to re-open the program
* The program should be working now

## Todo
* Store the value that decides if a machine is online/offline in the settings menu
* Have a first start menu that appears, that way we can avoid the "Empty" computer on first startup
* Get SSH working
* Compatability on Macosx
* Individual settings for each computer, that way you can select a connection method and username to connect with (I wont be doing this for passwords)
* Create a .exe that launches the python script silently (No command prompt window visible)

  
