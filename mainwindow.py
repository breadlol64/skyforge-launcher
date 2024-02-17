# This Python file uses the following encoding: utf-8
import sys
import minecraft_launcher_lib as mll
import subprocess

from PySide6.QtWidgets import QApplication, QMainWindow

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow
import os


class MainWindow(QMainWindow):
    def set_status(self, status: str):
        print(status)


    def set_progress(self, progress: int):
        if current_max != 0:
            print(f"{progress}/{current_max}")
            self.ui.install_pb.setValue(progress)


    def set_max(self, new_max: int):
        global current_max
        current_max = new_max
        self.ui.install_pb.setMaximum(current_max)

    def inst_mc(self, ver:str):
        print("installing", ver)
        callback = {
            "setStatus": self.set_status,
            "setProgress": self.set_progress,
            "setMax": self.set_max
        }
        mll.install.install_minecraft_version(ver, "D:/mctest", callback=callback)
        print("installed")

    def launch_mc(self, ver:str, username:str):
        if not ver in os.listdir("D:/mctest/versions"):
            print("version", ver, "not installed")
            self.inst_mc(ver)
            self.ui.install_pb.setValue(0)

        minecraft_command = mll.command.get_minecraft_command(ver, "D:/mctest", {"username": username, "uuid": "", "token": ""})
        print("launching")
        subprocess.call(minecraft_command)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        for v in mll.utils.get_available_versions("D:/mctest"):
            self.ui.ver_box.addItem(v["id"])
        self.ui.launch_btn.clicked.connect(lambda: self.launch_mc(self.ui.ver_box.currentText(), self.ui.username_edit.text()))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
