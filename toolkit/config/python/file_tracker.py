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

# from webhook_server import WebhookServer # 서버를 시작하기

## 마야나 누크가 열릴 때 tracker 코드가 작동되게 하며 메뉴바를 통해서 유아이를 열게 한다

try :
    from shotgrid.get_shotgrid_data import Shotgrid_Data
except:
    pass

class Tracker(QWidget):
    def __init__(self, sg : Shotgrid_Data = None):
        super().__init__()
        self._set_instance_val(sg)
        self._set_ui()

        self._test_exec()

    def _test_exec(self):
        self._get_opened_file_list()

    def _set_instance_val(self, sg):
        self.py_file_path = os.path.dirname(__file__)
        if not sg :
            self.sg = Shotgrid_Data("baked")
        else : self.sg = sg

        # WebhookServer() # flask server open

    def _set_ui(self):
        ui_file_path = f"{self.py_file_path}/tracker.ui"
        ui_file = QFile(ui_file_path)
        ui_file.open(QFile.ReadOnly)

        ui_loader = QUiLoader()
        self.ui = ui_loader.load(ui_file, self)
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)

        ui_file.close()

    def _get_opened_file_list(self):
        # 현재 내 작업과 링크되어있는 모든 태스크를 읽어와서 리스트로 저장한다
        asset_list = self.sg.get_assets_used_at_shot()
        task_list = self.sg.get_task_from_ent(self.sg.get_shot_from_code())

        my_content_list = []

        ## my_content_list에 들어있는 데이터들이 모두 최신의 것이어야 함
        ## 현재 내가 열어놓은 파일과 버전이 다르면 list에 출력할 때 색상을 변경하도록 하자
        
        for asset in asset_list:
            my_content_list.append(asset['code'])

        for task in task_list:
            my_content_list.append(f"{self.sg.user_info['shot']}_{task['content']}")

    


if __name__ == "__main__":
    app = QApplication()
    win = Tracker()
    win.show()
    app.exec()