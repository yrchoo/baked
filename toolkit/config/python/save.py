try :
    from PySide6.QtWidgets import QApplication, QWidget, QTreeWidgetItem
    from PySide6.QtWidgets import QTreeWidget, QLabel, QHBoxLayout
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import QFile, Qt, Signal
    from PySide6.QtGui import QPixmap

except:
    from PySide2.QtWidgets import QApplication, QWidget, QTreeWidgetItem
    from PySide2.QtWidgets import QTreeWidget, QLabel, QHBoxLayout
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtCore import QFile, Qt, Signal
    from PySide2.QtGui import QPixmap

import os
import re

class SaveFile(QWidget):
    SAVE_FILE = Signal(str) # 파일이 저장될 때 파일을 저장할 경로를 내보내기 위한 시그널

    def __init__(self):
        super().__init__()

        self._set_init_val()
        self._set_ui()
        self._set_event()
        self._update_new_file_name()

    def _set_init_val(self, path):
        self.py_file_path = os.path.dirname(__file__)

        self.file_path = ""


    def _set_ui(self):
        ui_file_path = f"{self.py_file_path}/save.ui"
        ui_file = QFile(ui_file_path)
        ui_file.open(QFile.ReadOnly)

        ui_loader = QUiLoader()
        self.ui = ui_loader.load(ui_file, self)

        self.ui.setWindowFlags(Qt.WindowStaysOnTopHint)

        ui_file.close()

    def _set_event(self):
        self.ui.radioButton_version.toggled.connect(self._update_new_file_name)
        self.ui.lineEdit_tag.textChanged.connect(self._update_new_file_name)


    def save_file(self, path : str):
        self.show()


    def _update_new_file_name(self):
        name_label = self.ui.label_file_name
        file_name = self.file_path.split("/")[-1]

        if self.ui.radioButton_version.isChecked():
            self.ui.lineEdit_tag.setEnabled(False)
            parce = re.compile("[v]\d{3}")
            version = parce.search(self.file_path).group()
            new_version = "v%03d" % (int(version.split('v')[-1]) + 1)
            new_file_name = file_name.replace(version, new_version)
        else :
            self.ui.lineEdit_tag.setEnabled(True)
            tag_text = f"_{self.ui.lineEdit_tag.text()}"
            name, ext = os.path.splitext(file_name)
            new_file_name = f"{name}{tag_text}{ext}"

        name_label.setText(new_file_name)

    def _click_save_btn(self):
        new_file_name = self.ui.label_file_name
        dir_name = os.path.dirname(self.file_path)

        new_path = f"{dir_name}/{new_file_name}"

        self.SAVE_FILE.emit(new_path)




if __name__ == "__main__":
    app = QApplication()
    win = SaveFile()
    win.show()
    app.exec()