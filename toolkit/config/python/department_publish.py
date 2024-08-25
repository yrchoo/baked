try:
    from PySide6.QtWidgets import QApplication, QWidget
    from PySide6.QtWidgets import QTreeWidgetItem, QMessageBox
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import QFile, Qt
    from PySide6.QtGui import QIcon, QPixmap, QFont
    import sys, os, yaml
    from shotgun_api3 import shotgun
    # from work_in_maya import MayaAPI
    import department_publish 
except:
    from PySide2.QtWidgets import QApplication, QWidget
    from PySide2.QtWidgets import QTreeWidgetItem, QMessageBox
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtCore import QFile, Qt
    from PySide2.QtGui import QIcon, QPixmap, QFont
    import sys, os, yaml
    import maya.cmds as cmds
    from shotgun_api3 import shotgun
    from work_in_maya import MayaAPI
try:
    import maya.cmds as cmds
except:
    import nuke

class DepartmentTree():
    def __init__(self, treewidget, tool):
        self.tree = treewidget
        self.tool = tool

        data = self.make_data()
        if not data:
            return
        self.put_data_in_tree(data)
        self.initial_tree_setting()
        
        path = "/home/rapa/,,./maya"
        from maya_ligpub_set import PubSet
        PubSet.export_rig_mb(path)

    def put_data_in_tree(self, data_dict):
        
        items = self.check_selection()
        file_name = self.get_current_file_name()

        file_parent = QTreeWidgetItem(self.tree)
        file_parent.setText(0, file_name)
        self._set_text_bold(file_parent)

        for item in data_dict:
            parent = QTreeWidgetItem(file_parent)
            parent.setText(0, item)
            parent.setText(1, "")
            parent.setText(2, "")
            parent.setFlags(parent.flags() | Qt.ItemIsUserCheckable)
            parent.setCheckState(1, Qt.Checked)
            self.put_icon("3d", parent)
            self._set_text_bold(parent)
            self._make_tree_item("ㄴ Publish to Flow", parent)
            self._make_tree_item("ㄴ Upload for reivew", parent)
        self.tree.expandAll()
        print (data_dict.keys())
        return data_dict.keys()
    
    def _make_tree_item(self, text, parent):
        """트리 위젯 아이템 만드는 메서드"""
        self.tree.setStyleSheet("QTreeWidget {font-size:12px}")
        item = QTreeWidgetItem(parent, [f"{text}", "", ""])
        item.setFlags(parent.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(2, Qt.Checked)
        font = QFont()
        font.setPointSize(10)
        item.setFont(0, font)
    
    def _set_text_bold(self, item):
        font = QFont()
        font.setBold(True)
        item.setFont(0, font)
    
    def initial_tree_setting(self):
        """트리위젯 초기 설정"""
        self.tree.setColumnCount(3)
        self.tree.setColumnWidth(0,200)
        self.tree.setColumnWidth(1,20)
        self.tree.setColumnWidth(2,20)

    def get_current_file_name(self):
        pass
    
    def put_icon(self, data_type, item):
        image_path  = f"/home/rapa/baked/toolkit/config/python/{data_type}.png"
        icon = QIcon(QPixmap(image_path))
        item.setIcon(0, icon)

    def make_data(self):
        pass

    def check_selection(self):
        """선택한 object/node 확인하는 메서드"""
        if self.tool == "maya":
            selected_data = MayaAPI.get_selected_objects(self)
        else:
            selected_data = nuke.selectedNode()
        if selected_data:
            return selected_data
        self._show_message_to_select_item()
        return
    
    def get_current_file_name(self):
        if self.tool == "maya":
            return MayaAPI.get_file_name(self)
        else:
            return nuke.basename() #####

    def _show_message_to_select_item(self):
        msg = QMessageBox()
        msg.setWindowTitle("Important")
        msg.setText("Please select the data to publish")
        msg.setIcon(QMessageBox.Information)
        msg.setDefaultButton(QMessageBox.Yes)
        msg.exec()    
        return None


class Modeling(DepartmentTree):
    """Publish Data: mb, mov(턴테이블)/ jpg(playblast)"""
    def make_data(self):
        """데이터 : mb"""
        selected_data = self.check_selection()
        data_dict = {}
        try: 
            for data in selected_data:
                data_dict[data] = "mb"
        except:
            return
        return data_dict

# class Rigging(DepartmentTree):
#     """Publish Data: mb, mov(턴테이블)/ jpg(playblast)"""
#     def make_data(self):
#         selected_data = self.check_selection()
#         for data in selected_data:
#             pass

# class Lookdev(DepartmentTree):
#     """Publish Data: mb, """

# class Animation(DepartmetTree):
#     """Publish Data: cache, camera, playblast"""
#     def make_data(self):
#         selected_data = self.check_selection()
#         pass

# class Matchmove(DepartmentTree):

# class Lighting(DepartmentTree):

# class FX()
