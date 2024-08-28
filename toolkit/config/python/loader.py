
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
import yaml
from pprint import pprint

try :
    from shotgrid.get_shotgrid_data import Shotgrid_Data
except :
    from get_shotgrid_data import Shotgrid_Data
    
from file_open import FileOpen

class Loader(QWidget):
    """
    Shotgrid 서버와 연결하여 현재 프로젝트에서 진행중인 파일들을 load해주는
    QWidget을 상속하는 클래스 입니다

    주석에서 말하는 서버는 작업에 쓰이는 파일들이 저장되는 곳을 뜻합니다
    Shotgrid 서버를 말하는 경우엔 Shotgrid라고 명시하고 있습니다
    """


    OPEN_FILE = Signal(str)

######################## __init__ 시점에서 불려지는 함수들 ###########################

    def __init__(self, sg : Shotgrid_Data, tool : str = None):
        """
        처음 Loader가 생성될 때 설정되어야하는 메서드들이 작성되어있는 생성자 
        """
        super().__init__()
        self._set_init_val(sg, tool)
        self._set_ui()
        self._set_event()
        self.set_tree_widget_data()
        self._set_my_task_table_widget()

    def _set_init_val(self, sg, tool):
        """
        Loader에서 사용되는 instance 변수들을 미리 지정해두는 메서드
        """
        test_path = {
            # 실행 환경이 다른 경우에 주소값을 바꾸기 위해서 저장해둔 값들 입니다 (추후 제거)
            # 다른 경로에서 작업하는 경우 test_path에 등록하고 self.home_path 변경하여 사용하세용   
            "rapa" : "/home/rapa/baked",
            "choo_mac" : "/Users/yerin/Desktop/NetflixAcademy/baked"
        }

        self.home_path = test_path["rapa"] # 다른 경로에서 작업할 때 변경할 부분입니다!

        self.project_name = "baked" # 프로젝트 이름 데이터 후에 login 시 읽어온 데이터로 사용해야됨. (추후 제거)
        self.py_file_path = os.path.dirname(__file__)
        self.sg : Shotgrid_Data = sg # login 시에 지정된 userdata를 가지고 Shotgrid에서 정보를 가져오는 Shotgrid_Data() 클래스
        self.project_path = f"{self.home_path}/show/{self.project_name}" # shotgrid가 실행되지 않을 때를 위한 기본 경로값 (추후 제거?)
        self.tool = tool # 현재 loader가 tool 프로그램을 통해서 실행되었을 때 값이 들어가는 변수
        self.content_files_data = {} # 현재 작업에서 사용되는 파일들의 정보들이 들어가는 dict

    def _set_ui(self):
        """
        Loader의 UI File이 설정되는 메서드
        """
        ui_file_path = f"{self.py_file_path}/loader.ui"
        ui_file = QFile(ui_file_path)
        ui_file.open(QFile.ReadOnly)

        ui_loader = QUiLoader()
        self.ui = ui_loader.load(ui_file, self)

        if self.tool :
            # tool 내에서 열릴 때에만 Loader창이 최상단에 있도록 함 
            self.setWindowFlags(Qt.WindowStaysOnTopHint) 

        ui_file.close()

    def _set_event(self):
        """
        UI 객체들 이벤트가 발생할 때 실행될 메서드를 연결해주는 메서드
        """
        self.OPEN_FILE.connect(self._open_file_from_loader)

        self.ui.tableWidget_files.cellDoubleClicked.connect(self._find_dir_name_in_tree)

        self.ui.treeWidget_task.currentItemChanged.connect(self._set_my_task_table_widget)
        self.ui.treeWidget_task.itemClicked.connect(self._set_my_task_table_widget)

        self.ui.treeWidget_asset.currentItemChanged.connect(self._set_asset_table_widget)
        self.ui.treeWidget_asset.itemClicked.connect(self._set_asset_table_widget)

        self.ui.treeWidget_seq.currentItemChanged.connect(self._set_seq_table_widget)
        self.ui.treeWidget_seq.itemClicked.connect(self._set_seq_table_widget)

        self.ui.treeWidget_content.currentItemChanged.connect(self._set_content_table_widget)
        self.ui.treeWidget_content.itemClicked.connect(self._set_content_table_widget)

        self.ui.tabWidget_task.currentChanged.connect(self._change_table_data)

#####################################################################################################


#################### tabWidget 연관 메서드 ##########################################################

    def _change_table_data(self, index):
        """
        Loader에서 tabWidget의 현재 tab이 변경되는 경우
        변경된 tab의 index를 받아와서 해당 탭에 맞는 데이터를 tableWidget에 띄우도록 하는 메서드
        """
        if index == 0:
            self._set_my_task_table_widget()
        elif index == 1:
            self._set_content_table_widget()
        elif index == 2:
            self._set_seq_table_widget()
        elif index == 3:
            self._set_asset_table_widget()

###############################################################################################


################# treeWidget 연관 메서드 ##################################################

    def set_tree_widget_data(self):
        """
        Loader가 실행될 때 각 treeWidget에 데이터를 넣어주는 메서드
        """
        self.ui.treeWidget_seq.clear()
        self.ui.treeWidget_asset.clear()
        self.ui.treeWidget_content.clear()
        self.ui.treeWidget_task.clear()


        if not self.sg.connected : # Shotgrid connection failed...
            self._set_seq_tree_widget_by_path()
            self._set_asset_tree_widget_by_path()
            # (추가사항) shotgrid와 연결이 실패했을 때 task tree와 content tree에 관한 처리가 이루어져야 한다

        else : # Shotgrid connected
            self._set_seq_tree_widget_by_shotgrid()
            self._set_asset_tree_widget_by_shotgrid()
            self._set_task_tree_widget_by_shotgrid()
            self._set_content_tree_widget_by_shotgrid()


    ###### Shotgrid에서 데이터를 가져오는 경우

    def _set_task_tree_widget_by_shotgrid(self):
        """
        Shotgrid에서 데이터를 가져와 현재 프로그램을 사용하고 있는 유저가 진행해야되는 작업물의 파일을 띄워주는
        treeWidget_task에 데이터를 넣어주는 메서드
        """
        task_tree = self.ui.treeWidget_task
        my_work = self.sg.user_info["shot"]
        my_task = self.sg.user_info["task"]
        if not my_work :
            my_work = self.sg.user_info["asset"]
            work_item = self._add_tree_item(task_tree, f"{my_work}/{my_task}")
        else :
            work_item = self._add_tree_item(task_tree, f"{my_work}/{my_task}")
        task_tree.setCurrentItem(work_item, 0)
        my_task_path = self._get_path()
        self._add_to_tree_widget_by_path_recursive(work_item, my_task_path)

    def _set_content_tree_widget_by_shotgrid(self):
        """
        현재 작업에서 불러와야하는 pub된 자료들을 띄워주는 treeWidget_content에
        Shotgrid에서 읽어온 데이터를 넣어주는 메서드
        """
        content_tree = self.ui.treeWidget_content
        my_task = self.sg.user_info["task"]
        task_level = {
            # 각 task에서 필요한 데이터들의 level을 저장해둔 것
            # published_file_type의 level field 값을 나눠두었습니다 참고
            "MOD" : [0],
            "RIG" : [1],
            "LKD" : [1],
            "ANI" : [0, 2],
            "LGT" : [0, 2, 3],
            "CMP" : [0, 4],
        }
        file_types = {}

        # 현재 Task에서 필요한 값을 가져오도록 하는 for문
        for i in task_level[my_task]:
            filters = [['sg_level', 'is', f'{i}']]
            fields = ['code', 'id', 'sg_level']
            file_type = self.sg.sg.find("PublishedFileType", filters, fields)
            if not file_type :
                break
            for ft in file_type:
                file_types[ft['code']] = ft # { "Plate" : Plate Entity }

        self._add_tree_item(content_tree, "All Content") # 전체 파일들을 출력할 선택지 하나를 추가
        for f_type in file_types.keys():
            self._add_tree_item(content_tree, f_type)

        if task_level[my_task][-1] < 2 : # Asset 작업자일 경우
            working = [self.sg.user_info['asset']]
        else : 
            working = [self.sg.user_info['shot']]
            assets = self.sg.get_assets_used_at_shot() # 현재 shot에서 사용되는 asset들을 추가해줌
            for asset in assets:
                working.append(asset['code'])

        self.content_files_data = {}

        for w in working: # 현재 작업에 필요한 shot, asset 데이터들을 하나씩 가져와서
            for t in task_level.keys():
                filters = [
                    ["project", "is", self.sg.project_data],
                    ["code", "contains", t],
                    ["code", "contains", w],
                ]
                fields = ["id", "code", "path", "published_file_type"]
                file_data = self.sg.sg.find_one("PublishedFile", filters, fields, order=[{'field_name': 'created_at', 'direction': 'asc'}])
                if not file_data:
                    continue
                self.content_files_data[file_data['code']] = file_data # 내 작업에 필요한 데이터를 가져옴
                # print(file_data)

                """
                file_data의 출력 결과

                {'type': 'PublishedFile', 'id': 337, 'code': 'ABC_0010_LGT_v001.####.exr', 
                'path': {
                    'content_type': 'image/exr', 'link_type': 'local', 'name': 'ABC_0010_LGT_v001.####.exr', 
                    'local_storage': {'type': 'LocalStorage', 'id': 3, 'name': 'show'}, 
                    'local_path_mac': None, 
                    'local_path_linux': '/home/rapa/baked/show/baked/SEQ/ABC/ABC_0010/LGT/pub/nuke/images/ABC_0010_LGT_v001/ABC_0010_LGT_v001.####.exr', 
                    'local_path_windows': 'D:\\show\\baked\\show\\baked\\SEQ\\ABC\\ABC_0010\\LGT\\pub\\nuke\\images\\ABC_0010_LGT_v001\\ABC_0010_LGT_v001.####.exr', 
                    'type': 'Attachment', 'id': 1154, 
                    'local_path': '/home/rapa/baked/show/baked/SEQ/ABC/ABC_0010/LGT/pub/nuke/images/ABC_0010_LGT_v001/ABC_0010_LGT_v001.####.exr', 
                    'url': 'file:///home/rapa/baked/show/baked/SEQ/ABC/ABC_0010/LGT/pub/nuke/images/ABC_0010_LGT_v001/ABC_0010_LGT_v001.####.exr'
                    }, 
                'published_file_type': {'id': 185, 'name': 'EXR Image', 'type': 'PublishedFileType'}}
                """    

    def _set_seq_tree_widget_by_shotgrid(self):
        """
        Shotgrid에서 현재 project에 존재하는 sequence 정보를 읽어와서
        해당 seq와 링크된 shot, shot에 링크된 task를 treeWidget에 넣고
        task가 가리키는 서버의 폴더를 가져와서 폴더 구조를 하위에 넣어주는 메서드
        """
        seq_tree = self.ui.treeWidget_seq

        self.seq_data = {
            # yaml 파일에 저장된 template을 통해 서버(파일이 저장되는 곳)주소를 구하기 위해
            # 현재 for문에서 작업되고 있는 seq, shot, task의 정보를 저장해둔 것
            "project" : self.sg.user_info["project"],
            "sequence" : None,
            "shot" : None,
            "asset" : None,
            "task" : None,
            "asset_type" : None
        }

        seqs = self.sg.get_sequences_entities()

        for seq in seqs:
            self.seq_data["sequence"] = seq['code']
            seq_item = self._add_tree_item(seq_tree, seq['code'])
            shots = self.sg.get_shot_from_seq(seq)
            for shot in shots:
                self.seq_data["shot"] = shot['code']
                shot_item = self._add_tree_item(seq_item, shot['code'])
                tasks = self.sg.get_task_from_ent(shot)
                for task in tasks:
                    self.seq_data["task"] = task['content']
                    task_item = self._add_tree_item(shot_item, task['content'])
                    # 현재 for문이 진행중인 seq, shot, task 정보를 가지고 yaml 파일을 통해 주소 생성
                    seq_path = self._get_path(self.seq_data) 
                    # 가져온 주소 하위에 존재하는 폴더 구조를 재귀함수로 task_item 하단에 추가해준다
                    self._add_to_tree_widget_by_path_recursive(task_item, seq_path)

    def _set_asset_tree_widget_by_shotgrid(self):
        """
        Shotgrid에서 현재 project에 존재하는 asset 정보를 읽어와서
        해당 asset와 링크된 task를 treeWidget에 넣고
        task가 가리키는 서버의 폴더를 가져와서 폴더 구조를 하위에 넣어주는 메서드
        """
        asset_tree = self.ui.treeWidget_asset
        assets = self.sg.get_asset_entities()
        self.asset_data = {
            # yaml 파일에 저장된 template을 통해 서버(파일이 저장되는 곳)주소를 구하기 위해
            # 현재 for문에서 작업되고 있는 seq, shot, task의 정보를 저장해둔 것
            "project" : self.sg.user_info["project"],
            "sequence" : None,
            "shot" : None,
            "asset" : None,
            "task" : None,
            "asset_type" : None
        }
        
        for asset in  assets:
            self.asset_data["asset_type"] = asset['sg_asset_type']
            # asset의 경우 같은 asset_type별로 묶어서 treeWidget에 넣기 위해
            # 현재 tree에 값을 넣을 asset의 asset_type 값이 존재하는 지 찾는다
            grp_list = asset_tree.findItems(self.asset_data["asset_type"], Qt.MatchExactly, 0)
            if len(grp_list) == 0:
                # tree에 현재 넣을 asset의 asset_type 값이 없는 경우 item으로 추가, 부모 아이템으로 지정
                parent_item = self._add_tree_item(asset_tree, self.asset_data["asset_type"])
            else :
                # 존재하는 경우 해당 아이템을 부모 아이템으로 지정
                parent_item = grp_list[0]
            self.asset_data["asset"] = asset['code']
            asset_item = self._add_tree_item(parent_item, asset['code'])
            tasks = self.sg.get_task_from_ent(asset)
            for task in tasks:
                self.asset_data["task"] = task['content']
                task_item = self._add_tree_item(asset_item, task['content'])
                # 현재 for문이 진행중인 asset, task 데이터를 가지고 yaml 파일을 통해 주소 생성
                asset_path = self._get_path(self.asset_data)
                # 가져온 주소 하위에 존재하는 폴더 구조를 재귀함수로 task_item 하단에 추가
                self._add_to_tree_widget_by_path_recursive(task_item, asset_path)
   

   ###### 서버 파일 경로를 통해 가져오는 경우

    def _set_seq_tree_widget_by_path(self):
        """
        파일이 저장되는 서버의 경로를 읽어와서 treeWidget_seq에 item을 넣는 메서드
        """
        seq_tree = self.ui.treeWidget_seq
        self._add_to_tree_widget_by_path_recursive(seq_tree, f"{self.project_path}/SEQ")

    def _set_asset_tree_widget_by_path(self):
        """
        파일이 저장되는 서버의 경로를 읽어와서 treeWidget_asset에 item을 넣는 메서드
        """
        seq_asset = self.ui.treeWidget_asset
        self._add_to_tree_widget_by_path_recursive(seq_asset, f"{self.project_path}/AST")

    def _add_to_tree_widget_by_path_recursive(self, parent_item, addr):
        """
        path와 parent_item이 주어지면 현재 경로 하단에 파일이 존재하지 않을 때까지
        재귀를 돌면서 treeWidgetItem을 추가하는 재귀 메서드
        """
        child_dirs = []
        if os.path.isdir(addr) : 
            child_dirs = os.listdir(addr)
            child_dirs.sort(reverse=True) # version이 높은 파일이 가장 상단에 위치하도록 하기 위해
        for child in child_dirs:
            if not os.path.isdir(f"{addr}/{child}") : 
                continue
            item = self._add_tree_item(parent_item, child)
            path = f"{addr}/{child}"
            self._add_to_tree_widget_by_path_recursive(item, path)

    ###### 그 외 treeWidget에 item을 넣어주는 기능을 수행하는 메서드

    def _add_to_tree_widget_by_path_recursive(self, parent_item, addr):
        """
        path와 parent_item이 주어지면 현재 경로 하단에 파일이 존재하지 않을 때까지
        재귀를 돌면서 treeWidgetItem을 추가하는 재귀 메서드
        """
        child_dirs = []
        if os.path.isdir(addr) : 
            child_dirs = os.listdir(addr)
            child_dirs.sort(reverse=True) # version이 높은 파일이 가장 상단에 위치하도록 하기 위해
        for child in child_dirs:
            if not os.path.isdir(f"{addr}/{child}") : 
                continue
            item = self._add_tree_item(parent_item, child)
            path = f"{addr}/{child}"
            self._add_to_tree_widget_by_path_recursive(item, path)
     
    def _add_tree_item(self, parent_item, text):
        """
        parent_item과 text를 전달받아 parent_item 하단에 item을 생성하고
        생성된 item을 return해주는 간단한 코드입니다
        """
        item = QTreeWidgetItem(parent_item)
        item.setText(0, text)
        return item

############################################################################################################

######################### 주소값과 관련된 메서드들 ##################################################
        
    def _open_yaml_file(self):
        """
        yaml 파일을 열어서 저장되어있는 path template을 읽어오는 메서드
        """
        with open(f'{self.home_path}/toolkit/config/core/env/open_path.yml') as f:
            yaml_data = yaml.load(f, Loader=yaml.FullLoader)
            yaml_path = yaml_data["paths"]
        return yaml_path

    def _get_path(self, path_data=None):
        """
        yaml 파일의 template을 통해서 path를 생성하는 메서드
        path_data : template에 들어갈 값들이 들어있는 dict 데이터
        """
        if not path_data: # path_data가 비어있으면 현재 user가 작업하는 경로를 기본으로 한다
            path_data = self.sg.user_info
        yaml_path = self._open_yaml_file()

        if path_data["asset"] :
            level = "asset"
            current = "asset_path"
            root_path = yaml_path["asset_root"]

        elif path_data["sequence"] :
            level = "sequence"
            current = "sequence_path"
            root_path = yaml_path["sequence_root"]

        if "name" in path_data.keys(): # 작업하는 경로에 대한 경로를 가져올 때
            current = f"my_{current}"
        
        new_path = yaml_path[current]["definition"].replace(f"@{level}_root", root_path)
        new_path = new_path.format(**path_data)
        
        return new_path
    
    def _get_current_item_path(self, data):
        """
        treeWidget에서 선택된 아이템을 기준으로 경로를 구하는 메서드
        """
        yaml_path = self._open_yaml_file()
        root_path = yaml_path[f"{data}_root"].format(**self.sg.user_info)

        current_tab = self.ui.tabWidget_task.currentWidget()
        current_treeWidget = current_tab.findChildren(QTreeWidget)[0]
        item = current_treeWidget.currentItem()

        path = ""
        while item :
            text = item.text(0)
            path = f"{text}/{path}"
            item = item.parent()
        
        new_path = f"{root_path}/{path}"
        print(f"_get_current_item_path : {new_path}")
        return new_path

############################################################################################################

######################### tableWidget과 연관된 메서드들 ##################################################

    def _set_my_task_table_widget(self):
        """
        treeWidget_task가 ui에 띄워진 treeWidget이라면
        해당 값에 대한 파일 데이터들을 tableWidget_files에 띄워주는 메서드
        """
        self.my_path = self._get_path() # 경로에 존재하는 파일들을 tableWidget에 출력해야하므로 경로를 가져온다
        item = self.ui.treeWidget_task.currentItem() 
        sub_path = ""
        self._set_table_for_file_list() # col = 1의 줄 형식의 table 구성

        while item :
            text = item.text(0).split('/')[-1]
            if text in self.sg.user_info.values(): 
                # Shotgrid에서 가져온 데이터가 폴더 이름일 경우
                # 이미 self.mypath에서 알 수 있기 때문에 break
                break
            sub_path = f"{text}/{sub_path}"
            # yaml에서 읽어온 경로보다 하위의 값들만 붙여준다
            item = item.parent()

        self.my_path = f"{self.my_path}/{sub_path}"
        dirs = os.listdir(self.my_path)

        row = 0
        for dir in dirs:
            # 현재 구한 주소 하위에 파일들이 존재하면
            self.ui.tableWidget_files.setRowCount(row + 1)
            if not os.path.isdir(f"{self.my_path}/{dir}"):
                if dir[0] == '.' :
                    continue
                cell = self._make_file_cell(dir) # 파일 아이콘이 설정되는 cell 생성 함수
            else : 
                if dir[0] == '.' :
                    continue
                cell = self._make_dir_cell(dir) # dir 아이콘이 설정되는 cell 생성 함수
            self.ui.tableWidget_files.setCellWidget(row, 0, cell)
            self.ui.tableWidget_files.setRowHeight(row,50)
            row += 1

        path = f"{self._get_path()}/" # 현재 띄우고 있는 창이 가장 상단의 창인지를 확인하기 위한 변수

        if self.my_path == path:
            # 파일이 아무것도 없을 때 혹은 다른 툴의 파일을 생성하고 싶을 때 사용되는 새로운 파일 생성 cell
            self.ui.tableWidget_files.setRowCount(row + 2)

            nuke_cell = self._make_file_cell("Make New Nuke File.nknc")
            self.ui.tableWidget_files.setCellWidget(row, 0, nuke_cell)
            self.ui.tableWidget_files.setRowHeight(row, 50)
            row += 1

            maya_cell = self._make_file_cell("Make New Maya File.mb")
            self.ui.tableWidget_files.setCellWidget(row, 0, maya_cell)
            self.ui.tableWidget_files.setRowHeight(row, 50)

            # 하단에 새로운 툴 파일을 만들 수 있는 cell을 추가할 수 있습니다 ***************************

            return
        
    def _set_seq_table_widget(self):
        """
        treeWidget_seq의 아이템이 선택되었을 때 tableWidget_files에
        이에 해당하는 파일들을 보여주는 메서드
        """
        self.my_path = self._get_current_item_path("sequence")
        dirs = os.listdir(self.my_path)
        row = 0
        self._set_table_for_file_list()
        img_file_list = []
        for dir in dirs:
            if not os.path.isdir(f"{self.my_path}/{dir}"):
                if dir[0] == '.' :
                    continue
                file_name = dir.split('.')[0]
                ext = dir.split('.')[-1]
                if ext in ["png", "exr"] :
                    if f"{file_name}.{ext}" in img_file_list:
                        continue
                    img_file_list.append(f"{dir.split('.')[0]}.{dir.split('.')[-1]}")
                    dir = f"{file_name}.####.{ext}"
                self.ui.tableWidget_files.setRowCount(row + 1)
                cell = self._make_file_cell(dir)
            else : 
                if dir[0] == '.' :
                    continue
                self.ui.tableWidget_files.setRowCount(row + 1)
                cell = self._make_dir_cell(dir)
            self.ui.tableWidget_files.setCellWidget(row, 0, cell)
            self.ui.tableWidget_files.setRowHeight(row,50)
            row += 1

    def _set_asset_table_widget(self):
        """
        treeWidget_asset의 아이템이 선택되었을 때 tableWidget_files에
        이에 해당하는 파일들을 보여주는 메서드
        """
        self.my_path = self._get_current_item_path("asset")
        dirs = os.listdir(self.my_path)
        col = 0
        row = 0
        self._set_table_for_asset_list()
        for dir in dirs:
            self.ui.tableWidget_files.setRowCount(row + 1)
            if not os.path.isdir(f"{self.my_path}/{dir}"):
                if dir[0] == '.' :
                    continue
                cell = self._make_asset_cell(dir)
            else : 
                if dir[0] == '.' :
                    continue
                cell = self._make_asset_dir_cell(dir)
            self.ui.tableWidget_files.setCellWidget(row, col, cell)
            self.ui.tableWidget_files.setRowHeight(row,206)
            col += 1
            if col == 3:
                col = 0
                row += 1

    def _set_content_table_widget(self):
        """
        treeWidget_content의 아이템이 선택되었을 때 tableWidget_files에
        이에 해당하는 파일들을 보여주는 메서드
        """
        cur_item = self.ui.treeWidget_content.currentItem()

        if cur_item == None:
            # current item이 없는 경우에는 기본적으로 All Content를 선택하여 출력하도록 한다
            cur_item = self.ui.treeWidget_content.findItems("All Content", Qt.MatchFlag.MatchExactly, 0)[0]
            self.ui.treeWidget_content.setCurrentItem(cur_item, 0)
            
        cur_file_type = cur_item.text(0)
         
        row = 0
        if cur_file_type == 'All Content':
            self._set_table_for_file_list()
            for data in self.content_files_data.keys():
                self.ui.tableWidget_files.setRowCount(row + 1)
                cell = self._make_file_cell(data)
                self.ui.tableWidget_files.setCellWidget(row, 0, cell)
                self.ui.tableWidget_files.setRowHeight(row,50)
                row += 1
        else :
            col = 0
            self._set_table_for_content_list()
            for file, data in self.content_files_data.items():
                if data['published_file_type']['name'] == cur_file_type:
                    self.ui.tableWidget_files.setRowCount(row + 1)
                    cell = self._make_asset_cell(file)
                    self.ui.tableWidget_files.setCellWidget(row, col, cell)
                    self.ui.tableWidget_files.setRowHeight(row,206)
                    if col == 3:
                        col = 0
                        row += 1


####################################################################################################


######################### 파일 로드, 생성 등과 연관된 메서드 ##################################################

    def _find_dir_name_in_tree(self, row, col):
        """
        tableWidget에서 cell이 선택되었을 때 해당 cell의 값이
        현재 보여지는 tabWidget 내부의 treewidget에 item으로 존재한다면
        treeWidget에서 해당 아이템을 선택하고
        아이템이 존재하지 않는다면 해당 파일이 존재하는 지를 확인하고
        존재하면 파일을 열고 존재하지 않는다면 새로운 파일을 생성한다
        """
        cell = self.ui.tableWidget_files.cellWidget(row, col)
        item_text = cell.findChild(QLabel, "name_label").text()
        
        current_tab = self.ui.tabWidget_task.currentWidget()
        current_treeWidget = current_tab.findChildren(QTreeWidget)[0]

        cur_item = current_treeWidget.currentItem()
        item = None

        if current_treeWidget.objectName() == "treeWidget_content":
            path = self.content_files_data[item_text]['path']['local_path']
            self.OPEN_FILE.emit(path)
            return

        if not cur_item:
            item = current_treeWidget.findItems(item_text, Qt.MatchExactly, 0)[0]
                
        if not item:
            for i in range(0, cur_item.childCount()):
                child = cur_item.child(i)
                if child.text(0) == item_text:
                    item = child
                    break

        if not item :
            path = f"{self.my_path}{item_text}"
            if os.path.isdir(path) :
                return
            if not os.path.exists(path) :
                self._create_new_file(path)
                return
            self.OPEN_FILE.emit(f"{self.my_path}{item_text}")
            if self.tool : self.close()
        else : 
            current_treeWidget.setCurrentItem(item, 0)
            current_treeWidget.currentItem().setExpanded(True)
        
    def _create_new_file(self, path):
        """
        경로를 받아와서 어떤 파일을 생성하는 지 확장자로 판단하여
        새로운 파일을 생성하고 해당 파일을 open한다
        """
        # print(self.my_path) # /home/rapa/baked/show/baked/SEQ/ABC/ABC_0020/LGT/dev/
        _, ext = os.path.splitext(path)

        # 파일 확장자에 따라 세부 경로 지정 ********************************
        if ext in [".nknc", "nk"]:
            path = f"{self.my_path}nuke/scenes/"
        elif ext in [".mb"]:
            path = f"{self.my_path}maya/scenes/"
        else :
            return

        if not os.path.exists(path):
            os.makedirs(path)
        
        working = self.sg.user_info['asset']
        if not working :
            working = self.sg.user_info['shot']

        new_file_path = f"{path}{working}_{self.sg.user_info['task']}_v001{ext}"

        # 새로운 파일이 생성되는 방식을 작성 ************************************************
        if ext in [".nknc", "nk"]:
            with open(new_file_path, "w") as file:
                pass
        elif ext in [".mb"]:
            os.system(f"cp /home/rapa/baked/toolkit/config/core/maya/empty_mb_file.mb {new_file_path}")
        else :
            return
       
        self.OPEN_FILE.emit(new_file_path)

        if self.tool:
            self.close()

    def _open_file_from_loader(self, path):
        """
        file Open을 담당하는 class 생성 path(str)값 전달
        """
        FileOpen(path, self.tool) # file_open.py


######################### table cell, row, col, 등등과 연관된 메서드 ##################################################

    def _make_dir_cell(self, dir_name, w=30, h=30):
        """
        dir icon이 뜨는 dir cell을 생성하고 return하는 메소드
        """
        cell = QWidget()
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)

        img_label = self._make_icon(f"{os.path.dirname(__file__)}/icons/folder.png", w, h)

        name_label = QLabel()
        name_label.setObjectName("name_label")
        name_label.setText(dir_name)

        layout.addWidget(img_label)
        layout.addWidget(name_label)

        cell.setLayout(layout)
        return cell
    
    def _make_asset_dir_cell(self, dir_name):
        """
        asset table 구조에서 dir icon이 뜨는 dir cell을 생성하고 return하는 메소드
        """
        cell = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        img_label = self._make_icon(f"{os.path.dirname(__file__)}/icons/folder.png")

        name_label = QLabel()
        name_label.setObjectName("name_label")
        name_label.setText(dir_name)
        name_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(img_label)
        layout.addWidget(name_label)

        cell.setLayout(layout)
        return cell
    
    def _make_icon(self, path, w=None, h=None):
        """
        path가 가리키는 이미지를 label에 설정하여
        해당 label을 return하는 메서드
        """
        img_label = QLabel()
        img_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(path)
        if w and h:
            pixmap = pixmap.scaled(w, h)
        img_label.setPixmap(pixmap)
        img_label.setScaledContents(True)

        return img_label
        
    def _make_file_cell(self, file_name):
        """
        file의 ext를 통해 해당 확장자에 맞는 이미지를 아이콘으로 하는 cell을 생성하고 return 한다
        """
        cell = QWidget()
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)

        ext = file_name.split('.')[-1]
        img_label = self._make_icon(f"{os.path.dirname(__file__)}/icons/{ext}.png", 30, 30)

        name_label = QLabel()
        name_label.setObjectName("name_label")
        name_label.setText(file_name)

        layout.addWidget(img_label)
        layout.addWidget(name_label)

        cell.setLayout(layout)
        return cell
    
    def _make_asset_cell(self, file_name):
        """
        asset의 썸네일 데이터를 가져와 이미지로 설정하는 cell을 생성하고 return한다
        """
        cell = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        dir_path = self._get_current_item_path("asset")
        name, ext = os.path.splitext(file_name)
        path = f"{dir_path}/.thumbnail/{name}.png"
        if not os.path.exists(path) :
            path = f"{os.path.dirname(__file__)}/icons/{ext.split('.')[-1]}.png"

        img_label = self._make_icon(path, 100, 100)

        name_label = QLabel()
        name_label.setObjectName("name_label")

        name_label.setText(file_name)
        name_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(img_label)
        layout.addWidget(name_label)

        cell.setLayout(layout)
        return cell

    def _set_table_for_file_list(self):
        file_table = self.ui.tableWidget_files
        file_table.clear()
        file_table.setColumnCount(1)
        file_table.setColumnWidth(0, 620)

    def _set_table_for_asset_list(self):
        file_table = self.ui.tableWidget_files
        file_table.clear()
        file_table.setColumnCount(3)
        file_table.setColumnWidth(0, 206)
        file_table.setColumnWidth(1, 206)
        file_table.setColumnWidth(2, 206)

    def _set_table_for_content_list(self):
        file_table = self.ui.tableWidget_files
        file_table.clear()
        file_table.setColumnCount(2)
        file_table.setColumnWidth(0, 309)
        file_table.setColumnWidth(1, 309)

#####################################################################################

        


######################### main() ##################################################
        
if __name__ == "__main__":
    app = QApplication()
    win = Loader(Shotgrid_Data())
    win.show()
    app.exec()