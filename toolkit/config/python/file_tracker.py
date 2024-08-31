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
import threading
from pprint import pprint

## 마야나 누크가 열릴 때 tracker 코드가 작동되게 하며 메뉴바를 통해서 유아이를 열게 한다


from shotgrid.fetch_shotgrid_data import ShotGridDataFetcher


class Tracker(QWidget):
    RELOAD_FILE = Signal(str, str)

    def __init__(self, sg : ShotGridDataFetcher = None):
        super().__init__()
        self._set_instance_val(sg)
        self._set_ui()
        self._set_event()

        self._test_exec()

    def _test_exec(self):
        self._get_opened_file_list()
        self._get_file_list_related_to_my_work()
        self._get_lastest_file_data()
        self._check_version()

    def _set_instance_val(self, sg):
        self.py_file_path = os.path.dirname(__file__)
        if not sg :
            self.sg = ShotGridDataFetcher()
            # 샷그리드 데이터가 연결되지 않으니 tracker를 사용할 수 없다고 pop하기!
        else : 
            self.sg = sg
            self.sg.observer.NEW_FILE_OCCUR.connect(self._check_new_data_type)

        self.lastest_file_dict = {}


    def _set_ui(self):
        ui_file_path = f"{self.py_file_path}/ui_files/tracker.ui"
        ui_file = QFile(ui_file_path)
        ui_file.open(QFile.ReadOnly)

        ui_loader = QUiLoader()
        self.ui = ui_loader.load(ui_file, self)
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)

        ui_file.close()

    def _set_event(self):
        self.ui.listWidget_using.itemClicked.connect(self._show_selected_item_data)
        self.ui.pushButton_load.clicked.connect(self._load_new_version)

    def _get_opened_file_list(self):
        ## 현재 내가 작업중인 파일에 열려있는 모든 파일 리스트를 가져온다
        ## nuke : 현재 존재하는 모든 write node에 knob("file")을 읽어오기
        ## maya : 선생님이 알려주신.... 뭔가의 캐시 파일 경로와 버전을 저장하는 방식을 사용하기
        self.opened_file_list = {
            # "ABC_0010_CMP_v001.nknc" : {},
            "ABC_0010_LGT_v001.####.exr" : {},
        }

        for data in self.opened_file_list.keys():
            filters = [
                ["project", "is", self.sg.project],
                ["code", "contains", data]
            ]
            fields = ["id", "code", "path", "created_by", "task", "version", "published_file_type", "description"]

            cur_file_data = self.sg.sg.find_one("PublishedFile", filters, fields, order=[{'field_name': 'created_at', 'direction': 'asc'}])
            pprint(cur_file_data)

            if not cur_file_data:
                continue

            self.opened_file_list.update(
                { data : cur_file_data }
            )

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
                ["project", "is", self.sg.project],
                ["code", "contains", data]
            ]
            fields = ["id", "code", "path", "created_by", "task", "version", "published_file_type", "description"]

            last_file_data = self.sg.sg.find_one("PublishedFile", filters, fields, order=[{'field_name': 'created_at', 'direction': 'desc'}])
            pprint(last_file_data)

            if not last_file_data:
                continue

            self.lastest_file_dict.update(
                { last_file_data['code'] : last_file_data }
            )

        """
        {
        'code': 'ABC_0010_LGT_v001.####.exr',
        'created_by': {'id': 99, 'name': 'baked 1.0', 'type': 'ApiUser'},
        'description': 'Description of the published file',
        'id': 338,
        'path': {'content_type': 'image/exr',
                'id': 1155,
                'link_type': 'local',
                'local_path': '/home/rapa/baked/show/baked/SEQ/ABC/ABC_0010/LGT/pub/nuke/images/ABC_0010_LGT_v001/ABC_0010_LGT_v001.####.exr',
                'local_path_linux': '/home/rapa/baked/show/baked/SEQ/ABC/ABC_0010/LGT/pub/nuke/images/ABC_0010_LGT_v001/ABC_0010_LGT_v001.####.exr',
                'local_path_mac': None,
                'local_path_windows': 'D:\\show\\baked\\show\\baked\\SEQ\\ABC\\ABC_0010\\LGT\\pub\\nuke\\images\\ABC_0010_LGT_v001\\ABC_0010_LGT_v001.####.exr',
                'local_storage': {'id': 3, 'name': 'show', 'type': 'LocalStorage'},
                'name': 'ABC_0010_LGT_v001.####.exr',
                'type': 'Attachment',
                'url': 'file:///home/rapa/baked/show/baked/SEQ/ABC/ABC_0010/LGT/pub/nuke/images/ABC_0010_LGT_v001/ABC_0010_LGT_v001.####.exr'},
        'published_file_type': {'id': 185,
                                'name': 'EXR Image',
                                'type': 'PublishedFileType'},
        'task': {'id': 6128, 'name': 'LGT', 'type': 'Task'},
        'type': 'PublishedFile',
        'version': {'id': 7840, 'name': 'v002', 'type': 'Version'}
        }
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
    
    def _show_selected_item_data(self, item):
        key = item.text()
        file_data = self.opened_file_list[key]

        self.ui.label_file.setText(key)
        # self.ui.label_path.setText(file_data['path']['local_path'])
        self.ui.label_user.setText(file_data['created_by']['name'])
        self.ui.label_task.setText(file_data['task']['name'])
        self.ui.label_type.setText(file_data['published_file_type']['name'])

        self.ui.plainTextEdit_comment.clear()
        self.ui.plainTextEdit_comment.insertPlainText(file_data['description'])

        if self.opened_file_list[key]['version']['name'] != self.lastest_file_dict[key]['version']['name']:
            self.ui.label_version.setText("You have a new version for this file")
            self.ui.pushButton_load.setEnabled(True)
        else:
            self.ui.label_version.setText("")
            self.ui.pushButton_load.setEnabled(False)


    def _check_new_data_type(self, data : dict):
        """
        flask 서버에서 받아온 data로 원하는 entity 값을 뽑아내서
        last version에 넣고 리스트의 정보를 업데이트 해준다
        """
        print(data)
        key = data['code']
        p = re.compile("[v]\d{3}")
        version = p.search(key).group()
        mat = key.split(version)[0]

        for cur_data in self.lastest_file_dict.keys():
            if mat in cur_data:
                self.lastest_file_dict.pop(cur_data)
                self.lastest_file_dict[key] = data
                break

        self._check_version()
        self._show_selected_item_data()

    def _load_new_version(self):
        cur_item = self.ui.listWidget_using.currentItem()
        key = cur_item.text()
        cur_path = self.opened_file_list[key]['path']['local_path']

        p = re.compile("[v]\d{3}")
        version = p.search(key).group()
        mat = key.split(version)[0]

        new_v_key = next((n for n in self.lastest_file_dict.keys() if mat in n), None)

        self.opened_file_list.pop(key)
        self.opened_file_list[new_v_key] = self.lastest_file_dict[new_v_key]

        cur_item.setText(new_v_key)

        new_path = self.opened_file_list[new_v_key]['path']['local_path']

        self._show_selected_item_data(cur_item)
        cur_item.setBackground(QColor(None))

        self.RELOAD_FILE.emit(cur_path, new_path)
    


if __name__ == "__main__":
    app = QApplication()
    win = Tracker()
    win.show()
    app.exec()