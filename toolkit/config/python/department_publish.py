try:
    from PySide6.QtWidgets import QTreeWidgetItem
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QFont, QBrush, QColor
except:
    from PySide2.QtWidgets import QTreeWidgetItem
    from PySide2.QtCore import Qt
    from PySide2.QtGui import QFont, QBrush, QColor
    
try:
    from work_in_maya import MayaAPI
except:
    import work_in_nuke as NukeAPI
import work_in_nuke as NukeAPI
from work_in_maya import MayaAPI
import os

class DepartmentWork():
    """
    DepartmentWork
    1. 각 부서별로 공통되는 메서드를 구현하기 위한 부모 클래스입니다.
    2. 기능:
        - 트리위젯으로 부서별로 필요한 정보들을 구성합니다.
        -  """
    def __init__(self, treewidget, tool):
        print (treewidget)
        self.tree = treewidget
        self.tool = tool
        self.maya = MayaAPI()
        if treewidget:
            self.initial_tree_setting()
        
    def initial_tree_setting(self):
        """트리위젯 초기 설정"""
        self.tree.setColumnCount(2)
        self.tree.setColumnWidth(0,250)
        self.tree.setColumnWidth(1,10)

    def put_data_in_tree(self, publish_dict):
        """아이템을 트리위젯에 넣는 메서드"""
        file_name = self.get_current_file_name()
        file_parent = QTreeWidgetItem(self.tree)
        file_parent.setText(0, file_name)
        file_parent.setText(1, "ㅡ")
        file_parent.setForeground(1, QBrush(QColor("sky blue")))
        self._set_text_bold(file_parent)
        # publish_dict = self.make_data()
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
        self.tree.expandAll()
  

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
            selected_data = self.maya.get_selected_objects()
        elif self.tool == "nuke":
            selected_data = NukeAPI.get_selected_write_nodes()
        if selected_data:
            return selected_data
    
    def get_current_file_name(self):
        """ 현재 작업하고 있는 파일 이름을 가져오는 메서드"""  ### 이런 if문 너무 별로
        if self.tool == "maya":
            return self.maya.get_file_name()
        elif self.tool == "nuke":
            return NukeAPI.get_file_name()
        
    """ 부모클래스에 디폴트 값으로 렌더, 캡쳐, 플레이블라스트 확장자를 선언하고, 
        만약 부서별로 다른 확장자로 렌더/플레이블라스트를 export 하고 싶을 때 
        부서별 자식 클래스에서 오버라이드를 통해 확장자를 수정해준다 
        eg) pub을 하기위해 modeling은 렌더할때 턴테이블 (mov) 로 하지만 lighting은 렌더할때 (exr)로 하기 때문에"""

    """렌더 확장자는 다양하기 때문에 파이프라인으로 확장자를 정해서 자동으로 렌더되게 구조화함"""

    def set_render_ext(self):
        """ 턴테이블 확장자 정해주는 메서드 """
        return "jpg"
    
    def save_scene_file(self, new_path):
        if self.tool == "maya":
            self.maya.save_file( new_path)
        elif self.tool == "nuke":
            NukeAPI.save_file(new_path)
        print (f"&&&&&&&&&&&&&&&&& {new_path}")
    
    def save_as_alembic(self, alembic_path, file):
        self.maya.export_alemibc(alembic_path, file)

    def save_camera_as_alembic(self, alembic_path, file):
        self.maya.export_alemibc(alembic_path, file)
    
    def render_as_exr(self, path):
        self.maya.render_exr_sequence(path)

class MOD(DepartmentWork):
    def make_data(self):
        """ 선택된 object/node 가져오는 메서드 """
        selected_data = self.check_selection()
        publish_dict = {self.get_current_file_name():{'description':'', 'file type':'', 'ext': '', 'path':''}}
        try:
            for data in selected_data:
                publish_dict[data] = {'description':'', 'file type':'', 'ext': '', 'path':''}
        except: 
            pass
        self.put_data_in_tree(publish_dict)
        return publish_dict
    
    def render_data(self, render_path):
        # self.maya_api = 
        print (render_path)
        print (os.path.splitext(render_path))
        self.maya.render_turntable(render_path)

    def get_ready_for_publish(self):
        """ 퍼블리쉬 하기전 데이터 처리하는 메서드 """
        self.maya.modeling_publish_set()
    
    def save_data(self, publish_dict):
        """ 선택된 노드, 오브젝트 별로 export 하는 메서드 """
        self.get_ready_for_publish()
        scene_path = publish_dict[self.get_current_file_name()]['path']
        self.save_scene_file(scene_path)
        for file in publish_dict:
            if publish_dict[file]['file type'] == 'Model Cache': ### 이거 구려
                self.save_as_alembic(publish_dict[file]['path'], file)
        return publish_dict

class RIG(DepartmentWork):
    def make_data(self):
        """ 선택된 object/node 가져오는 메서드 """
        selected_data = self.check_selection()
        publish_dict = {self.get_current_file_name():{'description':'', 'file type':'', 'ext': '', 'path':''}}
        try:
            for data in selected_data:
                publish_dict[data] = {'description':'', 'file type':'', 'ext': '', 'path':''}
        except: 
            pass
        self.put_data_in_tree(publish_dict)
        return publish_dict
    
    def render_data(self, render_path):
        self.maya.render_turntable(render_path)

    def save_data(self, publish_dict):
        """ 선택된 노드, 오브젝트 별로 export 하는 메서드 """
        scene_path = publish_dict[self.get_current_file_name()]['path']
        self.save_scene_file(scene_path)
        return publish_dict

class LKD(DepartmentWork):
    """ Publish Data: mb, ma(shader), tiff(texture) """    
    def __init__(self, treewidget, tool):
        super().__init__(treewidget, tool)
        texture_list = self.maya.get_texture_list()
        shader_list = self.maya.get_custom_shader_list()
        self.lookdev_list = []
        self.lookdev_list.extend(texture_list)
        self.lookdev_list.extend(shader_list)
    
    def make_data(self):
        """ 쉐이더 텍스쳐 데이터 따로 가져오는 메서드 """
        """ 룩뎁인 경우 디스크립션이 하나면 되는데.. """

        publish_dict = {self.get_current_file_name():{'description':'', 'file type':'', 'ext': '', 'path':''}}
        ma_file = self.get_current_file_name().replace(".mb", ".ma")
        json_file = ma_file.replace(".ma", ".json")
        publish_dict[ma_file] = {'description':'', 'file type':'', 'ext': '', 'path':''}
        publish_dict[json_file] = {'description':'', 'file type':'', 'ext': '', 'path':''} ### json...
        self.put_data_in_tree(publish_dict)
        return publish_dict

    def set_render_ext(self): #######
        """ 렌더 확장자 정해주는 메서드 """

        return "exr"
    
    def render_data(self, render_path): #################################### exr rendering
        thumbnail_path = self.maya.render_turntable(render_path) 
        return thumbnail_path
    
    def save_data(self, publish_dict):
        scene_file = self.get_current_file_name()
        scene_path = publish_dict[scene_file]['path'].replace(".ma", ".mb")
        self.save_scene_file(scene_path) # mb

        ma_file = self.get_current_file_name().replace(".mb", ".ma")
        json_file = self.get_current_file_name().replace(".mb", ".json")
        ma_file_path = publish_dict[ma_file]['path']
        json_file_path = publish_dict[json_file]['path'].replace(".ma", ".json")

        publish_dict[json_file]['path'] = json_file
        publish_dict[scene_file]['path'] = scene_path # mb

        self.maya.export_shader(ma_file_path, json_file_path) #ma, #json
        print ("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
        print (scene_path)
        print (publish_dict)
        print (publish_dict[scene_file]['path'])
        print ("~~~", publish_dict)
        return publish_dict

class ANI(DepartmentWork): 
    def make_data(self):
        """ 선택된 object/node 가져오는 메서드 """
        selected_data = self.check_selection()
        publish_dict = {self.get_current_file_name():{'description':'', 'file type':'', 'ext': '', 'path':''}}
        try:
            for data in selected_data:
                publish_dict[data] = {'description':'', 'file type':'', 'ext': '', 'path':''}
        except: 
            pass
        self.put_data_in_tree(publish_dict)
        return publish_dict
    
    def set_render_ext(self):
        """ 렌더 확장자 정해주는 메서드 """
        return "exr"
    
    def render_data(self, path): ###################################### 카메라 설정..?
        self.maya.render_file(path)
    
    def save_data(self, publish_dict):
        scene_path = publish_dict[self.get_current_file_name()]['path']
        self.save_scene_file(scene_path)
        for file, info in publish_dict.items():
            if 'Cache' in info['file type'] :
                self.save_as_alembic(info['path'], file)
            elif info['file type'] in ['Camera']:
                self.save_camera_as_alembic(info['path'], file)
        return publish_dict

class LGT(DepartmentWork):
    """
    라이팅은 마야와 누크를 모두 사용하기 때문에 툴별로 UI에 보여주는 데이터가 다릅니다.
    """
    def make_data(self):
        if self.tool == 'maya':
            selected_data = self.maya._get_lighting_layers()
            publish_dict = {self.get_current_file_name():{'description':'', 'file type':'', 'ext': '', 'path':''}}
            try:
                for data in selected_data:
                    if not "default" in data:
                        publish_dict[data] = {'description':'', 'file type':'', 'ext': '', 'path':''}
            except: 
                pass
            self.put_data_in_tree(publish_dict)
        elif self.tool == "nuke":
            selected_data = NukeAPI.get_selected_write_nodes()
            publish_dict = {self.get_current_file_name():{'description':'', 'file type':'', 'ext': '', 'path':''}}
            try:
                for data in selected_data:
                    publish_dict[data.knob('name').value()] = {'description':'', 'file type':'', 'ext': '', 'path':''}
            except:
                pass
            self.put_data_in_tree(publish_dict)
        return publish_dict


    def set_render_ext(self):
        """ 렌더 확장자 정해주는 메서드 """
        return "exr"
    
    def save_data(self, publish_dict):
        """ 파일 타입별로 파일 저장하는 메서드 """
        for file, info in list(publish_dict.items()):
            if 'Lighting' in info['file type']:
                scene_path = publish_dict[self.get_current_file_name()]['path']
                self.save_scene_file(scene_path)
            elif 'EXR' in info['file type']: # 
                if self.tool == "maya":
                    print ("##", info['path'])
                    publish_dict = self.maya.render_all_layers_to_exr(file, publish_dict)
                elif self.tool == "nuke":
                    NukeAPI.render_selected_write_nodes_with_exr(info['path'], 1001, 1096)
                    # os.system(f'''nuke -t make_slate_mov_nuke.py -path "{info['path']}" -first "1001" -last "1096"''')
            elif 'Precomp' in info['file type']:
                scene_path = publish_dict[self.get_current_file_name()]['path']
                self.save_scene_file(scene_path)
        return publish_dict
    
    def render_data(self, image_path):
        # 누크에서는 바로 thumbnail을 render하지 않습니다
        pass


class MM(DepartmentWork):
    def make_data(self):
        selected_data = self.check_selection()
        publish_dict = {self.get_current_file_name():{'description':'', 'file type':'', 'ext': '', 'path':''}}
        try:
            for data in selected_data:
                publish_dict[data] = {'description':'', 'file type':'', 'ext': '', 'path':''}
        except: 
            pass
        self.put_data_in_tree(publish_dict)
        return publish_dict
    
    def set_render_ext(self):
        """ 렌더 확장자 정해주는 메서드 """
        return "exr"
    
    def save_data(self, publish_dict):
        scene_path = publish_dict[self.get_current_file_name()]['path']
        self.save_scene_file(scene_path)
        for file, info in publish_dict.items():
            if 'Camera' in file['file type']:
                self.save_as_alembic(info['path'])
            elif "Scene" in file['file type']:
                self.save_scene_file(info['path'])
        return publish_dict

class CMP(DepartmentWork):
    def make_data(self):
        """트리 위젯에 내보내는 데이터 모아두기"""
        selected_data = NukeAPI.get_selected_write_nodes()
        print ("###", selected_data)
        publish_dict = {self.get_current_file_name():{'description':'', 'file type':'', 'ext': '', 'path':''}}
        try:
            for data in selected_data:
                publish_dict[data.knob('name').value()] = {'description':'', 'file type':'', 'ext': '', 'path':''}
        except: 
            pass
        self.put_data_in_tree(publish_dict)
        return publish_dict
    
    def save_data(self, publish_dict):
        """데이터 저장하기"""
        scene_path = publish_dict[self.get_current_file_name()]['path']
        self.save_scene_file(scene_path) # nknc
        for file, info in list(publish_dict.items()):
            if 'EXR' in info['file type']: # 
                NukeAPI.render_selected_write_nodes_with_exr(info['path'], 1001, 1096)
            elif 'Comp' in info['file type']:
                scene_path = publish_dict[self.get_current_file_name()]['path']
                self.save_scene_file(scene_path)
        return publish_dict
    
class FX(DepartmentWork):
    def make_data(self):
        pass

