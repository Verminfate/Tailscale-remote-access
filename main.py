from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout,QFrame, QLineEdit, QFormLayout, QDialog, QDialogButtonBox)
from PyQt5.QtCore import QSettings, Qt  # Corrected import
from PyQt5.QtGui import QPalette, QColor
import sys
from datetime import datetime, timedelta
import pytz
import subprocess
import requests

settings = QSettings('VCX0', 'RMM')


def check_online_status(time_string):
    timestamp = datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%SZ")
    timestamp = timestamp.replace(tzinfo=pytz.UTC)
    current_time = datetime.now(tz=pytz.UTC)
    if current_time - timestamp < timedelta(seconds=5000):
        return "Online"
    else:
        return "Offline"

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.setFixedWidth(parent.width()) 

    def initUI(self):
        self.setWindowTitle('Settings')
        layout = QFormLayout(self)

        self.client_id_field = QLineEdit(self)
        self.client_secret_field = QLineEdit(self)
        self.client_tailnet_name_field = QLineEdit(self)

        self.client_id_field.setText(settings.value('client_id', ''))
        self.client_secret_field.setText(settings.value('client_secret', ''))
        self.client_tailnet_name_field.setText(settings.value('tailnet_name', ''))

        layout.addRow('Client ID:', self.client_id_field)
        layout.addRow('Client Secret:', self.client_secret_field)
        layout.addRow('Tailnet Name:', self.client_tailnet_name_field)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def accept(self):
        print(self.client_id_field.text(),self.client_secret_field.text(),self.client_tailnet_name_field.text())
        # Save the settings when OK is clicked
        settings.setValue('client_id', self.client_id_field.text())
        settings.setValue('client_secret', self.client_secret_field.text())
        settings.setValue('tailnet_name', self.client_tailnet_name_field.text())
        super().accept()


def grab_computer_data():
    OAUTH_CLIENT_ID = settings.value('client_id', '')
    OAUTH_CLIENT_SECRET = settings.value('client_secret', '')

    response = requests.post(
        "https://api.tailscale.com/api/v2/oauth/token",
        data={
            "client_id": OAUTH_CLIENT_ID,
            "client_secret": OAUTH_CLIENT_SECRET
        }
    )
    computers = {}

    No_response = {
        "Empty": {
            "IP": "Empty",
            "OS": "Empty",
            "Last Seen": "2023-11-19T23:46:46Z"
        }
    } 

    if response.status_code == 200:
        access_token = response.json().get('access_token')

        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        devices_response = requests.get(
            'https://api.tailscale.com/api/v2/tailnet/' + settings.value('tailnet_name', '') + '/devices',
            headers=headers
        )

        if devices_response.status_code == 200:
            devices = devices_response.json().get('devices', [])
            for device in devices:
                name = device.get('name').split('.')[0]
                ipv4 = [ip for ip in device.get('addresses', []) if not ip.startswith('fd7a:')][0]
                os = device.get('os')
                last_seen = device.get('lastSeen')

                computers[name] = {
                    "IP": ipv4,
                    "OS": os,
                    "Last Seen": last_seen
                }

            return computers
        else:
            print("Error fetching devices:", devices_response.status_code, devices_response.text)
    else:
        print("Error:", response.status_code, response.text)
        return No_response

computer_data = grab_computer_data()
print(computer_data)

class DeviceConnectApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.settings = QSettings()

    def refreshDevices(self):
        print(settings.allKeys())

    def initUI(self):
        self.setWindowTitle('VCX0-RMM')
        self.setGeometry(300, 300, 500, 300)  

   
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))  
        self.setPalette(palette)

        layout = QVBoxLayout()

        for index, (computer_name, info) in enumerate(computer_data.items(), start=1):
            ip = computer_data[computer_name]['IP']
            OS = computer_data[computer_name]['OS']
            method = "None"
            if(OS == "windows"):
                method = "RDP"
                OS = "Windows"
            if(OS == "linux"):
                method = "SSH"
                OS = "Linux"
            if(OS == "iOS"):
                method = "None"
                OS = "IOS"
            Last_Seen = computer_data[computer_name]['Last Seen']
            frame = QFrame()
            frame.setFrameShape(QFrame.StyledPanel)
            frame_layout = QHBoxLayout(frame)
            frame.setStyleSheet("background-color: #8c8c8c;")  

            status_layout = QHBoxLayout()
            status_layout.setSpacing(2)  
            status_layout.setContentsMargins(0, 0, 0, 0)

            name_label = QLabel(computer_name)
            ip_label = QLabel(ip)
            os_label = QLabel(OS)


            online_offline_box = QLabel("■")
            Last_Seen_Label = QLabel(check_online_status(Last_Seen))
            if Last_Seen_Label.text() == "Online":
                online_offline_box.setStyleSheet("QLabel { color: #00FF00; }")
            else:
                online_offline_box.setStyleSheet("QLabel { color: red; }")
            status_layout.addWidget(online_offline_box, alignment=Qt.AlignLeft)
            status_layout.addWidget(Last_Seen_Label, alignment=Qt.AlignLeft)
            status_container = QWidget()
            status_container.setLayout(status_layout)



            button = QPushButton('Connect')
            button.clicked.connect(lambda computer_name1=computer_name, ip=ip, m=method: self.connectDevice(computer_name1, ip, m))

            frame_layout.addWidget(name_label)
            frame_layout.addWidget(ip_label)
            frame_layout.addWidget(os_label)
            frame_layout.addWidget(status_container)
            frame_layout.addWidget(button)

            layout.addWidget(frame)


    
        bottom_layout = QHBoxLayout()

 
        refresh_button = QPushButton('Refresh')
        refresh_button.clicked.connect(self.refreshDevices) 

      
        settings_button = QPushButton('Settings')
        settings_button.clicked.connect(self.openSettings)

       
        for button in (refresh_button, settings_button):
            button.setStyleSheet("QPushButton { background-color: #8c8c8c; "
                                "border: none; "
                                "padding-top: 10px; padding-bottom: 10px; }")

      
        bottom_layout.addWidget(refresh_button)
        bottom_layout.addWidget(settings_button)

      
        layout.addLayout(bottom_layout)

        self.setLayout(layout)

    def connectDevice(self,computer_name1,ip,m):
        print(ip,m)
        if m == "SSH":
            exit
        elif m == "RDP":
            rdp_command = f"mstsc /v:{ip}"
            subprocess.run(["cmd", "/c", rdp_command], shell=True)
        elif m == "None":
            exit

    def openSettings(self):
        settings_dialog = SettingsDialog(self)
        if settings_dialog.exec_():
            print("Settings saved")
        else:
            print("Settings dialog cancelled")

app = QApplication(sys.argv)
ex = DeviceConnectApp()
ex.show()
sys.exit(app.exec_())