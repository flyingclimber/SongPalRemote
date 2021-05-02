import sys
import os
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QMainWindow, QSlider
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt

SOUNDBAR_ENDPOINT = os.getenv('SOUNDBAR_ENDPOINT')
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

class SongBarGui(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.statusLabel = QLabel(self)
        self.statusLabel.move(110, 125)

        self.button_status = QPushButton(self)
        self.button_status.setText(STATUS)
        self.button_status.move(64, 32)
        self.button_status.clicked.connect(self.status_button_clicked)

        self.button_on = QPushButton(self)
        self.button_on.setText(ON)
        self.button_on.move(64, 64)
        self.button_on.clicked.connect(self.poweron_button_clicked)

        self.button_off = QPushButton(self)
        self.button_off.setText(OFF)
        self.button_off.move(64, 94)
        self.button_off.clicked.connect(self.poweroff_button_clicked)

        self.volumeSlider = QSlider(Qt.Horizontal, self)
        self.volumeSlider.setGeometry(30, 120, 100, 30)
        self.volumeSlider.valueChanged[int].connect(self.change_volume)

        self.setGeometry(50, 50, 320, 200)
        self.setWindowTitle(APP_NAME)
        self.status_button_clicked()
        self.show()

    def status_button_clicked(self):
        stream = os.popen(f"{SONGPAL} --endpoint {SOUNDBAR_ENDPOINT} status")
        output = stream.read()
        status = self.parse_status(output)

        self.power = ON if status.power else OFF
        self.volume = status.volume
        self.change_volume(status.volume)

        self.statusLabel.setText(self.power)

    def poweron_button_clicked(self):
        stream = os.popen(f"{SONGPAL} --endpoint {SOUNDBAR_ENDPOINT} power on")
        output = stream.read()
        if output:
            self.statusLabel.setText(ON)

    def poweroff_button_clicked(self):
        stream = os.popen(f"{SONGPAL} --endpoint {SOUNDBAR_ENDPOINT} power off")
        output = stream.read()
        if output:
            self.statusLabel.setText(OFF)

    def change_volume(self, val=0):
        self.volumeSlider.setValue(int(val))
        stream = os.popen(f"{SONGPAL} --endpoint {SOUNDBAR_ENDPOINT} volume {val}")
        output = stream.read()

    def parse_status(self, status):
        print(status)
        lines = status.split("\n")
        sb_status = SoundBarStatus()

        if lines and lines[0] == POWER_ON:
            sb_status.power = True
            sb_status.volume = lines[1].split(" ")[1].split("/")[0]
        else:
            sb_status.power = False
            sb_status.volume = lines[1].split(" ")[1].split("/")[0]

        return sb_status

if __name__ == '__main__':
    app = QApplication(sys.argv)
    SongBarGui = SongBarGui()
    sys.exit(app.exec_())
