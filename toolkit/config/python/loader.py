
try :
    from PySide6.QtWidgets import QApplication, QWidget, QTreeWidgetItem
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import QFile, Qt
except:
    from PySide2.QtWidgets import QApplication, QWidget, QTreeWidgetItem
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtCore import QFile, Qt

import os

try :
    from shotgrid.get_shotgrid_data import Shotgrid_Data
except :
    from get_shotgrid_data import Shotgrid_Data

class Loader(QWidget):
    def __init__(self, sg : Shotgrid_Data):
        super().__init__()
        self._set_init_val(sg)
        self._set_ui()
        self._set_tree_widget_data()

    def _set_init_val(self, sg):
        self.project_name = "baked"
        self.py_file_path = os.path.dirname(__file__)
        self.sg : Shotgrid_Data = sg 
        self.project_path = f"/home/rapa/baked/show/{self.project_name}"

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
            item = QTreeWidgetItem(parent_item)
            item.setText(0, child)
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
            asset_item = self._add_tree_item(asset_tree, asset['code'])
            tasks = self.sg.get_task_from_ent(asset)
            for task in tasks:
                self._add_tree_item(asset_item, task['content'])
    
    def _add_tree_item(self, parent_item, text):
        item = QTreeWidgetItem(parent_item)
        item.setText(0, text)
        return item

    def _set_task_tree_widget_by_shotgrid(self):
        task_tree = self.ui.treeWidget_task

        tasks = self.sg.get_assigned_task()
        for task in tasks:
            # task = {'id': 1269, 'name': 'ABC_0010', 'type': 'Shot'}
            # task = {'id': 1451, 'name': 'Banana', 'type': 'Asset'}
            if task['type'] == 'Shot' :
                # task의 Seq 또는 Asset을 구해서
                # 부모 아이템으로 추가한 다음에
                # 그 아래에 해당 shot, task 들을 추가하기...
                # item = QTreeWidgetItem(task_tree)
                # item.setText(0, child)  
                seq_ent = self.sg.get_seq_from_shot(task)
                seq_list = task_tree.findItems(seq_ent['code'], Qt.MatchExactly, 0)
                if len(seq_list) == 0:
                    parent_item = QTreeWidgetItem(task_tree)
                    parent_item.setText(0, seq_ent['code'])
                else :
                    parent_item = seq_list[0]
                shot_item = QTreeWidgetItem(parent_item)
                shot_item.setText(0, task['name'])

                # task_item = QTreeWidgetItem(shot_item)
                # task_item.setText(0, self.sg.user_info['task'])    
            elif task['type'] == 'Asset':
                # Asset Group을 구해서
                asset = self.sg.get_asset_entity(task)
                # 해당 Group을 부모 아이템으로 추가한 다음에
                # 그 아래에 asset, task 들을 추가하기...
                grp = asset['sg_asset_type']
                grp_list = task_tree.findItems(grp, Qt.MatchExactly, 0)
                if len(grp_list) == 0:
                    parent_item = QTreeWidgetItem(task_tree)
                    parent_item.setText(0, grp)
                else :
                    parent_item = grp_list[0]
                asset_item = QTreeWidgetItem(parent_item)
                asset_item.setText(0, task['name'])

                # task_item = QTreeWidgetItem(asset_item)
                # task_item.setText(0, self.sg.user_info['task'])

    def _set_task_tree_widget_by_path(self):
        task_tree = self.ui.treeWidget_task
        


if __name__ == "__main__":
    app = QApplication()
    win = Loader(Shotgrid_Data("baked"))
    win.show()
    app.exec()