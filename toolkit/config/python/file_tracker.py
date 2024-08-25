try :
    from PySide6.QtWidgets import QApplication, QWidget, QTreeWidgetItem
    from PySide6.QtWidgets import QTreeWidget, QLabel, QHBoxLayout
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import QFile, Qt, Signal
    from PySide6.QtGui import QPixmap, QColor

except:
    from PySide2.QtWidgets import QApplication, QWidget, QTreeWidgetItem
    from PySide2.QtWidgets import QTreeWidget, QLabel, QHBoxLayout
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtCore import QFile, Qt, Signal
    from PySide2.QtGui import QPixmap, QColor

import os
import re

from pprint import pprint

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
        self._get_file_list_related_to_my_work()
        self._get_lastest_file_data()
        self._check_version()

    def _set_instance_val(self, sg):
        self.py_file_path = os.path.dirname(__file__)
        if not sg :
            self.sg = Shotgrid_Data("baked")
        else : self.sg = sg

        self.lastest_file_dict = {}

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
        ## 현재 내가 작업중인 파일에 열려있는 모든 파일 리스트를 가져온다
        ## nuke : 현재 존재하는 모든 write node에 knob("file")을 읽어오기
        ## maya : 선생님이 알려주신.... 뭔가의 캐시 파일 경로와 버전을 저장하는 방식을 사용하기
        self.opened_file_list = {
            "ABC_0010_CMP_v001.nknc" : {},
            "ABC_0010_LGT_v001.####.exr" : {},
        }

        for data in self.opened_file_list.keys():
            filters = [
                ["project", "is", self.sg.project_data],
                ["code", "contains", data]
            ]
            fields = ["id", "code", "path", "task", "version"]

            cur_file_data = self.sg.sg.find_one("PublishedFile", filters, fields, order=[{'field_name': 'created_at', 'direction': 'asc'}])
            pprint(cur_file_data)

            if not cur_file_data:
                continue

            self.opened_file_list.update(
                { data : cur_file_data }
            )

        ## 현재 열려있는 파일들의 버전 파일 정보를 가져올까말까... 가져와서 띄울까 말까 개고민됨묘

        self.ui.listWidget_using.clear()
        self.ui.listWidget_using.addItems(self.opened_file_list.keys())
    
    def _get_file_list_related_to_my_work(self):
        # 현재 내 작업과 링크되어있는 모든 태스크를 읽어와서 리스트로 저장한다
        asset_list = self.sg.get_assets_used_at_shot()
        task_list = self.sg.get_task_from_ent(self.sg.get_shot_from_code())

        self.my_content_list = []
                
        for asset in asset_list:
            self.my_content_list.append(asset['code'])

        for task in task_list:
            self.my_content_list.append(f"{self.sg.user_info['shot']}_{task['content']}")


    def _get_lastest_file_data(self):
        ## my_content_list에 들어있는 데이터들이 모두 최신의 것이어야 함
        ## 현재 내가 열어놓은 파일과 버전이 다르면 list에 출력할 때 색상을 변경하도록 하자

        for data in self.my_content_list:
            filters = [
                ["project", "is", self.sg.project_data],
                ["code", "contains", data]
            ]
            fields = ["id", "code", "path", "task", "version"]

            last_file_data = self.sg.sg.find_one("PublishedFile", filters, fields, order=[{'field_name': 'created_at', 'direction': 'desc'}])
            pprint(last_file_data)

            if not last_file_data:
                continue

            self.lastest_file_dict.update(
                { last_file_data['code'] : last_file_data }
            )

        """
        {'code': 'ABC_0010_LGT_v001.####.exr',
        'id': 322,
        'path': {'content_type': 'image/exr',
                'id': 1131,
                'link_type': 'local',
                'local_path': '/home/rapa/baked/show/baked/SEQ/ABC/ABC_0010/LGT/pub/nuke/images/ABC_0010_LGT_v001/ABC_0010_LGT_v001.####.exr',
                'local_path_linux': '/home/rapa/baked/show/baked/SEQ/ABC/ABC_0010/LGT/pub/nuke/images/ABC_0010_LGT_v001/ABC_0010_LGT_v001.####.exr',
                'local_path_mac': None,
                'local_path_windows': 'D:\\show\\baked\\show\\baked\\SEQ\\ABC\\ABC_0010\\LGT\\pub\\nuke\\images\\ABC_0010_LGT_v001\\ABC_0010_LGT_v001.####.exr',
                'local_storage': {'id': 3, 'name': 'show', 'type': 'LocalStorage'},
                'name': 'ABC_0010_LGT_v001.####.exr',
                'type': 'Attachment',
                'url': 'file:///home/rapa/baked/show/baked/SEQ/ABC/ABC_0010/LGT/pub/nuke/images/ABC_0010_LGT_v001/ABC_0010_LGT_v001.####.exr'},
        'task': {'id': 6128, 'name': 'LGT', 'type': 'Task'},
        'type': 'PublishedFile',
        'version': {'id': 7800, 'name': 'v001', 'type': 'Version'}}
        """

    def _check_version(self):
        for key in self.opened_file_list:
            p = re.compile("[v]\d{3}")
            version = p.search(key).group()
            mat = key.split(version)[0]

            for last_key in self.lastest_file_dict.keys():
                if mat in last_key:
                    if version == self.lastest_file_dict[last_key]['version']:
                        break
                    item = self.ui.listWidget_using.findItems(key, Qt.MatchFlag.MatchExactly)[0]
                    item.setBackground(QColor("yellow"))
                    break
                    


if __name__ == "__main__":
    app = QApplication()
    win = Tracker()
    win.show()
    app.exec()