try :
    from PySide6.QtWidgets import QApplication, QWidget
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import QFile, Signal
    from PySide6.QtGui import QPixmap, QColor

except:
    from PySide2.QtWidgets import QApplication, QWidget
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtCore import QFile, Signal
    from PySide2.QtGui import QPixmap, QColor

import os
import re
from pprint import pprint

from functools import partial

from shotgrid.fetch_shotgrid_data import ShotGridDataFetcher

import subprocess


class Tracker(QWidget):
    RELATED_FILE_DATA_CHANGED = Signal(dict)
    RELOAD_FILE = Signal(str, str)
    LOAD_FILE = Signal(str)

    def __init__(self, sg : ShotGridDataFetcher, open_file_data = None, latest_file_dict = None):
        super().__init__()
        print("Tracker __init__()")
        self._set_instance_val(sg, open_file_data, latest_file_dict)
        self._set_ui()
        self._set_event()
        self._get_file_list_related_to_my_work() # 이거 수정해야됨
        self.get_opened_file_list()


    def _set_instance_val(self, sg, open_file_data, latest_file_dict):
        self.py_file_path = os.path.dirname(__file__)
        self.sg = sg
        # 샷그리드 데이터가 연결되지 않으니 tracker를 사용할 수 없다고 pop하기!
        self.sg.observer.NEW_FILE_OCCUR.connect(self._check_new_data_type)

        self.pub_file_fields = ["id", "code", "path", "created_by", "task", "version", "published_file_type", "description"]
        self.opened_file_path_list = open_file_data
        self.lastest_file_dict = latest_file_dict
        self.opened_file_dict = {}
        self.cur_showing_data = {}
        self.related_tasks = []

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
        self.ui.pushButton_movie.clicked.connect(self.open_mov)

    def get_opened_file_list(self, open_file_path_list = None):
        if open_file_path_list :
            print(f"!!!!!!!!!!!!!!!!!Get Open File : {open_file_path_list}")
            self.opened_file_path_list = open_file_path_list
        # 현재 내가 열고 있는 모든 파일들의 정보를 shotgrid에서 읽어와서 저장한다
        if self.opened_file_path_list :
            for data in self.opened_file_path_list:
                file_name = os.path.basename(data)
                if file_name in self.opened_file_dict.keys() :
                    continue
                filters = [
                    ["project", "is", self.sg.project],
                    ["code", "contains", file_name]
                ]

                cur_file_data = self.sg.sg.find_one("PublishedFile", 
                                                    filters, 
                                                    self.pub_file_fields, 
                                                    order=[{'field_name': 'created_at', 'direction': 'desc'}])

                if not cur_file_data:
                    continue
                self.opened_file_dict[file_name] = cur_file_data 

        self._set_list_data()
        

    def _set_list_data(self):
        self.ui.listWidget_using.clear()
        self.ui.listWidget_not.clear()
        using_row = 0

        if not self.opened_file_dict:
            self.ui.listWidget_not.addItems(self.lastest_file_dict.keys())
            return

        for file in self.lastest_file_dict.keys():
            parse = re.compile("v\d{3}")
            p_data = parse.search(file).group()
            file_name = file.split(p_data)[0]
            _, ext = os.path.splitext(file)

            opened_file = next((key for key, f in self.opened_file_dict.items() if file_name in key and ext in key), None)
            if not opened_file:
                print(f"Put {file} in not using list.")
                self.ui.listWidget_not.addItem(file)
            else:
                print(f"Put {opened_file} in using list.")
                self.ui.listWidget_using.addItem(opened_file)
                item = self.ui.listWidget_using.item(using_row)
                using_row += 1
                if file != opened_file :
                    item.setBackground(QColor("yellow"))
                    

    
    def _get_file_list_related_to_my_work(self):
        if self.lastest_file_dict :
            self._set_list_data()
            return
        
        # tracker가 실행될 때 최초 한 번만 실행됨
        my_task = self.sg.user_info["task"]
        """
        현재 내 작업에서 필요한 선행 작업의 최신 version에 링크된 publishedFiles 값을 가져오는 메서드
        """
        task_level = {
            # 각 task에서 필요한 선행 TASK들을 저장해둔 것
            "MOD" : {'asset' : [], 'shot' : []},
            "RIG" : {'asset' : ['MOD'], 'shot' : []},
            "LKD" : {'asset' : ['MOD'], 'shot' : []},
            "ANI" : {'asset' : ['RIG'], 'shot' : ['MM']},
            "LGT" : {'asset' : ['LKD'], 'shot' : ['ANI', 'LKD', 'MM']},
            "CMP" : {'asset' : [], 'shot' : ['LGT', 'MM']},
        }
        pub_files = {}
        self.related_tasks = []
        for ast_task in task_level[my_task]['asset']:
            # asset 작업자라면 해당 asset의 task 엔티티를 찾아서 저장하고
            if self.sg.user_info['asset']:
                task = self.sg.sg.find_one("Task", [['entity', 'is', self.sg.work], ['content','is',ast_task]])
                self.related_tasks.append(task)
            # shot 작업자라면 shot에 link되어있는 asset엔티티를 찾아서 task 엔티티를 저장한다
            elif self.sg.user_info['shot']:
                # shot에 링크된 asset들을 찾는다
                assets = self.sg.sg.find_one("Shot", [['id', 'is', self.sg.work['id']]], ['assets'])['assets']    
                for asset in assets:
                    task = self.sg.sg.find_one("Task", [['entity', 'is', asset], ['content','is',ast_task]])
                    self.related_tasks.append(task)

        for shot_task in task_level[my_task]['shot']:
            task = self.sg.find_one("Task", [['entity', 'is', self.sg.work], ['content','is',shot_task]])
            self.related_tasks.append(task)

        # 각 task에서 가장 최근에 pub된 version의 pub_files를 가져온다
        for task in self.related_tasks:
            version = self.sg.sg.find_one("Version", 
                                          [['sg_task','is',task]], 
                                          ['published_files'],
                                          order=[{'field_name': 'created_at', 'direction': 'desc'}])
            if not version or not version['published_files']:
                continue

            for file in version['published_files']:
                file = self.sg.sg.find_one("PublishedFile", 
                                           [['id','is',file['id']]], 
                                           self.pub_file_fields)
                pub_files[file['code']] = file
        
        pprint(pub_files)

        self.lastest_file_dict = pub_files
        self._set_list_data()
    
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
            print(f"showing thumbnail... {thumbnail_path}")
            pixmap = QPixmap(thumbnail_path)
            self.ui.label_thumbnail.setPixmap(pixmap)
            self.ui.label_thumbnail.setScaledContents(True)

        self.ui.pushButton_movie.setEnabled(os.path.exists(self.cur_showing_data['movie_path']))


    def _check_new_data_type(self, data : dict):
        """
        flask 서버에서 받아온 data로 원하는 entity 값을 뽑아내서
        last version에 넣고 리스트의 정보를 업데이트 해준다
        """
        print(data) # 새로 들어오는 정보는 version entity가 생성되었을 때의 것이다
        version = data.get('entity')
        version = self.sg.find_one("Version", [['id', 'is', version['id']]], ['task', 'published_files'])

        if version['task'] not in self.related_tasks:
            return
        
        for pub_file in version['published_files']:
            old_data_key = next((key for key, f in self.lastest_file_dict.items() if f['task']['id'] == version['task']['id']))
            self.lastest_file_dict.pop(old_data_key)
            self.lastest_file_dict[pub_file['code']] = pub_file

        self._set_list_data()
        self._show_selected_item_data()
        self.RELATED_FILE_DATA_CHANGED.emit(self.lastest_file_dict)

    def _load_new_version(self):
        reload_item = self.ui.listWidget_using.currentItem()
        load_item = self.ui.listWidget_not.currentItem()

        if reload_item:
            cur_path = self.opened_file_dict[reload_item.text()]
            new_v_key = next((key for key, f in self.lastest_file_dict.items() if self.opened_file_dict[reload_item.text()]['task']['id'] == f['task']['id']), None)

            self.opened_file_dict.pop(reload_item)
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
            self.LOAD_FILE.emit(file_path)
            self._set_list_data()

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
    win = Tracker(ShotGridDataFetcher())
    win.show()
    app.exec()