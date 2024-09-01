
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtUiTools import QUiLoader
from shotgrid.user_env_val import Make_User_Data
from ui_files.ui_Login import Ui_Form
import sys

class Login(QWidget):
    def __init__(self):
        super().__init__()

        self.setup_ui()
        self.log_in()
    
    def log_in(self):

        self.ui.pushButton_enter.clicked.connect(self.login_loader)
        
    #샷그리드가 다운되었을경우 사용자가 직접 데이터 정보를 입력하고 sh 파일로 내보낸후 loader 연결.
    def login_loader(self):
        
        project = "baked" 
        name = self.ui.lineEdit_name.text()
        task = self.ui.lineEdit_task.text()
        shot = self.ui.lineEdit_shot.text()
        asset = self.ui.lineEdit_asset.text()
        
        #사용자 데이터 전달.
        Make_User_Data(name=name,project=project,shot=shot,asset=asset,task=task)
        self.close()
        

    def setup_ui(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
       
if __name__ == "__main__":

    app = QApplication(sys.argv) 
    win = Login()
    win.show()  
    app.exec()