import sys
import os
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

SOUNDBAR_ENDPOINT = os.getenv('SOUNDBAR_ENDPOINT')
SONGPAL = 'songpal'
POWER_ON = 'Power on'
APP_NAME = 'Songpal Remote'
ON = 'On'
OFF = 'Off'


class SongBarGui(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.statusLabel = QLabel(self)
        self.statusLabel.move(110, 125)

        self.button1 = QPushButton(self)
        self.button1.setText("Power On")
        self.button1.move(64, 32)
        self.button1.clicked.connect(self.poweron_button_clicked)

        self.button2 = QPushButton(self)
        self.button2.setText("Power Off")
        self.button2.move(64, 64)
        self.button2.clicked.connect(self.poweroff_button_clicked)

        self.button3 = QPushButton(self)
        self.button3.setText("Status")
        self.button3.move(64, 94)
        self.button3.clicked.connect(self.status_button_clicked)

        self.setGeometry(50, 50, 320, 200)
        self.setWindowTitle(APP_NAME)
        self.show()

    def status_button_clicked(self):
        stream = os.popen(f"{SONGPAL} --endpoint {SOUNDBAR_ENDPOINT} status")
        output = stream.read().split("\n")
        if output and output[0] == POWER_ON:
            status = ON
        else:
            status = OFF
        self.statusLabel.setText(status)

    def poweron_button_clicked(self):
        stream = os.popen(f"songpal --endpoint {SOUNDBAR_ENDPOINT} power on")
        output = stream.read()
        if output:
            self.statusLabel.setText(ON)

    def poweroff_button_clicked(self):
        stream = os.popen(f"songpal --endpoint {SOUNDBAR_ENDPOINT} power off")
        output = stream.read()
        if output:
            self.statusLabel.setText(OFF)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    SongBarGui = SongBarGui()
    sys.exit(app.exec_())
