try:
    from PySide6.QtWidgets import QApplication, QWidget
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import QFile, Qt
    from PySide6.QtGui import QIcon, QPixmap, QFont
    import sys, os, yaml
    from shotgun_api3 import shotgun
    # from work_in_maya import MayaAPI
    import department_publish 
except:
    from PySide2.QtWidgets import QApplication, QWidget
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtCore import QFile, Qt
    from PySide2.QtGui import QBrush, QColor
    import sys, os, yaml
    import maya.cmds as cmds
    from shotgun_api3 import shotgun
    from work_in_maya import MayaAPI
    from work_in_nuke import NukeAPI
    import department_publish 
    from importlib import reload
    reload(department_publish)

class Publisher(QWidget):
    def __init__(self):
        super().__init__()
        self._set_ui()
        self._initial_setting()
        self._get_task_type()
        self._set_event()
        self.publish_dict = {}

    def _set_event(self):

        self.ui.checkBox_check.clicked.connect(self._select_all_items)

        self.ui.pushButton_collapse.clicked.connect(self._collapse_tree)
        self.ui.pushButton_expand.clicked.connect(self._expand_tree)
        self.ui.pushButton_publish.clicked.connect(self._publish_file_data)
        self.ui.pushButton_cancel.clicked.connect(self._cancel_and_close)
        self.ui.pushButton_load.clicked.connect(self._load_publish_summary)

        self.ui.comboBox_task.currentIndexChanged.connect(self._show_link_entity)
        self.ui.comboBox_type.currentIndexChanged.connect(self._put_publish_type_info_dict)

        self.ui.treeWidget.itemSelectionChanged.connect(self._show_file_detail)
        self.ui.treeWidget.itemClicked.connect(self._make_publish_info_dict)
        self.ui.treeWidget.itemChanged.connect(self._connect_check_state)

    def _set_ui(self):
        """ui 셋업해주는 메서드"""
        ui_file_path = '/home/rapa/baked/toolkit/config/python/publisher_final.ui' 
        ui_file = QFile(ui_file_path)
        ui_file.open(ui_file.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(ui_file, self)  
        ui_file.close()

    def _initial_setting(self):
        """초기 ui 세팅하는 메서드"""
        """tree에 데이터 넣기"""
        self.tree = self.ui.treeWidget
        self.tool = "maya" ##################

        department = self._get_user_info()['task']
        getattr(department_publish, department)(self.tree,'maya')    

        self.show()
        self._get_published_file_category()
        self.ui.checkBox_check.setChecked(True)
    
    def _show_file_detail(self):
        text = self.tree.currentItem().text(0)
        if text in ["Publish to Flow", "Upload for reivew"]:
            text = self.tree.currentItem().parent().text(0)
        self.ui.label_name.setText(text)
        self.ui.label_info.setText(f"file")
        self.ui.label_name.setAlignment(Qt.AlignLeft)
        self.ui.label_info.setAlignment(Qt.AlignLeft)

        # label_image = self.ui.label
        # data_type = 'grp'
        # pixmap = QPixmap(f"/home/rapa/baked/toolkit/config/python/{data_type}.png") 
        # scaled_pixmap = pixmap.scaled(50, 50) 
        # label_image.setPixmap(scaled_pixmap)

    def _expand_tree(self):
        """트리 위젯을 여는 메서드"""
        self.tree.expandAll()
        
    def _collapse_tree(self):
        """트리 위젯을 닫는 메서드"""
        self.tree.collapseAll()
    
    def _select_all_items(self):
        """모든 아이템 체크박스 선택되게/선택 안 되게 하는 메서드"""
        parent_count = self.tree.topLevelItemCount()
        for count_parent in range(parent_count): 
            child_count = self.tree.topLevelItem(count_parent).childCount() # object 개수
            for count in range(child_count):
                object = self.tree.topLevelItem(count_parent).child(count)
                child_ver = object.child(0)
                child_pub = object.child(1)
                if self.ui.checkBox_check.isChecked():
                    child_ver.setCheckState(1, Qt.Checked)
                    child_pub.setCheckState(1, Qt.Checked)
                else:
                    child_ver.setCheckState(1, Qt.Unchecked)
                    child_pub.setCheckState(1, Qt.Unchecked)

    def _connect_check_state(self, item, column):
        """publish 체크랑 review 체크 연동시키기"""
        if item.text(0) == "Upload for review":
            return
        if item.checkState(column) == Qt.Checked:
            parent = item.parent()
            parent.child(1).setCheckState(1, Qt.Checked)

    ##########################저장하고 버전 관리##################

    def _get_path_using_template(self):
        """템플릿을 이용해서 저장할 경로, 파일 이름 만드는 메서드"""

        ### abc 는 (버전그대로) 펍에 올라가고, mb파일, nknc 파일은 버전업돼서 저장되게
        yaml_path = self._import_yaml_template()
        file_info_dict = self._get_user_info()
        tool = file_info_dict["tool"]
        level = file_info_dict["seq/asset"]
        current = f"{tool}_{level}_pub"

        if current in yaml_path:
            root_path = yaml_path[f"{level}_root"]
            new_path = yaml_path[current]["definition"].replace(f"@{level}_root", root_path)
            new_path = new_path.format(**file_info_dict)   ### 각 키 이름 별로 딕셔너리랑 매칭되게 하는 겁니당
            self._check_validate(new_path)
        return new_path

    def _get_user_info(self):
        """유저에 대한 정보 가저오는 메서드"""
        user_file_info = {
                    "name":"Seoyeon Yoon",
                    "project":"baked",
                    "seq/asset":"asset",
                    "asset_type": "Character",
                    "asset":"Apple",
                    "task":"Modeling",
                    "dev/pub":"dev",
                    "tool":"maya",
                    "version":"001",
                    "filename":"desk_MOD_v001",
                    "maya_extension":"mb"}
        return user_file_info

    def _make_version_up(self):
        """버전 업해주는 메서드"""
        user_info = self._get_user_info()
        file_path = MayaAPI.get_current_path(self)
        if os.path.exists(file_path):
            version = user_info["version"]
            print(version)
            version_number = int(version.split("v")[1])
            version_number += 1
            str_version = str(version_number)
            new_version = f"{str_version.zfill(3)}" 
        return new_version
    
    def _import_yaml_template(self):
        """template.yml import 하는 메서드"""
        with open('/home/rapa/baked/toolkit/config/core/env/sy_template.yml') as f:
            yaml_data = yaml.load(f, Loader=yaml.FullLoader)
            yaml_path = yaml_data["paths"]
        return yaml_path
    
    def _check_validate(self, new_path):
        """저장할 파일 경로가 유효한지 확인하는 메서드 (폴더가 존재하지 않으면 생성해주기)"""
        file_path = "".join(new_path.split("/")[:-2])
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        
    def _cancel_and_close(self):
        self.close()
    
    ########################################shotgun part###############################################
    
    def _connect_sg(self):
        """샷그리드 연결시키는 메서드"""
        URL = "https://4thacademy.shotgrid.autodesk.com"
        SCRIPT_NAME = "pipeline key"
        API_KEY = "^axlq0daadimnwnatxrdoYfsm"
        sg = shotgun.Shotgun(URL,
                         SCRIPT_NAME,
                         API_KEY)
        return sg

    def _get_published_file_category(self):
        """published file type 콤보박스에 넣어주는 메서드"""
        sg = self._connect_sg()
        published_file_type = ['']
        published_file_type_sg = sg.find("PublishedFileType", [["sg_level", "is_not", None]], fields=["code"])
        for info in published_file_type_sg:
            published_file_type.append(info['code'])
        self.ui.comboBox_type.addItems(published_file_type)
        
    def _get_task_type(self):
        sg = self._connect_sg()
        asset_steps_list = ['-----------select------------']
        shot_steps_list = []
        asset_steps = sg.find("Step", [['entity_type', 'is', 'Asset']], fields=["description"])
        shot_steps = sg.find("Step", [['entity_type', 'is', 'Shot']], fields=["description"])

        for asset in asset_steps:
            asset_steps_list.append(f"[Asset]  {asset['description']}")
        for shot in shot_steps:
            shot_steps_list.append(f"[Shot]   {shot['description']}")
            
        self.ui.comboBox_task.addItems(asset_steps_list)
        self.ui.comboBox_task.addItems(shot_steps_list)
        return asset_steps_list, shot_steps_list

    def _show_link_entity(self):
        self.ui.comboBox_link.clear()
        task = self.ui.comboBox_task.currentText()[9:]
        sg = self._connect_sg()
        link_list = ['']
        step = sg.find("Step", [['description', 'is', task]], fields=["code"])[0]['code']
        link = sg.find("Task", [['step.Step.code', 'is', step], ['project.Project.name', 'is', 'baked']], fields=["entity"])
        for item in link:
            link_list.append(item['entity'].get('name'))
        if task == "":
            self.ui.comboBox_link.setCurrentIndex(0)
        self.ui.comboBox_link.addItems(link_list)

    ################### 펍할 데이터들 #######################
    def _connect_file_and_type(self):
        file = self.ui.currentItem.text(0) # 현재 클릭된 파일 이름
        file_type = self.publish_dict[file]['file type']
        self.ui.comboBox_type.setCurrentText(file_type)

    def _make_publish_info_dict(self, item, column):
        """"""
        file = item.text(column)
        if file == "Publish to Flow" or file == "Upload for review" or item.parent() == None:
            return
        if file not in self.publish_dict:
            self.publish_dict[file] = {'pub': "", 'review': "", 'file type': ""}
        try:
            if item.child(0).checkState(1) == Qt.Checked:
                self.publish_dict[file]['pub'] = 'pub'
            elif item.child(1).checkState(1) == Qt.Checked:
                self.publish_dict[file]['review'] = 'review'

            if self.publish_dict[file]['file type'] == "":
                self.ui.comboBox_type.setCurrentText("")
            else:
                self.ui.comboBox_type.setCurrentText(self.publish_dict[file]['file type'])
        except:
            pass

    def _check_pub_or_version(self):
        """모든 아이템 체크박스 선택되게/선택 안 되게 하는 메서드"""
        parent_count = self.tree.topLevelItemCount()
        for count_parent in range(parent_count): 
            child_count = self.tree.topLevelItem(count_parent).childCount() # object 개수
            for count in range(child_count):
                object = self.tree.topLevelItem(count_parent).child(count)
                child_ver = object.child(0)
                child_pub = object.child(1)
                object_text = object.text(0)
                if child_pub.checkState(1) == Qt.Checked:
                    self.publish_dict[object_text]['pub'] = 'pub'
                elif child_ver.checkState(1) == Qt.Checked:
                    self.publish_dict[object_text]['review'] = 'review'
    

    def _put_publish_type_info_dict(self):
        item = self.tree.currentItem()
        file = item.text(0)
        if file in ['Publish to Flow', 'Upload for review']:
            return
        if file not in self.publish_dict and file != "":
            self.publish_dict[file] = {'pub': "", 'review': "", 'file type': ""}
        self.publish_dict[file]['file type'] = self.ui.comboBox_type.currentText()
        if self.publish_dict[file]['file type'] != '':
            item.setText(1, "O")
            item.setForeground(1, QBrush(QColor("orange")))
    
    def _load_publish_summary(self):
        self.ui.textEdit.clear()
        self._check_pub_or_version()
        for file, value in self.publish_dict.items(): 
            if file == "":
                continue
            self.ui.textEdit.append(file) 
            if value['pub'] == "pub":
                self.ui.textEdit.append('- Publish to Flow')
                self.ui.textEdit.append('- Upload for review')
            elif value['review'] == "review":
                self.ui.textEdit.append('- Upload for review')
            self.ui.textEdit.append(f"- File type: {value['file type']}")
            self.ui.textEdit.append("")


    ##############################################PUBLISH#############################################33
    def _publish_file_data(self):
        # 1. 체크박스 체크 =>  publish (check 된 데이터만) :
        # 2. 샷그리드 업로드 : (published) mb,cache,nknc (versions)mov/jpg
             # => ui에 있는 정보 다 가져와서 딕셔너리에 넣어서 => 넣어주기
        # 3. save (이건 여기 적힌 모든 데이터를 다 pub으로 세이브)
            # publish 할때 cache, mb 한 묶음으로? 
            # camera 데이터는 따로 
        #3. 모델링에서 그룹이 여러개 선택되는 경우 ) 경고문 (하나만 선택하시오) 
        #4. 
        new_path = self._get_path_using_template()
        print (new_path)
        if self.tool == "maya":
            MayaAPI.save_file(self, new_path)
        else:
            NukeAPI.save_file(self, new_path)

    def _show_publish_summary(self):
        """textEdit에 퍼블리쉬할 데이터 입력하는 함수"""
        pass
        

    def _show_published_type(self):
        """해당 파일을 click 할때마다 type 설정할 수 있게 해주는"""

    def create_version(self):
        task = self.ui.comboBox_task.currentText()
        link = self.ui.comboBox_link.currentText()
        name = self._get_user_info['name']
        # description = self.file_pub_data[]
        version = self._get_user_info['version']
        project = self._get_user_info['project']
        #review_path = # mov 저장하고 나온 데이터로 
        # pub_path = # pub 저장하고 나온 데이터로 => 
        version_data = {'project': project,
                        'code': f"V{version}",     # 이름 (추후 입력되는 데이터를 받아오는걸로 수정가능)
                        'entity': link,
                        'sg_task': task,
                        'sg_status_list': 'wip', # 상태 (추후 수정가능)
                        'user': name,
                        'sg_upload_movie': "review_path",
                        'description': 'description',
                        'published_files' : pub_path}
        
        version = self.sg.create('Version', version_data)
        self.sg.upload_thumbnail("Version", version['id'], thumbnail_path)
        return version


# published file을 생성한다.
    def create_published_file(self, published_file_type):
        task = self.ui.comboBox_task.currentText()
        link = self.ui.comboBox_link.currentText()
        name = self._get_user_info['name']
        # description = self.file_pub_data[]
        version = self._get_user_info['version']
        project = self._get_user_info['project']
        # pub_path = # pub 저장하고 나온 데이터로
        published_file_data = {'project': self.project,
                               'code': "Name",   # 이름 (추후 입력되는 데이터를 받아오는걸로 수정가능)
                               'published_file_type': {'type': 'PublishedFileType', 'id': pub_types},
                               'sg_status_list': 'ip', # 상태 (추후 수정가능)
                               'description': description,
                               'entity': link,
                               'task': task,
                               'version': version,
                               'path': {'local_path': pub_path},
                               'created_by': name,
                               'published_file_type' : published_file_type}
        published_file = self.sg.create('PublishedFile', published_file_data)
        return published_file

    def _save_file_dev_version_up(self):
        new_path = self._get_path_using_template()

    def _save_file_pub(self):
         ### dev 에서 VER up 해주는거 & pub에서 Ver 그대로인거
         pass
    
if __name__ == "__main__":
    app = QApplication(sys.argv)        
    # app.exec() 
