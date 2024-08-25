
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

try :
    from shotgrid.get_shotgrid_data import Shotgrid_Data
except :
    from get_shotgrid_data import Shotgrid_Data
    
from file_open import FileOpen

class Loader(QWidget):
    OPEN_FILE = Signal(str)

    def __init__(self, sg : Shotgrid_Data, tool : str = None):
        super().__init__()
        self._set_init_val(sg, tool)
        self._set_ui()
        self._set_event()
        self._set_tree_widget_data()
        self._set_my_task_table_widget()

    def _set_init_val(self, sg, tool):
        # 다른 경로에서 작업하는 경우 test_path에 등록하고 self.home_path 변경하여 사용하세용
        test_path = {
            "rapa" : "/home/rapa/baked",
            "choo_mac" : "/Users/yerin/Desktop/NetflixAcademy/baked"
        }

        self.home_path = test_path["rapa"] # 다른 경로에서 작업할 때 변경할 부분입니다!

        self.project_name = "baked"
        self.py_file_path = os.path.dirname(__file__)
        self.sg : Shotgrid_Data = sg 
        self.project_path = f"{self.home_path}/show/{self.project_name}"
        self.tool = tool

    def _set_ui(self):
        ui_file_path = f"{self.py_file_path}/loader.ui"
        ui_file = QFile(ui_file_path)
        ui_file.open(QFile.ReadOnly)

        ui_loader = QUiLoader()
        self.ui = ui_loader.load(ui_file, self)

        if self.tool :
            self.setWindowFlags(Qt.WindowStaysOnTopHint) # tool 내에서 열릴 때에만 

        ui_file.close()
        # self.show()

    def _set_event(self):
        self.OPEN_FILE.connect(self._open_file_from_loader)

        self.ui.tableWidget_files.cellDoubleClicked.connect(self._find_dir_name_in_tree)

        self.ui.treeWidget_task.currentItemChanged.connect(self._set_my_task_table_widget)
        self.ui.treeWidget_task.itemClicked.connect(self._set_my_task_table_widget)

        self.ui.treeWidget_asset.currentItemChanged.connect(self._set_asset_table_widget)
        self.ui.treeWidget_asset.itemClicked.connect(self._set_asset_table_widget)

        self.ui.treeWidget_seq.currentItemChanged.connect(self._set_seq_table_widget)
        self.ui.treeWidget_seq.itemClicked.connect(self._set_seq_table_widget)

        self.ui.tabWidget_task.currentChanged.connect(self._change_table_data)

    def _change_table_data(self, index):
        if index == 0:
            self._set_my_task_table_widget()
        elif index == 1:
            self._set_seq_table_widget()
        elif index == 2:
            self._set_asset_table_widget()

    def _set_tree_widget_data(self):
        if not self.sg.connected : # Shotgrid connection failed...
            self._set_seq_tree_widget_by_path()
            self._set_asset_tree_widget_by_path()
        else : # Shotgrid connected
            self._set_seq_tree_widget_by_shotgrid()
            self._set_asset_tree_widget_by_shotgrid()
            self._set_task_tree_widget_by_shotgrid()

    def _set_seq_tree_widget_by_path(self):
        seq_tree = self.ui.treeWidget_seq
        self._add_to_tree_widget_by_path_recursive(seq_tree, f"{self.project_path}/SEQ")

    def _set_asset_tree_widget_by_path(self):
        seq_asset = self.ui.treeWidget_asset
        self._add_to_tree_widget_by_path_recursive(seq_asset, f"{self.project_path}/AST")

    def _add_to_tree_widget_by_path_recursive(self, parent_item, addr):
        child_dirs = []
        if os.path.isdir(addr) : child_dirs = os.listdir(addr)
        for child in child_dirs:
            if not os.path.isdir(f"{addr}/{child}") : 
                continue
            item = self._add_tree_item(parent_item, child)
            path = f"{addr}/{child}"
            self._add_to_tree_widget_by_path_recursive(item, path)

    def _set_seq_tree_widget_by_shotgrid(self):
        seq_tree = self.ui.treeWidget_seq
        self.seq_data = {
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
                    seq_path = self._get_path(self.seq_data)
                    self._add_to_tree_widget_by_path_recursive(task_item, seq_path)

    def _set_asset_tree_widget_by_shotgrid(self):
        asset_tree = self.ui.treeWidget_asset
        assets = self.sg.get_asset_entities()
        self.asset_data = {
            "project" : self.sg.user_info["project"],
            "sequence" : None,
            "shot" : None,
            "asset" : None,
            "task" : None,
            "asset_type" : None
        }
        
        for asset in  assets:
            self.asset_data["asset_type"] = asset['sg_asset_type']
            grp_list = asset_tree.findItems(self.asset_data["asset_type"], Qt.MatchExactly, 0)
            if len(grp_list) == 0:
                parent_item = self._add_tree_item(asset_tree, self.asset_data["asset_type"])
            else :
                parent_item = grp_list[0]
            self.asset_data["asset"] = asset['code']
            asset_item = self._add_tree_item(parent_item, asset['code'])
            tasks = self.sg.get_task_from_ent(asset)
            for task in tasks:
                self.asset_data["task"] = task['content']
                task_item = self._add_tree_item(asset_item, task['content'])
                asset_path = self._get_path(self.asset_data)
                self._add_to_tree_widget_by_path_recursive(task_item, asset_path)
    
    def _add_tree_item(self, parent_item, text):
        item = QTreeWidgetItem(parent_item)
        item.setText(0, text)
        return item

    def _set_task_tree_widget_by_shotgrid(self):
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


    def _open_file(self, path):
        self.OPEN_FILE.emit(path)

    def _open_file_from_loader(self, path):
        # if self.tool : return
        # file Open을 담당하는 class 생성 path(str)값 전달
        FileOpen(path, self.tool)
        

    def _open_yaml_file(self):
        with open(f'{self.home_path}/toolkit/config/core/env/open_path.yml') as f:
            yaml_data = yaml.load(f, Loader=yaml.FullLoader)
            yaml_path = yaml_data["paths"]
        return yaml_path

    def _get_path(self, path_data=None):
        if not path_data:
            path_data = self.sg.user_info
        yaml_path = self._open_yaml_file()

        if path_data["asset"] :
            level = "asset"
            current = "asset_path"
            root_path = yaml_path["asset_root"]
        else:
            level = "sequence"
            current = "sequence_path"
            root_path = yaml_path["sequence_root"]

        if "name" in path_data.keys():
            current = f"my_{current}"
        
        new_path = yaml_path[current]["definition"].replace(f"@{level}_root", root_path)
        new_path = new_path.format(**path_data)
        
        return new_path
    
    def _set_my_task_table_widget(self):
        self.my_path = self._get_path()
        item = self.ui.treeWidget_task.currentItem()
        sub_path = ""
        while item :
            text = item.text(0).split('/')[-1]
            if text in self.sg.user_info.values():
                break
            sub_path = f"{text}/{sub_path}"
            item = item.parent()
        self.my_path = f"{self.my_path}/{sub_path}"
        dirs = os.listdir(self.my_path)
        row = 0
        self._set_table_for_file_list()
        for dir in dirs:
            self.ui.tableWidget_files.setRowCount(row + 1)
            if not os.path.isdir(f"{self.my_path}/{dir}"):
                if dir[0] == '.' :
                    continue
                cell = self._make_file_cell(dir)
            else : 
                if dir[0] == '.' :
                    continue
                cell = self._make_dir_cell(dir)
            self.ui.tableWidget_files.setCellWidget(row, 0, cell)
            self.ui.tableWidget_files.setRowHeight(row,50)
            row += 1

    def _set_seq_table_widget(self):
        """
        현재 table에 띄우는 값이 seq tab의 데이터인지 asset tab인지를 받아와서 출력하는 메서드
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
        현재 table에 띄우는 값이 seq tab의 데이터인지 asset tab인지를 받아와서 출력하는 메서드
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


    def _get_current_item_path(self, data):
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
        

    def _add_tree_widget_cell(self, parent_item, text):
        item = QTreeWidgetItem(parent_item)
        item.setText(0, text)

    def _find_dir_name_in_tree(self, row, col):
        cell = self.ui.tableWidget_files.cellWidget(row, col)
        item_text = cell.findChild(QLabel, "name_label").text()
        
        current_tab = self.ui.tabWidget_task.currentWidget()
        current_treeWidget = current_tab.findChildren(QTreeWidget)[0]

        cur_item = current_treeWidget.currentItem()
        item = None

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
            self._open_file(f"{self.my_path}{item_text}")
            if self.tool : self.close()
        else : 
            current_treeWidget.setCurrentItem(item, 0)
            current_treeWidget.currentItem().setExpanded(True)
        
    def _make_dir_cell(self, dir_name, w=30, h=30):
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
        img_label = QLabel()
        img_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(path)
        if w and h:
            pixmap = pixmap.scaled(w, h)
        img_label.setPixmap(pixmap)
        img_label.setScaledContents(True)

        return img_label
        
    def _make_file_cell(self, file_name):
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
        
        
        
if __name__ == "__main__":
    app = QApplication()
    win = Loader(Shotgrid_Data())
    win.show()
    app.exec()