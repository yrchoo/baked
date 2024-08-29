try:    
    from PySide6.QtWidgets import QApplication, QWidget, QButtonGroup
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import QFile, Qt
    from PySide6.QtGui import QBrush, QColor, QIcon
    from PySide6.QtGui import QPixmap, QTextCursor
    from PySide6.QtMultimedia import QMediaPlayer, QMediaContent
    from PySide6.QtMultimediaWidgets import QVideoWidget
    from shotgun_api3 import shotgun
    import department_publish 
    import work_in_maya
    from importlib import reload
    from capture_module import SubWindow_Open, MakeScreenCapture
    from work_in_maya import MayaAPI
    from work_in_nuke import NukeAPI
    import sys
    import os
    import yaml
    import glob
except:
    from PySide2.QtWidgets import QApplication, QWidget, QButtonGroup
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtCore import QFile, Qt
    from PySide2.QtGui import QBrush, QColor, QIcon
    from PySide2.QtGui import QPixmap, QTextCursor
    from shotgun_api3 import shotgun
    import department_publish 
    from importlib import reload
    from capture_module import SubWindow_Open, MakeScreenCapture
    from work_in_maya import MayaAPI
    from work_in_nuke import NukeAPI
    import work_in_maya
    import sys
    import os
    import yaml
    import glob

class Publisher(QWidget):
    def __init__(self):
        super().__init__()
        self._set_ui()
        self.initial_setting()
        self._get_task_type()
        self._set_event()

    def _set_event(self):
        """이벤트 발생 메서드"""

        self.ui.checkBox_check.clicked.connect(self._select_all_items)

        self.ui.pushButton_collapse.clicked.connect(self._collapse_tree)
        self.ui.pushButton_expand.clicked.connect(self._expand_tree)
        self.ui.pushButton_publish.clicked.connect(self._publish_file_data)
        self.ui.pushButton_cancel.clicked.connect(self._close_ui)
        self.ui.pushButton_load.clicked.connect(self._load_publish_summary)
        self.ui.pushButton_thumbnail.clicked.connect(self._make_thumbnail)

        self.ui.comboBox_task.currentIndexChanged.connect(self._show_link_entity)
        self.ui.comboBox_task.currentTextChanged.connect(self._connect_to_department)
        self.ui.comboBox_type.currentIndexChanged.connect(self._put_publish_type_info_dict)

        self.ui.treeWidget.itemChanged.connect(self._connect_check_state)
        self.ui.treeWidget.itemChanged.connect(self._check_pub_or_version)

        self.ui.treeWidget.itemClicked.connect(self._show_file_detail)
        self.ui.treeWidget.itemClicked.connect(self._connect_item_and_type)
        self.ui.treeWidget.itemClicked.connect(self._show_description)
        self.ui.plainTextEdit_description.textChanged.connect(self._write_description)

        self.button_group = QButtonGroup()
        button_list = [self.ui.radioButton_playblast, self.ui.radioButton_capture, self.ui.radioButton_render]
        for button in button_list:
            self.button_group.addButton(button)
        self.button_group.buttonClicked.connect(self._show_thumbnail)

    def _set_ui(self):
        """ui 셋업해주는 메서드"""
        ui_file_path = '/home/rapa/baked/toolkit/config/python/publisher_final.ui' 
        ui_file = QFile(ui_file_path)

        loader = QUiLoader()
        self.ui = loader.load(ui_file, self)  
        ui_file.close()

    def initial_setting(self):
        """초기 ui 세팅하는 메서드"""

        self.tree = self.ui.treeWidget
        self.tool = "maya" #### 일단 보류

        reload(department_publish)
        reload(work_in_maya)
        self.publish_dict = department_publish.DepartmentTree(self.tree, 'maya').put_data_in_tree()
        print("*****", self.publish_dict, '*****')

        self.show()
        self._get_published_file_category()
        self.ui.checkBox_check.setChecked(True)
        self.ui.pushButton_load.setIcon(QIcon(f"/home/rapa/baked/toolkit/config/python/icons/reload.png"))

    def _show_file_detail(self, item, _):
        """ 선택한 treewidget 아이템 정보 크게 보여주는 메서드 """
        text = item.text(0)

        if text in ["Publish to Flow", "Upload for review"]:
            text = self.tree.currentItem().parent().text(0)
        self.ui.label_name.setText(text)
        self.ui.label_info.setText(f"file")
        self.ui.label_name.setAlignment(Qt.AlignLeft)
        self.ui.label_info.setAlignment(Qt.AlignLeft)

        # 선택되는 파일에 따라 이미지 변경해주기
        # label_image = self.ui.label
        # data_type = 'grp'
        # pixmap = QPixmap(f"/home/rapa/baked/toolkit/config/python/{data_type}.png") 
        # scaled_pixmap = pixmap.scaled(50, 50) 
        # icon = self.publish_dict[text]['ext']
        # icon = 'mb'
        # self.ui.label_image.setIcon(QIcon(f"/home/rapa/baked/toolkit/config/python/icons/{icon}.png"))
    
    def _select_all_items(self):
        """ 모든 아이템 체크박스 선택되게/선택 안 되게 하는 메서드 """
        parent_count = self.tree.topLevelItemCount()
        for count_parent in range(parent_count): 
            child_count = self.tree.topLevelItem(count_parent).childCount()
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
        """ publish 체크랑 review 체크 연동시키기 """
        pass
        # if item.text(0) == "Upload for review":
        #     return
        # if item.checkState(column) == Qt.Checked:
        #     parent = item.parent()
        #     parent.child(1).setCheckState(1, Qt.Checked)

    ########################## 저장하고 버전 관리 #############################

    def _get_path_using_template(self, work, ext=""):
        """ yaml 템플릿을 이용해서 저장할 경로, 파일 이름 만드는 메서드 """

        yaml_path = self._import_yaml_template()
        file_info_dict = self._get_user_info()
        tool = file_info_dict["tool"]
        level = file_info_dict["seq/asset"]
        current = f"{tool}_{level}_{work}"
        if ext: 
            current += f"_{ext}"
        print (f"146_get_path_using_template : {current}")
        
        new_path = ""
        if current in yaml_path:
            root_path = yaml_path[f"{level}_root"]
            new_path = yaml_path[current]["definition"].replace(f"@{level}_root", root_path)
            new_path = new_path.format(**file_info_dict)
            print (f"163_get_path_using_template:  {new_path}")
            self._check_validate(new_path)
        return new_path

    def _get_user_info(self):
        """ 유저에 대한 정보 가저오는 메서드 """ # 임시 설정 
        """ 유저 커스텀 버튼 있으면 좋을듯 """

        self.user_file_info = {
                    "name":"Seoyeon Yoon",
                    "project":"baked",
                    "seq/asset":"asset",
                    "shot": "",
                    "asset_type": "Character",
                    "asset":"Apple",
                    "task":"MOD",
                    "dev/pub":"dev",
                    "tool":"maya",
                    "version":"001",
                    "filename":"desk_MOD_v001",
                    "maya_extension":"mb"}
        return self.user_file_info
    
    def _connect_to_department(self, task):
        print(task)
        self.department = task[9:]
        self.department = "MOD"
        self.dep_class = getattr(department_publish, self.department)(self.tree,'maya')

    def _make_version_up(self):
        """버전 업해주는 메서드"""
        user_info = self._get_user_info()
        file_path = self._get_path_using_template('dev')
        if os.path.exists(file_path):
            version = user_info["version"]
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
        file_path = "/".join(new_path.split("/")[:-1])
        print (f"206/_check_validate : {file_path}")
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        return file_path
        
    def _close_ui(self):
        """UI창 끄는 메서드"""
        self.close()

    def _expand_tree(self):
        """트리 위젯을 여는 메서드"""
        self.tree.expandAll()
        
    def _collapse_tree(self):
        """트리 위젯을 닫는 메서드"""
        self.tree.collapseAll()

    def _connect_item_and_type(self, item, _):
        """Treewidget item누를 때마다 콤보박스에 내가 선택한 타입 뜨게 하기"""
        file = item.text(0)
        print (f"--- {file}")
        if file in ['Publish to Flow', 'Upload for review']:
            self.ui.comboBox_type.setCurrentText("")
            return
        if not self.publish_dict[file]['file type']:
            self.ui.comboBox_type.setCurrentText('')
        self.ui.comboBox_type.setCurrentText(self.publish_dict[file]['file type'])
        
    def _show_description(self, item, _):
        """treewidget 각 아이템별로 저장된 description 보여주는 메서드"""
        file = item.text(0)
        if file in ["Upload for review", "Publish to Flow"]:
            item = item.parent()
            file = item.text(0)
        self.ui.plainTextEdit_description.setPlainText(self.publish_dict[file].get('description', "")) # 현재 파일의 description
        
    def _write_description(self):
        """수정된 description 딕셔너리에 저장하는 메서드"""
        item = self.tree.currentItem()
        file = item.text(0)
        print (file)
        if file in ["Upload for review", "Publish to Flow"]:
            item = self.tree.currentItem().parent()
            file = item.text(0)
        if self.ui.plainTextEdit_description.toPlainText():
            self.publish_dict[file]['description'] = self.ui.plainTextEdit_description.toPlainText()
        
    ################################### get shotgrid data ##########################################
    
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
        self.file_type_ext = {}
        published_file_type_sg = sg.find("PublishedFileType", [["sg_level", "is_not", None]], fields=["code", "sg_ext"])
        for info in published_file_type_sg:
            published_file_type.append(info['code'])
            self.file_type_ext[info['code']] = info['sg_ext']
        self.ui.comboBox_type.addItems(published_file_type)
        
    def _get_task_type(self):
        """shotgrid에서 task 종류 가져오는 메서드"""
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
        """shotgrid 에서 task 와 링크된 entity 가져오는 메서드"""
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

    def _check_pub_or_version(self, item, _):
        """treewidget 아이템별로 publish/review 구분하는 메서드"""
        if item.text(1): 
            return 

        key = item.parent().text(0)
        val = item.checkState(1)
        value = self._is_checked(item) # checkState는 True/False 로 찍히지 않는다..
            
        if "Publish to Flow" in item.text(0):
            print ('flow누름')
            print (f"key:{key}, val:{val}")
            option = "pub"
            parent_item = item.parent()
            child = parent_item.child(1)
            if value == False:
                item.setForeground(0, QBrush(QColor("gray")))
                child.setForeground(0, QBrush(QColor("gray")))
            else:
                item.setForeground(0, QBrush(QColor("white")))
                if not item.parent().parent():
                    child.setForeground(0, QBrush(QColor("gray")))
                else:
                    child.setForeground(0, QBrush(QColor("white")))
                    # child.setCheckState(1, val)
        elif "Upload for review" in item.text(0):
            print("review 누름")
            option = "rev"
            parent_item = item.parent()
            child = parent_item.child(0)
            if value == True:
                item.setForeground(0, QBrush(QColor("white")))
                child.setForeground(0, QBrush(QColor("gray")))
            else:
                item.setForeground(0, QBrush(QColor("gray")))
                child.setForeground(0, QBrush(QColor("gray")))

        self.publish_dict[key][option] = value

    def _is_checked(self, item):
        """checkbox checked 일때 True 리턴하는 메서드"""
        if item.checkState(1) == Qt.Checked:
            return True
        else:
            return False
    
    def _put_publish_type_info_dict(self, index):
        """treewidget 아이템 별로 published type 기록하는 메서드"""
        item = self.tree.currentItem()
        file = item.text(0)
        if file in ['Publish to Flow', 'Upload for review'] or index == 0:
            return
        self.publish_dict[file]['file type'] = self.ui.comboBox_type.currentText()
        item.setText(1, "O")
        item.setForeground(1, QBrush(QColor("light pink")))
    
    def _load_publish_summary(self):
        """퍼블리쉬할 데이터 보여주는 메서드"""
        self.ui.textEdit.clear()
        for file, value in self.publish_dict.items(): 
            if file == "":
                continue
            if value['pub'] == False and value['rev'] == False:
                continue
            self.ui.textEdit.append(f'<b>{file}</b>') 
            if value['pub'] == True and value['rev'] == True:
                self.ui.textEdit.append('- Publish to Flow')
                self.ui.textEdit.append('- Upload for review')
            elif value['pub'] == False and value['rev'] == True:
                self.ui.textEdit.append('- Upload for review')
            self.ui.textEdit.append(f"- File type: {value['file type']}")
            self.ui.textEdit.append(f"- Description: {value['description']}")
            self.ui.textEdit.append("")
        self.ui.textEdit.moveCursor(QTextCursor.Start)
        print ("------------", self.publish_dict, '------------')

    ############################# Flow: publish/versions에 올리기 ########################################

    def _make_root_path(self):
        """maya까지 root path 가져오기"""
        return self._get_path_using_template('root')
    
    def _show_thumbnail(self, button):
        """썸네일 보여주는 메서드"""
        image_path = ""
        if button.text() == "PlayBlast":
            ext = self.dep_class.set_playblast_ext()
            image_path = self._get_path_using_template("playblast", ext)
        elif button.text() == "Capture":
            ext = self.dep_class.set_capture_ext()
            image_path = self._get_path_using_template("capture", ext)
        elif button.text() == "Render":
            ext = self.dep_class.set_render_ext()
            image_path = self._get_path_using_template("render", ext) # 부서별로 펍할 external 입력받기

        path = self._check_validate(image_path)    
        files = glob.glob(f"{path}/*")

        if not files:
            self.ui.label_thumbnail.setText("No Thumbnail Found")
            self.ui.label_thumbnail.setAlignment(Qt.AlignCenter)
            return
        recent_image_file = max(files, key=os.path.getmtime)
        pixmap = QPixmap(recent_image_file) 
        scaled_pixmap = pixmap.scaled(288, 162) 
        self.ui.label_thumbnail.setPixmap(scaled_pixmap) # 가장 최근 사진으로 뽑기

    def _make_thumbnail(self): 
        """썸네일 만들어주는 메서드"""
        # Lighting, Comp 팀은 지원해주지 않기
        # 만약 존재하면 그거 보여주도록

        if self.ui.radioButton_playblast.isChecked():
            ext = self.dep_class.set_playblast_ext()
            image_path = self._get_path_using_template("playblast", ext)
            self._check_validate(image_path)
            MayaAPI.make_playblast(self, image_path, ext)
            self._show_thumbnail(self.ui.radioButton_playblast)

        elif self.ui.radioButton_capture.isChecked():
            ext = self.dep_class.set_capture_ext()
            image_path = self._get_path_using_template("capture", ext)
            self._check_validate(image_path)
            MakeScreenCapture(QWidget) ########### 클래스 보내는 방법 헷갈려
            self._show_thumbnail(self.ui.radioButton_capture)

        elif self.ui.radioButton_render.isChecked():
            ext = self.dep_class.set_render_ext()
            image_path = self._get_path_using_template("render", ext)
            self._check_validate(image_path)  
            self._show_thumbnail(self.ui.radioButon_render)
    
    ######################### PUBLISH 버튼 누르면 발생하는 이벤트 ############################

    def _publish_file_data(self):
        """publish 눌렀을 때 발생하는 이벤트"""
        if not self._save_file_pub:
            return
        preview_path = self._apply_ffmpeg()
        self.publish_dict['preview'] = {'path' : preview_path}
        self._save_file_dev_version_up()
        self._create_published_file()
        self._create_version()
    
    def _save_file_pub(self):
        """ (1) pub 파일에 저장하는 메서드 (scene파일, cache만) (version 작업 파일 그대로) """
        """ 펍할때는 무조건 scene파일 올리는거니까 scene파일 선택되어있지 않으면 versions로만 올린다는 이야기 """
        """ 펍한다고 하면 펍한다고 체크한 데이터들로만 진행 """
        scene_file = self.publish_dict.keys()[0]
        if not self.publish_dict[scene_file]['pub'] or self._get_path_for_selected_files():
            return False
        for file in self.publish_dict: 
            if not file['pub']:
                continue
            ext = self.publish_dict['ext']
            self._get_path_using_template('pub', ext)
        self.dep_class.save_data(self.publish_dict)
        return True
    
    def _get_path_for_selected_files(self):
        """선택된 파일 타입에 따라 경로 만들어서 딕셔너리에 넣어주기 """
        for file in self.publish_dict:
            if not file['pub']:
                continue
            if not self.publish_dict[file]['file type'] : ### check empty data
                self.label_info.setText(f"Please select file type")
                return False
            self.publish_dict[file]['ext'] = self.file_type_ext[file['file type']]
            path = self._get_path_using_template("capture", file['ext'])
            self.publish_dict[file]['path'] = path
        return True
            

    def _save_file_dev_version_up(self):
        """ (2) dev 파일에 저장하는 메서드 (dev 폴더에 저장할) """
        """ dev에는 scene파일만 cache들은 저장 안됨 + 썸네일 저장"""
        self._make_version_up() # scene 파일
        new_path = self._get_path_using_template('dev')

    def _apply_ffmpeg(self):
        """ (3) ffmpeg 만드는 메서드"""
        """ 예린님 코드로 연결시키기"""
        image_path = self._get_path_using_template("ffmpeg")
        MayaAPI.ffmpeg
        return image_path
    
    ############### 샷그리드에 파일 올리는 메서드들은 따로 파일 만들예정 ###############

    def _create_published_file(self):
        """ (4) 샷그리드 published_file 에 pub 파일들 올리는 메서드 """
        print (f"PUBLISHED /// {self.publish_dict}")
        task = self.ui.comboBox_task.currentText()
        link = self.ui.comboBox_link.currentText()
        name = self._get_user_info['name']
        version = self._get_user_info['version']
        project = self._get_user_info['project']
        description = self.file_pub_data['description']
        published_file_type = self.publish_dict['file type']
        # pub_path = # pub 저장하고 나온 데이터로
        published_file_data = {'project': project,
                               'code': "파일 이름",   # 이름 (추후 입력되는 데이터를 받아오는걸로 수정가능)
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

    def _create_version(self):
        """ (5) 샷그리드 versions에 오리는 메서드 """
        print (f"REVIEW     /// {self.publish_dict}")
        task = self.ui.comboBox_task.currentText()
        link = self.ui.comboBox_link.currentText()
        name = self._get_user_info['name']
        description = self.publish_dict['description']
        version = self._get_user_info['version']
        project = self._get_user_info['project']
        # review_path = mov 저장하고 나온 경로 
        # pub_path = pub 저장하고 나온 경로
        # thumbnail_path = 썸네일 만들고 나온 경로
        version_data = {'preview': "썸네일",
                        'project': project,
                        'code': f"v{version}",     # 이름 (추후 입력되는 데이터를 받아오는걸로 수정가능)
                        'entity': link,
                        'sg_task': task,
                        'sg_status_list': 'wip', # 상태 (추후 수정가능)
                        'user': name,
                        'sg_upload_movie': "review_path",
                        'published_files': "pub된 경우",
                        'description': description,
                        'published_files' : pub_path}
        
        version = self.sg.create('Version', version_data)
        self.sg.upload_thumbnail("Version", version['id'], thumbnail_path)
        return version
    
if __name__ == "__main__":
    app = QApplication(sys.argv) 
