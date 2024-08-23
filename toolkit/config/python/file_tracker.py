try :
    from PySide6.QtWidgets import QApplication, QWidget, QTreeWidgetItem
    from PySide6.QtWidgets import QTreeWidget, QLabel, QHBoxLayout
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import QFile, Qt, Signal
    from PySide6.QtGui import QPixmap

except:
    from PySide2.QtWidgets import QApplication, QWidget, QTreeWidgetItem
    from PySide2.QtWidgets import QTreeWidget, QLabel, QHBoxLayout
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtCore import QFile, Qt, Signal
    from PySide2.QtGui import QPixmap

import os
import time


class Tracker(QWidget):
    def __init__(self):
        super().__init__()
        self._set_instance_val()
        self._set_ui()

    def _set_instance_val(self):
        self.py_file_path = os.path.dirname(__file__)

    def _set_ui(self):
        ui_file_path = f"{self.py_file_path}/tracker.ui"
        ui_file = QFile(ui_file_path)
        ui_file.open(QFile.ReadOnly)

        ui_loader = QUiLoader()
        self.ui = ui_loader.load(ui_file, self)
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)

        ui_file.close()

    def _get_opened_file_list():
        pass

if __name__ == "__main__":
    app = QApplication()
    win = Tracker()
    win.show()
    app.exec()