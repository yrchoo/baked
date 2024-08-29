
from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QTableWidgetItem, QPushButton,QListWidgetItem,QDialog
from PySide6.QtWidgets import QMessageBox, QHeaderView,QLabel,QVBoxLayout
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile , Qt,QSize,QTimer,Signal,Slot


from pprint import pprint

import shotgrid_total_profile
from shotgrid.user_env_val import Make_User_Data
import sys
from shotgun_api3 import shotgun


class Login(QWidget):
    def __init__(self, datas, parent=None):
        super().__init__(parent)
    
        self.datas = datas
        self.setup_ui()
        self.log_in()
    
    def log_in(self):

        self.ui.pushButton_enter.clicked.connect(self.insert_data)
        self.ui.pushButton_enter.clicked.connect(self.close_ui)
        
    def insert_data(self):

        name = self.ui.lineEdit_name.text(),
        shot = self.ui.lineEdit_shot.text(),
        task = self.ui.lineEdit_task.text(),
        asset = self.ui.lineEdit_asset.text()
        # data_list = [name,shot,task,asset]

    #샷그리드가 다운되었을경우 사용자가 직접 데이터 정보를 입력하고 sh 파일로 내보낸후 loader 연결.
    def close_ui(self):
        project = "baked" 
        name = self.ui.lineEdit_name.text()
        task = self.ui.lineEdit_task.text()
        shot = self.ui.lineEdit_shot.text()
        asset = self.ui.lineEdit_asset.text()
        #사용자 데이터 전달.
        Make_User_Data(name=name,project=project,shot=shot,asset=asset,task=task)
        self.close()
            
    def show_log_in_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

    def setup_ui(self):
        from ui_files.ui_Login import Ui_Form
        self.ui = Ui_Form()
        self.ui.setupUi(self)
       
if __name__ == "__main__":

    app = QApplication(sys.argv) 
    datas = []
    win = Login(datas)
    win.show()  
    app.exec()