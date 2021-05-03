import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt, QTimer
from PyQt5 import uic

SOUNDBAR_ENDPOINT = os.getenv('SOUNDBAR_ENDPOINT')
STATUS_POLL_INTERVAL = 60000
SONGPAL = 'songpal'
POWER_ON = 'Power on'
APP_NAME = 'Songpal Remote'
ON = 'On'
OFF = 'Off'
STATUS = 'Status'


class SoundBarStatus():
    def __init__(self) -> None:
        self.power = OFF
        self.volume = 0

class SongPalGui(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi("SongPalLayout.ui", self)

        self.powerButton.clicked.connect(self.power_button_clicked)
        self.volumeDownButton.clicked.connect(lambda: self.step_volume(-1))
        self.volumeUpButton.clicked.connect(lambda: self.step_volume(+1))

        self.get_status()

        self.statusTimer = QTimer()
        self.statusTimer.timeout.connect(self.get_status)
        self.statusTimer.start(STATUS_POLL_INTERVAL)

        self.show()

    def get_status(self):
        stream = os.popen(f"{SONGPAL} --endpoint {SOUNDBAR_ENDPOINT} status")
        output = stream.read()
        status = self.parse_status(output)

        self.power = ON if status.power else OFF
        self.volume = status.volume
        self.update_volume_slider(self.volume)

        self.statusbar.clearMessage()
        self.statusbar.showMessage(self.power)

    def power_button_clicked(self):
        if self.power == ON:
            stream = os.popen(f"{SONGPAL} --endpoint {SOUNDBAR_ENDPOINT} power off")
        else:
            stream = os.popen(f"{SONGPAL} --endpoint {SOUNDBAR_ENDPOINT} power on")

        self.statusbar.showMessage(self.statusTextLabel)

    def step_volume(self, step):
        newVolume = self.volume + step
        self.update_volume_slider(newVolume)
        self.volume = newVolume
        stream = os.popen(f"{SONGPAL} --endpoint {SOUNDBAR_ENDPOINT} volume {newVolume}")

    def update_volume_slider(self, val):
       self.volumeSlider.setValue(int(val))

    def parse_status(self, status):
        print(status)
        lines = status.split("\n")
        sb_status = SoundBarStatus()

        sb_status.power = True if lines and lines[0] == POWER_ON else False
        sb_status.volume = int(lines[1].split(" ")[1].split("/")[0])

        return sb_status

if __name__ == '__main__':
    app = QApplication(sys.argv)
    SongPalGui = SongPalGui()
    sys.exit(app.exec_())
