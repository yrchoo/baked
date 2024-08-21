
try :
    from PySide6.QtWidgets import QApplication, QWidget, QTreeWidgetItem
    from PySide6.QtWidgets import QTreeWidget, QLabel, QHBoxLayout
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import QFile, Qt, Signal
    from PySide6.QtGui import QPixmap

except:
    from PySide2.QtWidgets import QApplication, QWidget, QTreeWidgetItem
    from PySide2.QtWidgets import QTreeWidget
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtCore import QFile, Qt, Signal
    from PySide2.QtGui import QPixmap

import os

# test

try :
    from shotgrid.get_shotgrid_data import Shotgrid_Data
except :
    from get_shotgrid_data import Shotgrid_Data

class Loader(QWidget):
    OPEN_FILE = Signal(str)

    def __init__(self, sg : Shotgrid_Data, tool : str = None):
        super().__init__()
        self._set_init_val(sg, tool)
        self._set_ui()
        self._set_tree_widget_data()
        self._set_my_task_table_widget()

    def _set_init_val(self, sg, tool):
        self.project_name = "baked"
        self.py_file_path = os.path.dirname(__file__)
        self.sg : Shotgrid_Data = sg 
        self.project_path = f"/home/rapa/baked/show/{self.project_name}"
        self.tool = tool

    def _set_ui(self):
        ui_file_path = f"{self.py_file_path}/loader.ui"
        ui_file = QFile(ui_file_path)
        ui_file.open(QFile.ReadOnly)

        ui_loader = QUiLoader()
        self.ui = ui_loader.load(ui_file, self)

        self.ui.setWindowFlags(self.ui.windowFlags() | Qt.WindowStaysOnTopHint)

        ui_file.close()
        # self.show()

    def _set_tree_widget_data(self):
        if not self.sg.connected : # Shotgrid connection failed...
            self._set_seq_tree_widget_by_path()
            self._set_asset_tree_widget_by_path()
            self._set_task_tree_widget_by_path()
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
        seqs = self.sg.get_sequences_entities()
        for seq in seqs:
            seq_item = self._add_tree_item(seq_tree, seq['code'])
            shots = self.sg.get_shot_from_seq(seq)
            for shot in shots:
                shot_item = self._add_tree_item(seq_item, shot['code'])
                tasks = self.sg.get_task_from_ent(shot)
                for task in tasks:
                    self._add_tree_item(shot_item, task['content'])

    def _set_asset_tree_widget_by_shotgrid(self):
        asset_tree = self.ui.treeWidget_asset
        assets = self.sg.get_asset_entities()
        
        for asset in  assets:
            grp = asset['sg_asset_type']
            grp_list = asset_tree.findItems(grp, Qt.MatchExactly, 0)
            if len(grp_list) == 0:
                parent_item = QTreeWidgetItem(asset_tree)
                parent_item.setText(0, grp)
            else :
                parent_item = grp_list[0]
            asset_item = self._add_tree_item(parent_item, asset['code'])
            tasks = self.sg.get_task_from_ent(asset)
            for task in tasks:
                self._add_tree_item(asset_item, task['content'])
    
    def _add_tree_item(self, parent_item, text):
        item = QTreeWidgetItem(parent_item)
        item.setText(0, text)
        return item

    def _set_task_tree_widget_by_shotgrid(self):
        task_tree = self.ui.treeWidget_task
        my_work = self.sg.user_info["SHOT"]

        if not my_work :
            my_work = self.sg.user_info["ASSET"]
            work_item = self._add_tree_item(task_tree, my_work)
        else :
            work_item = self._add_tree_item(task_tree, my_work)

        my_task = self.sg.user_info["TASK"]
        task_item = self._add_tree_item(work_item, my_task)

        my_task_path = self._get_path()
        self._add_to_tree_widget_by_path_recursive(task_item, my_task_path)

        # tasks = self.sg.get_assigned_task()
        # for task in tasks:
        #     # task = {'id': 1269, 'name': 'ABC_0010', 'type': 'Shot'}
        #     # task = {'id': 1451, 'name': 'Banana', 'type': 'Asset'}
        #     if task['type'] == 'Shot' :
        #         # task의 Seq 또는 Asset을 구해서
        #         # 부모 아이템으로 추가한 다음에
        #         # 그 아래에 해당 shot, task 들을 추가하기...
        #         seq_ent = self.sg.get_seq_from_shot(task)
        #         seq_list = task_tree.findItems(seq_ent['code'], Qt.MatchExactly, 0)
        #         if len(seq_list) == 0:
        #             parent_item = self._add_tree_item(task_tree, seq_ent['code'])
        #         else :
        #             parent_item = seq_list[0]
        #         self._add_tree_item(parent_item, task['name'])

        #         # task_item = QTreeWidgetItem(shot_item)
        #         # task_item.setText(0, self.sg.user_info['task'])    
        #     elif task['type'] == 'Asset':
        #         # Asset Group을 구해서
        #         asset = self.sg.get_asset_entity(task)
        #         # 해당 Group을 부모 아이템으로 추가한 다음에
        #         # 그 아래에 asset, task 들을 추가하기...
        #         grp = asset['sg_asset_type']
        #         grp_list = task_tree.findItems(grp, Qt.MatchExactly, 0)
        #         if len(grp_list) == 0:
        #             parent_item = self._add_tree_item(task_tree, grp)
        #         else :
        #             parent_item = grp_list[0]
        #         self._add_tree_item(parent_item, task['name'])
        #         # task_item = QTreeWidgetItem(asset_item)
        #         # task_item.setText(0, self.sg.user_info['task'])

    def _set_task_tree_widget_by_path(self):
        task_tree = self.ui.treeWidget_task
        # 현재 task 경로 가져와서 그냥... recursive path로 tree 추가하는 함수 호출하기

    def _open_file(self, path):
        self.OPEN_FILE.emit(path)

    def _open_file_from_loader(self, path):
        if self.tool : return
        # file Open을 담당하는 class 생성 path(str)값 전달
        #

    def _get_path(self):
        path = f'/home/rapa/baked/show/baked/SEQ/{self.sg.user_info["SEQ"]}/{self.sg.user_info["SHOT"]}/{self.sg.user_info["TASK"]}/dev'
        return path
    
    def _set_my_task_table_widget(self):
        path = self._get_path()
        dirs = os.listdir(path)
        row = 0
        self._set_table_for_file_list()
        for dir in dirs:
            self.ui.tableWidget_files.setRowCount(row + 1)
            if not os.path.isdir(f"{path}/{dir}"):
                if dir[0] == '.' :
                    continue
                cell = self._make_file_cell(dir)
            else : cell = self._make_dir_cell(dir)
            self.ui.tableWidget_files.setCellWidget(row, 0, cell)
            self.ui.tableWidget_files.setRowHeight(row,50)
            row += 1

    def _add_tree_widget_cell(self, parent_item, text):
        item = QTreeWidgetItem(parent_item)
        item.setText(0, text)


    def _find_dir_name_in_tree(self, dir_name):
        pass

    def _make_dir_cell(self, dir_name):
        cell = QWidget()
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)

        img_label = self._make_icon(f"{os.path.dirname(__file__)}/icons/folder.png")

        name_label = QLabel()
        name_label.setText(dir_name)

        layout.addWidget(img_label)
        layout.addWidget(name_label)

        cell.setLayout(layout)
        return cell
    
    def _make_icon(self, path):
        img_label = QLabel()
        pixmap = QPixmap(path)
        print(path)
        scaled_pixmap = pixmap.scaled(30, 50)
        img_label.setPixmap(scaled_pixmap)

        return img_label
        
    def _make_file_cell(self, file_name):
        cell = QWidget()
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)

        ext = file_name.split('.')[-1]
        img_label = self._make_icon(f"{os.path.dirname(__file__)}/icons/{ext}.png")

        name_label = QLabel()
        name_label.setText(file_name)

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
        
        
        


if __name__ == "__main__":
    app = QApplication()
    win = Loader(Shotgrid_Data("baked"))
    win.show()
    app.exec()