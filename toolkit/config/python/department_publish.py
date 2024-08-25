try:
    from PySide6.QtWidgets import QTreeWidgetItem, QMessageBox
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QIcon, QPixmap, QFont
except:
    from PySide2.QtWidgets import QTreeWidgetItem, QMessageBox
    from PySide2.QtCore import Qt
    from PySide2.QtGui import QIcon, QPixmap, QFont
    from work_in_maya import MayaAPI

class DepartmentTree():
    def __init__(self, treewidget, tool):
        self.tree = treewidget
        self.tool = tool

        data = self.make_data()
        self.initial_tree_setting()
        self.put_data_in_tree(data)
    
    def put_data_in_tree(self, data_dict):
        
        file_name = self.get_current_file_name()
        file_parent = QTreeWidgetItem(self.tree)
        file_parent.setText(0, file_name)
        self._set_text_bold(file_parent)

        data_dict[f"{file_name}.mov"] = "mov"

        for item in data_dict:
            parent = QTreeWidgetItem(file_parent)
            parent.setText(0, item)
            self._set_text_bold(parent)
            self._make_tree_item("ㄴ Publish to Flow", parent)
            self._make_tree_item("ㄴ Upload for reivew", parent)
        
        self.tree.expandAll()

        return data_dict
    
    def _make_tree_item(self, text, parent):
        """트리 위젯 아이템 만드는 메서드"""
        self.tree.setStyleSheet("QTreeWidget {font-size:12px}")
        item = QTreeWidgetItem(parent, [f"{text}", ""])
        item.setFlags(parent.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(1, Qt.Checked)
        font = QFont()
        font.setPointSize(10)
        item.setFont(0, font)
    
    def _set_text_bold(self, item):
        font = QFont()
        font.setBold(True)
        item.setFont(0, font)
    
    def initial_tree_setting(self):
        """트리위젯 초기 설정"""
        self.tree.setColumnCount(2)
        self.tree.setColumnWidth(0,250)
        self.tree.setColumnWidth(1,10)

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
    
    def get_current_file_name(self):
        if self.tool == "maya":
            return MayaAPI.get_file_name(self)
        else:
            return nuke.basename() #####
    
    def object_type_dictionary(self):
        # transform (group 노드인경우 ) => mb
        object_type_dict = MayaAPI.get_object_type
        print(object_type_dict)
        return object_type_dict
    

class Modeling(DepartmentTree):
    """Publish Data: mb, mov(턴테이블)/ jpg(playblast)"""
    def make_data(self):
        """publish 데이터 : mb"""
        selected_data = self.check_selection()
        data_dict = {}
        try: 
            for data in selected_data:
                data_dict[data] = "mb"
            return data_dict
        except:
            return
    
    def save_data(self):
        pass

class Rigging(DepartmentTree):
    def make_data(self):
        data_dict = ['mb', 'mov']


class Lighting(DepartmentTree):
    def make_data(self):
        pass

class Lookdev(DepartmentTree):
    """Publish Data: mb, """    
    pass

class Animation(DepartmentTree):
    def make_data(self):
        selected_data = self.check_selection()
        data_dict = {}
        for data in selected_data:
            data_dict[data] = "abc"
        return data_dict


# class Animation(DepartmetTree):
#     """Publish Data: cache, camera, playblast"""
#     def make_data(self):
#         selected_data = self.check_selection()
#         pass

# class Matchmove(DepartmentTree):

# class Lighting(DepartmentTree):

# class FX()
