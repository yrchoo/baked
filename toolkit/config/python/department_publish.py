try:
    from PySide6.QtWidgets import QTreeWidgetItem
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QFont, QBrush, QColor
except:
    from PySide2.QtWidgets import QTreeWidgetItem
    from PySide2.QtCore import Qt
    from PySide2.QtGui import QFont, QBrush, QColor

from work_in_maya import MayaAPI
from work_in_nuke import NukeAPI
from functools import partial

class DepartmentTree():
    def __init__(self, treewidget, tool):
        self.tree = treewidget
        self.tool = tool
        self.initial_tree_setting()
        
    def initial_tree_setting(self):
        """트리위젯 초기 설정"""
        self.tree.setColumnCount(2)
        self.tree.setColumnWidth(0,250)
        self.tree.setColumnWidth(1,10)

    def put_data_in_tree(self):
        """아이템을 트리위젯에 넣는 메서드"""
        file_name = self.get_current_file_name()
        file_parent = QTreeWidgetItem(self.tree)
        file_parent.setText(0, file_name)
        file_parent.setText(1, "ㅡ")
        file_parent.setForeground(1, QBrush(QColor("sky blue")))
        self._set_text_bold(file_parent)
        self._make_tree_item("Publish to Flow", file_parent)
        self._make_tree_item("Upload for review", file_parent)
        publish_dict = self.make_data()
        print (publish_dict)

        # 데이터가 없는 경우에도 오류없이 import 되게끔
        if not publish_dict:
            return
        for item in publish_dict: # 파일 (mb) 가장 앞에 있어서 빼주기
            if item == file_name:
                continue
            parent = QTreeWidgetItem(file_parent)
            parent.setText(0, item)
            parent.setText(1, "ㅡ")
            parent.setForeground(1, QBrush(QColor("sky blue")))
            self._set_text_bold(parent)
            self._make_tree_item("Publish to Flow", parent)
            self._make_tree_item("Upload for review", parent)
      
        self.tree.expandAll()
        publish_dict[file_name] = {'pub':True, 'rev':True, 'description':'', 'file type':'', 'ext':'', 'path':''}
        return publish_dict

    def make_data(self):
        """ 선택된 object/node 가져오는 메서드 """
        selected_data = self.check_selection()
        publish_dict = {self.get_current_file_name():{'pub':True, 'rev':False, 'description':'', 'file type':'', 'ext': '', 'path':''}}
        try:
            for data in selected_data:
                publish_dict[data] = {'pub':True, 'rev':True, 'description':'', 'file type':'', 'ext': '', 'path':''}
        except: 
            pass
        return publish_dict
        
    def _make_tree_item(self, text, parent):
        """ 트리 위젯 아이템 만드는 메서드 """
        self.tree.setStyleSheet("QTreeWidget {font-size:12px}")
        item = QTreeWidgetItem(parent, [f"{text}", ""])
        item.setFlags(parent.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(1, Qt.Checked)
        font = QFont()
        font.setPointSize(10)
        item.setFont(0, font)
        if parent.text(0) == self.get_current_file_name() and 'review' in text:
            item.setCheckState(1, Qt.Unchecked)
            item.setDisabled(1)

    def _set_text_bold(self, item):
        """ 선택된 아이템의 텍스트를 볼드체로 바꾸는 메서드"""
        font = QFont()
        font.setBold(True)
        item.setFont(0, font)

    def check_selection(self):
        """ 선택한 object/node 확인하는 메서드 """
        if self.tool == "maya":
            selected_data = MayaAPI.get_selected_objects(self)
        else:
            selected_data = NukeAPI.get_selected_write_nodes(self)
        if selected_data:
            return selected_data
    
    def get_current_file_name(self):
        """ 현재 작업하고 있는 파일 이름을 가져오는 메서드"""
        if self.tool == "maya":
            return MayaAPI.get_file_name(self)
        else:
            return NukeAPI.get_file_name() #####
    
class MOD(DepartmentTree):
    """ 겹치는 메서드 정리할 필요가 있음 .. 수정 중"""

    def get_ready_for_publish(self):
        """ 퍼블리쉬 하기전 데이터 처리하는 메서드 """
        pass

    def set_render_ext(self):
        """ 턴테이블 확장자 정해주는 메서드 """
        return "mov"
    
    def set_capture_ext(self):
        """ 캡쳐 확장자 정해주는 메서드 """
        return "jpg"
    
    def set_playblast_ext(self):
        """ 플레이블라스트 확장자 정해주는 메서드"""
        return "jpg"
    
    def save_data(self, publish_dict):
        """ 선택된 노드, 오브젝트 별로 export 하는 메서드 """
        pass
        # mb, cache 파일 따로 내보내기 

class Rigging(DepartmentTree):
    def get_ready_for_publish(self):
        """ 퍼블리쉬 하기전 데이터 처리하는 메서드 """
        pass

    def set_render_ext(self):
        """ 턴테이블 확장자 정해주는 메서드 """
        return "mov"
    
    def set_capture_ext(self):
        """ 캡쳐 확장자 정해주는 메서드 """
        return "jpg"
    
    def set_playblast_ext(self):
        """ 플레이블라스트 확장자 정해주는 메서드"""
        return "jpg"
    
    def save_data(self, new_path):
        pass

class Lookdev(DepartmentTree):
    """ Publish Data: mb, ma(shader), png(texture) """    
    def make_data(self):
        """ 쉐이더 텍스쳐 데이터 따로 가져오는 메서드 """
        pass

    def set_render_ext(self):
        """ 렌더 확장자 정해주는 메서드 """
        render_ext_dict = {}
        render_ext_dict["pub"] = "tiff"
        render_ext_dict["review"] = "jpg"
        return render_ext_dict
    
    def set_capture_ext(self):
        """ 캡쳐 확장자 정해주는 메서드 """
        return "jpg"
    
class Animation(DepartmentTree):
    def set_render_ext(self):
        """ 렌더 확장자 정해주는 메서드 """
        return "exr"
    
    def set_capture_ext(self):
        """캡쳐 확장자 정해주는 메서드"""
        return "jpg"
    
    def set_playblast_ext(self):
        """플레이블라스트 확장자 정해주는 메서드 """
        return "jpg"

class Lighting(DepartmentTree):
    def make_data(self):
        pass
    
    def set_render_ext(self):
        """ 렌더 확장자 정해주는 메서드 """
        return "exr"
    
    def set_capture_ext(self):
        """캡쳐 확장자 정해주는 메서드"""
        return "jpg"
    
    def set_playblast_ext(self):
        """ 플레이블라스트 확장자 정해주는 메서드 """
        return "jpg"

class Matchmove(DepartmentTree):
    def make_data(self):
        pass
    
    def set_render_ext(self):
        """ 렌더 확장자 정해주는 메서드 """
        return "exr"
    
    def set_capture_ext(self):
        """ 캡쳐 확장자 정해주는 메서드 """
        return "jpg"
    
    def set_playblast_ext(self):
        """ 플레이블라스 확장자 정해주는 메서드 """
        return "jpg"


class FX(DepartmentTree):
    def make_data(self):
        pass