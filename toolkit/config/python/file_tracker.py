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

from functools import partial

from shotgrid.fetch_shotgrid_data import ShotGridDataFetcher

import subprocess


class Tracker(QWidget):
    RELOAD_FILE = Signal(str, str)
    LOAD_FILE = Signal(str)

    def __init__(self, sg : ShotGridDataFetcher = None, open_file_data = None):
        super().__init__()
        self._set_instance_val(sg, open_file_data)
        self._set_ui()
        self._set_event()

        self._test_exec()

    def _test_exec(self):
        self._get_file_list_related_to_my_work()
        self.get_opened_file_list()


    def _set_instance_val(self, sg, open_file_data):
        self.py_file_path = os.path.dirname(__file__)
        if not sg :
            self.sg = ShotGridDataFetcher()
            # 샷그리드 데이터가 연결되지 않으니 tracker를 사용할 수 없다고 pop하기!
        else : 
            self.sg = sg
            self.sg.observer.NEW_FILE_OCCUR.connect(self._check_new_data_type)

        self.lastest_file_dict = {}
        self.pub_file_fields = ["id", "code", "path", "created_by", "task", "version", "published_file_type", "description"]
        self.opened_file_path_list = open_file_data
        self.opened_file_dict = {}
        self.cur_showing_data = {}

    def _set_ui(self):
        ui_file_path = f"{self.py_file_path}/ui_files/tracker.ui"
        ui_file = QFile(ui_file_path)
        ui_file.open(QFile.ReadOnly)

        ui_loader = QUiLoader()
        self.ui = ui_loader.load(ui_file, self)
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)

        ui_file.close()

    def _set_event(self):
        self.ui.listWidget_using.itemClicked.connect(partial(self._set_current_selected_data, "using"))
        self.ui.listWidget_not.itemClicked.connect(partial(self._set_current_selected_data, "not"))
        self.ui.pushButton_load.clicked.connect(self._load_new_version)
        self.ui.label_thumbnail.doubleClicked.connect(self.open_mov)

    def get_opened_file_list(self):
        ## 현재 내가 작업중인 파일에 열려있는 모든 파일 리스트를 가져온다
        ## nuke : 현재 존재하는 모든 write node에 knob("file")을 읽어오기
        ## maya : 선생님이 알려주신.... 뭔가의 캐시 파일 경로와 버전을 저장하는 방식을 사용하기
        if self.opened_file_path_list :
            for data in self.opened_file_path_list:
                file_name = os.path.basename(data)
                if self.opened_file_dict[file_name] :
                    continue
                filters = [
                    ["project", "is", self.sg.project],
                    ["code", "contains", file_name]
                ]

                cur_file_data = self.sg.sg.find_one("PublishedFile", filters, self.pub_file_fields, order=[{'field_name': 'created_at', 'direction': 'asc'}])

                if not cur_file_data:
                    continue

                self.opened_file_dict[file_name] = cur_file_data 

        self._set_list_data()
        

    def _set_list_data(self):
        self.ui.listWidget_using.clear()
        self.ui.listWidget_not.clear()
        if not self.opened_file_dict:
            self.ui.listWidget_not.addItems(self.lastest_file_dict.keys())
        else:
            for file in self.lastest_file_dict.keys():
                p = re.compile("[v]\d{3}")
                version = p.search(file).group()
                mat = file.split(version)[0] +'v'
                opened_file = next((f for f in self.opened_file_dict.keys() if mat in f), None)
                if not opened_file:
                    print(f"Put {file} in not using list.")
                    self.ui.listWidget_not.addItem(file)
                else:
                    print(f"Put {opened_file} in using list.")
                    item = self.ui.listWidget_using.addItem(opened_file)
                    if file != opened_file :
                        item.setBackground(QColor("yellow"))
                    

    
    def _get_file_list_related_to_my_work(self):
        my_task = self.sg.user_info["task"]
        """
        현재 내 작업에서 필요한 선행 작업의 최신 version에 링크된 publishedFiles 값을 가져오는 메서드
        """
        task_level = {
            # 각 task에서 필요한 선행 TASK들을 저장해둔 것
            "MOD" : [],
            "RIG" : ['MOD'],
            "LKD" : ['MOD'],
            "ANI" : ['RIG', 'MM'],
            "LGT" : ['ANI', 'LKD', 'MM'],
            "CMP" : ['LGT', 'MM'],
        }
        pub_files = {}
        for task_content in task_level[my_task]:
            entity = self.sg.get_asset_entity(self.sg.user_info['asset'])
            if not entity:
                entity = self.sg.get_shot_from_code(self.sg.user_info['shot'])
            task = self.sg.fetch_cur_task_by_taskname_linkedentity(task_content, entity)

            version = self.sg.sg.find_one("Version", 
                                          [['entity','is',entity],['sg_task','is',task]], 
                                          ['published_files'],
                                          order=[{'field_name': 'created_at', 'direction': 'asc'}])
            if not version:
                continue

            for file in version['published_files']:
                file = self.sg.sg.find_one("PublishedFile", 
                                           [['id','is',file['id']]], 
                                           self.pub_file_fields)
                pub_files[file['code']] = file

            self.lastest_file_dict = pub_files
        
        pprint(pub_files)


    # def _check_version(self):
    #     for key in self.opened_file_dict:
    #         p = re.compile("[v]\d{3}")
    #         version = p.search(key).group()
    #         mat = key.split(version)[0]

    #         for last_key in self.lastest_file_dict.keys():
    #             if mat in last_key:
    #                 if version == self.lastest_file_dict[last_key]['version']:
    #                     break
    #                 item = self.ui.listWidget_using.findItems(key, Qt.MatchFlag.MatchExactly)[0]
    #                 item.setBackground(QColor("yellow"))
    #                 break
    
    def _set_current_selected_data(self, list_name, item):
        key = item.text()

        if list_name == "using":
            self.ui.listWidget_not.setCurrentRow(-1)
            self.cur_showing_data = self.opened_file_dict[key]
        elif list_name == "not":
            self.ui.listWidget_using.setCurrentRow(-1)
            self.cur_showing_data = self.lastest_file_dict[key]

        self._show_selected_item_data(key, list_name)

        if list_name == 'using':
            if item.background().color() == QColor('yellow'):
                self.ui.label_version.setText("You have a new version for this file")
                self.ui.pushButton_load.setEnabled(True)
            else:
                self.ui.label_version.setText("")
                self.ui.pushButton_load.setEnabled(False)
        elif list_name == 'not':
            self.ui.label_version.setText("You didn't open this file yet")
            self.ui.pushButton_load.setEnabled(True)


    def _show_selected_item_data(self, key, list_name):
        self.ui.label_file.setText(key)
        # self.ui.label_path.setText(file_data['path']['local_path'])
        self.ui.label_user.setText(self.cur_showing_data['created_by']['name'])
        self.ui.label_task.setText(self.cur_showing_data['task']['name'])
        self.ui.label_type.setText(self.cur_showing_data['published_file_type']['name'])
        self.ui.plainTextEdit_comment.clear()
        self.ui.plainTextEdit_comment.insertPlainText(self.cur_showing_data['description'])

        path = self.cur_showing_data['path']['local_path']
        thumbnail_dir = os.path.dirname(path).replace("/scenes/", "/movies/ffmpeg/")
        file, _ = os.path.splitext(os.path.basename(path))
        thumbnail_path = f"{thumbnail_dir}{file}_slate.jpg"
        self.cur_showing_data['movie_path'] = f"{thumbnail_dir}{file}_slate.mov"
        if os.path.exists(thumbnail_path):
            pixmap = QPixmap(thumbnail_path)
            self.ui.label_thumbnail.setPixmap(pixmap)
            self.ui.label_thumbnail.setScaledContents(True)




    def _check_new_data_type(self, data : dict):
        """
        flask 서버에서 받아온 data로 원하는 entity 값을 뽑아내서
        last version에 넣고 리스트의 정보를 업데이트 해준다
        """
        print(data)
        key = data['code']
        p = re.compile("[v]\d{3}") 
        version = p.search(key).group()
        mat = key.split(version)[0] +'v'

        for cur_data in self.lastest_file_dict.keys():
            if mat in cur_data:
                self.lastest_file_dict.pop(cur_data)
                self.lastest_file_dict[key] = data
                break

        self._set_list_data()
        self._show_selected_item_data()

    def _load_new_version(self):
        reload_item = self.ui.listWidget_using.currentItem()
        load_item = self.ui.listWidget_not.currentItem()

        if reload_item:
            key = reload_item.text()
            cur_path = self.opened_file_dict[key]['path']['local_path']

            p = re.compile("[v]\d{3}")
            version = p.search(key).group()
            mat = key.split(version)[0] + "v"

            new_v_key = next((n for n in self.lastest_file_dict.keys() if mat in n), None)

            self.opened_file_dict.pop(key)
            self.opened_file_dict[new_v_key] = self.lastest_file_dict[new_v_key]

            reload_item.setText(new_v_key)

            new_path = self.opened_file_dict[new_v_key]['path']['local_path']

            self._show_selected_item_data(reload_item)
            reload_item.setBackground(QColor(None))

            self.RELOAD_FILE.emit(cur_path, new_path)

        elif load_item:
            key = load_item.text()
            file_path = self.lastest_file_dict[key]['path']['local_path']
            print(f"Opened {file_path}")

            self.opened_file_dict[key] = self.lastest_file_dict[key]
            self._set_list_data()
            self.LOAD_FILE.emit(file_path)

    def open_mov(self):
        if not self.cur_showing_data :
            return
        
        mov_path = self.cur_showing_data['movie_path']
        
        rv_player_path = "rv"
        if not os.path.exists(mov_path):
            print(f"Error: {mov_path} 파일을 찾을 수 없습니다.")
            return
        
        try:
            subprocess.run([rv_player_path, mov_path])
        except Exception as e:
            print("RV Player 실행 오류")


if __name__ == "__main__":
    app = QApplication()
    win = Tracker()
    win.show()
    app.exec()