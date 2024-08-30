try:    
    from PySide6.QtWidgets import QApplication, QWidget, QButtonGroup
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import QFile, Qt
    from PySide6.QtGui import QBrush, QColor, QIcon
    from PySide6.QtGui import QPixmap, QTextCursor
    from PySide6.QtMultimedia import QMediaPlayer, QMediaContent
    from PySide6.QtMultimediaWidgets import QVideoWidget
except:
    from PySide2.QtWidgets import QApplication, QWidget, QButtonGroup
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtCore import QFile, Qt
    from PySide2.QtGui import QBrush, QColor, QIcon
    from PySide2.QtGui import QPixmap, QTextCursor

from shotgun_api3 import shotgun
import department_publish 
import shotgrid.fetch_shotgrid_data
from importlib import reload
from capture_module import SubWindow_Open, MakeScreenCapture
from work_in_maya import MayaAPI
from work_in_nuke import NukeAPI
import work_in_maya
import sys
import os
import yaml
import glob
import re
reload(department_publish)
reload(work_in_maya)
reload(shotgrid.fetch_shotgrid_data)


from shotgrid.fetch_shotgrid_data import ShotGridDataFetcher
class Publisher(QWidget):
    def __init__(self, sg : ShotGridDataFetcher, tool :str = None):

        super().__init__()
        self._set_initial_val(sg, tool)
        self._set_ui()
        self._initial_ui_setting()
        self._get_task_type()
        self._show_link_entity()
        self._task_setting()
        self._link_setting()
        self._connect_department()
        self._set_event()

    def _set_initial_val(self, sg, tool):
        self.sg : ShotGridDataFetcher = sg # login 시에 지정된 userdata를 가지고 Shotgrid에서 정보를 가져오는 Shotgrid_Data() 클래스
        self.tool = tool

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
        self.ui.comboBox_task.currentTextChanged.connect(self._connect_department)
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

    def _link_setting(self):
        if self.user_data['task'].lower() in self.asset_steps_dict:
            self.ui.comboBox_link.setCurrentText(self.user_data['asset'])
        else:
            self.ui.comboBox_link.setCurrentText(self.user_data['shot'])

    def _set_ui(self):
        """ui 셋업해주는 메서드"""

        ui_file_path = '/home/rapa/baked/toolkit/config/python/publisher_final.ui' 
        ui_file = QFile(ui_file_path)

        loader = QUiLoader()
        self.ui = loader.load(ui_file, self)  
        ui_file.close()

    def _initial_ui_setting(self):
        """초기 ui 세팅하는 메서드"""

        self.tree = self.ui.treeWidget
        self.publish_dict = department_publish.DepartmentWork(self.tree, 'maya').put_data_in_tree()

        self.show()
        self._get_published_file_category()
        self.ui.checkBox_check.setChecked(True)
        self.ui.pushButton_load.setIcon(QIcon(f"/home/rapa/baked/toolkit/config/python/icons/reload.png"))

        user_data = self.sg.user_info
        self.user_data = self._get_user_info(user_data) ## 현재 유저 정보, 작업 파일 딕셔너리로 저장

        if self.user_data['shot'] != "":
            self.ui.comboBox_link.setCurrentText(self.user_data['shot'])
        else:
            self.ui.comboBox_link.setCurrentText(self.user_data['asset'])

    def _show_file_detail(self, item, _):
        """ 선택한 treewidget 아이템 정보 크게 보여주는 메서드 """

        text = item.text(0)
        if text in ["Publish to Flow", "Upload for review"]:
            text = item.parent().text(0)
            item = item.parent()
        if not item.parent():
            pixmap = QPixmap("/home/rapa/baked/toolkit/config/python/icons/scene.png")         
        else:
            pixmap = QPixmap("/home/rapa/baked/toolkit/config/python/icons/object.png") 
        scaled_pixmap = pixmap.scaled(30, 30) 
        self.ui.label.setPixmap(scaled_pixmap)
        self.ui.label_name.setText(text)

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
        try:
            if item.text(0) == "Upload for review" or not item.parent().parent():
                return
            elif item.checkState(column) == Qt.Checked:
                parent = item.parent()
                parent.child(1).setCheckState(1, Qt.Checked)
        except:
            pass
    ########################## 저장하고 버전 관리 #############################

    def _get_path_using_template(self, work, ext=""):
        """ yaml 템플릿을 이용해서 저장할 경로, 파일 이름 만드는 메서드 """

        yaml_path, _ = self._import_yaml_template()
        file_info_dict = self.user_data
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

    def _get_user_info(self, user_data):
        """ 유저에 대한 정보 가저오는 메서드 """ # 임시 설정 
        """ 유저 커스텀 버튼 있으면 좋을듯 """
        
        if self.tool == 'maya':
            _, yaml_key = self._import_yaml_template()
            user_data['maya_extension'] = yaml_key['maya_extension']['default']
            
        user_data['tool'] = self.tool
        current_file_name = department_publish.DepartmentWork(self.tree, self.tool).get_current_file_name()
        version = self._get_version_from_current_file(current_file_name)
        user_data['version'] = version
        if user_data["asset"]:
            user_data["seq/asset"] = "asset"
        else:
            user_data["seq/asset"] = "sequence"
            
        return user_data
    
    def _get_version_from_current_file(self, file):
        """ 현재 작업하는 파일 버전 가져오는 메서드 """

        p = re.compile("[v]\d{3}")      
        p_version = p.search(file)  
        if p_version:
            version = p_version.group()[1:]
            return version   
    
    def _connect_department(self):
        """나중에는 ui에서 가져오는 거롤"""
        reversed_task_dict = dict(map(reversed, self.task_dict.items()))
        task = self.ui.comboBox_task.currentText()
        self.department = reversed_task_dict[task].upper()
        self.dep_class = getattr(department_publish, self.department)(self.tree,'maya')
    
    def _import_yaml_template(self):
        """template.yml import 하는 메서드"""
        with open('/home/rapa/baked/toolkit/config/core/env/sy_template.yml') as f:
            yaml_data = yaml.load(f, Loader=yaml.FullLoader)
            yaml_path = yaml_data["paths"]
            yaml_key = yaml_data["keys"]
        return yaml_path, yaml_key
    
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
        try:
            file = item.text(0)
        except:
            return # disabled 된 경우
        if file in ["Upload for review", "Publish to Flow"]:
            item = self.tree.currentItem().parent()
            file = item.text(0)
        if self.ui.plainTextEdit_description.toPlainText():
            self.publish_dict[file]['description'] = self.ui.plainTextEdit_description.toPlainText()
        
    ################################### get shotgrid data ##########################################

    def _get_published_file_category(self):
        """published file type 콤보박스에 넣어주는 메서드"""
        published_file_type = ['']
        self.file_type_ext = {}
        published_file_type_sg = self.sg.sg.find("PublishedFileType", [["sg_level", "is_not", None]], fields=["code", "sg_ext"])
        for info in published_file_type_sg:
            published_file_type.append(info['code'])
            self.file_type_ext[info['code']] = info['sg_ext']
        self.ui.comboBox_type.addItems(published_file_type)
        
    def _get_task_type(self):
        """shotgrid에서 task 종류 가져오는 메서드"""
        asset_steps_list = []
        shot_steps_list = []
        self.asset_steps_dict = {}
        self.shot_steps_dict = {}
        asset_steps = self.sg.sg.find("Step", [['entity_type', 'is', 'Asset']], fields=["description", "code"])
        shot_steps = self.sg.sg.find("Step", [['entity_type', 'is', 'Shot']], fields=["description", "code"])
        for asset in asset_steps:
            self.asset_steps_dict[asset['code']] = f"[Asset]  {asset['description']}"
            asset_steps_list.append(f"[Asset]  {asset['description']}")

        for shot in shot_steps:
            self.shot_steps_dict[shot['code']] = f"[Shot]   {shot['description']}"
            shot_steps_list.append(f"[Shot]   {shot['description']}")

        self.ui.comboBox_task.addItems(asset_steps_list)
        self.ui.comboBox_task.addItems(shot_steps_list)
        
        self.task_dict = {} # mod:[Asset]  Modeling
        self.task_dict.update(self.asset_steps_dict)
        self.task_dict.update(self.shot_steps_dict)

    def _show_link_entity(self):
        """shotgrid 에서 task 와 링크된 entity 가져오는 메서드"""

        self.ui.comboBox_link.clear()
        task = self.ui.comboBox_task.currentText()[9:]
        link_list = []
        step = self.sg.sg.find("Step", [['description', 'is', task]], fields=["code"])[0]['code']
        link = self.sg.sg.find("Task", [['step.Step.code', 'is', step], ['project.Project.name', 'is', 'baked']], fields=["entity"])
        for item in link:
            link_list.append(item['entity'].get('name'))
        self.ui.comboBox_link.addItems(link_list)

        # task = self.ui.comboBox_task.currentText()
        # reversed_task_dict = dict(map(reversed, self.task_dict.items()))
        # if reversed_task_dict[task] == self.user_data["task"].lower():
        #     return

        

    def _check_pub_or_version(self, item, column):
        """treewidget 아이템별로 publish/review 구분하는 메서드"""
        if item.text(1) or column == 0: 
            return 

        key = item.parent().text(0)
        val = item.checkState(1)
        value = self._is_checked(item) # checkState는 True/False 로 찍히지 않는다..    

        if "Publish to Flow" in item.text(0):
            option = "pub"
            parent_item = item.parent()
            child = parent_item.child(1)
            if not item.parent().parent():
                self.publish_dict[key][option] = value
            else:
                child.setCheckState(1, val)
        elif "Upload for review" in item.text(0):
            option = "rev"
            parent_item = item.parent()
            child = parent_item.child(0)
            if not value: 
                child.setCheckState(1, val)

        self.publish_dict[key][option] = value
        self._connect_check_color(item, child)
    
    def _is_checked(self, item):
        """ checkbox checked 일때 True 리턴하는 메서드 """
        if item.checkState(1) == Qt.Checked:
            return True
        else:
            return False
        
    def _connect_check_color(self, item1, item2):
        """ 체크박스 유무에 따라 색깔 변경해주는 메서드 """
        if item1.checkState(1) == Qt.Checked:
            item1.setForeground(0, QBrush(QColor("white")))
        else:
            item1.setForeground(0, QBrush(QColor("gray")))
        if item2.checkState(1) == Qt.Checked:
            item2.setForeground(0, QBrush(QColor("white")))
        else:
            item2.setForeground(0, QBrush(QColor("gray")))
    
    def _put_publish_type_info_dict(self, index):
        """ treewidget 아이템 별로 published type 기록하는 메서드 """
        item = self.tree.currentItem()
        file = item.text(0)
        if file in ['Publish to Flow', 'Upload for review'] or index == 0:
            return
        self.publish_dict[file]['file type'] = self.ui.comboBox_type.currentText()
        item.setText(1, "O")
        item.setForeground(1, QBrush(QColor("light pink")))
    
    def _load_publish_summary(self):
        """ 퍼블리쉬할 데이터 보여주는 메서드 """

        self.ui.textEdit.clear()
        for file, value in self.publish_dict.items(): 
            if value['pub'] == False and value['rev'] == False:
                continue

            self.ui.textEdit.append(f'<b>{file}</b>') 
            if value['pub'] == True and value['rev'] == True:
                self.ui.textEdit.append('- Publish to Flow')
                self.ui.textEdit.append('- Upload for review')
            elif value['pub'] == False and value['rev'] == True:
                self.ui.textEdit.append('- Upload for review')
            elif value['pub'] == True and value['rev'] == False:
                self.ui.textEdit.append('- Publish to Flow')
            self.ui.textEdit.append(f"- File type: {value['file type']}")
            self.ui.textEdit.append(f"- Description: {value['description']}")
            self.ui.textEdit.append("")

        self.ui.textEdit.moveCursor(QTextCursor.Start)
        print ("------------", self.publish_dict, '------------')

    ############################# Flow: publish/versions에 올리기 ########################################
    
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

        start_frame, last_frame = self._get_frame_number(files) # 프레임 넘버, 경로 정보 저장하기
        self.preview_info = {'input path' : image_path, 
                             'start frame' : int(start_frame),
                             'last frame' : int(last_frame)}
        print (f"420:: self.preview_info {self.preview_info}")

    def _get_frame_number(self, files):
        """ 플레이블라스트, 렌더, 캡처를 통해 받은 파일 경로로 프레임 넘버 가져오기 """
        
        if len(files) == 1:
            return 1, None
        
        files = sorted(files)
        start_image = files[0]
        last_image = files[-1]
        p = re.compile("[.]\d{4}[.]")      
        p_start = p.search(start_image)  
        p_last = p.search(last_image)

        if p_start and p_last:
            start_frame = p_start.group()[1:5]
            last_frame = p_last.group()[1:5]        
        return start_frame, last_frame
        
    def _make_thumbnail(self): 
        """ 썸네일 새로 만들어주는 메서드 """
        # Lighting, Comp 팀은 지원해주지 않기

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

    def _publish_file_data(self): ##########MAIN############
        """publish 눌렀을 때 발생하는 이벤트"""
        if self._save_file_pub() == False :
            return
        
        input_path = self.preview_info['input path']
        self._apply_ffmpeg(input_path, self.user_data['project'])
        version = self._create_version_data()
        self._create_published_file(version)
        self._save_file_dev_version_up()
    
    def _save_file_pub(self):
        """ (1) pub 파일에 저장하는 메서드 (scene파일, cache만) (version 작업 파일 그대로) """
        """ 펍할때는 무조건 scene파일 올리는거니까 scene파일 선택되어있지 않으면 versions로만 올린다는 이야기 """
        """ 펍한다고 하면 펍한다고 체크한 데이터들로만 진행 """

        print ("----------", list(self.publish_dict.keys()))
        scene_file = list(self.publish_dict.keys())[0]
        print (f"--------451 scene_file {scene_file}---------")
        if not self.publish_dict[scene_file]['pub'] or not self._get_path_for_selected_files():
            return False
        print('-------------------------------------------')
        for file in self.publish_dict: 
            if not self.publish_dict[file]['pub']:
                continue
            try:
                ext = self.publish_dict['ext']
            except:
                ext = ''
            self._get_path_using_template('pub', ext)

        self.dep_class.save_data(self.publish_dict)
        print (f"476: save_file_pub: {self.publish_dict}")
        return True
    
    def _get_path_for_selected_files(self):
        """ 선택된 파일 타입에 따라 경로 만들어서 딕셔너리에 넣어주기 """
        for file in self.publish_dict:
            if not self.publish_dict[file]['pub']:
                continue
            if not self.publish_dict[file]['file type'] : ### check empty data
                self.label_info_2.setText(f"Please select file type")
                return False
            self.publish_dict[file]['ext'] = self.file_type_ext[self.publish_dict[file]['file type']]
            self.user_data['group'] = file
            path = self._get_path_using_template("pub", self.publish_dict[file]['ext'])
            self.publish_dict[file]['path'] = path
            print ("..........", file, ".........")
        print (f"480_________{self.publish_dict}")
        return True

    def _apply_ffmpeg(self, input_path, project_name):
        """ (3) ffmpeg 만드는 메서드"""
        """ 예린님 코드로 연결시키기"""
        output_path = self._get_path_using_template("ffmpeg")
        start_frame = self.preview_info['start frame']
        last_frame = self.preview_info['last frame']
        MayaAPI.make_ffmpeg(self, start_frame, last_frame, input_path, output_path, project_name)
        self.preview_info['output_path'] = output_path

    def _save_file_dev_version_up(self):
        """ (2) dev 파일에 저장하는 메서드 (dev 폴더에 저장할) """
        """ dev에는 scene파일만 cache들은 저장 안됨 + 썸네일 저장 """
        self.user_data['version'] = self._make_version_up() # scene 파일
        new_path = self._get_path_using_template('dev')
        department_publish.DepartmentWork(self.tree, self.tool).save_scene_file(new_path)
    
    def _make_version_up(self):
        """버전 업해주는 메서드"""
        user_info = self.user_data
        file_path = self._get_path_using_template('dev')
        if os.path.exists(file_path):
            version = int(user_info["version"])
            version += 1
            str_version = str(version)
            new_version = f"{str_version.zfill(3)}" 
        return new_version
    
    ############### 샷그리드에 파일 올리는 메서드들은 따로 파일 만들예정 ###############

    def _separate_pub_review(self):
        """pub된 데이터들은 다 versions에 올라가도록"""
        """versions에 올리는 데이터들은 published files 라는 링크는 없음"""
        """'pub':True, 'rev':False, 'description':'', 'file type':'', 'ext': '', 'path':''}}"""

        published_file_dict = {}
        review_file_dict = {}
        for file, info in self.publish_dict.items():
            if self.publish_dict[file]['pub']:
                published_file_dict[file] = info
            else:
                review_file_dict[file] = info
        
        return published_file_dict, review_file_dict
    
    def _create_version_data(self):
        """ (5) 샷그리드 versions에 오리는 메서드 """
        print (f"REVIEW     /// {self.publish_dict}")
        published_file_dict, review_file_dict = self._separate_pub_review()

        # version
        version = self.user_data['version']
        version = f'v{version}'
        # task
        reversed_task_dict = dict(map(reversed, self.task_dict.items()))
        task = self.ui.comboBox_task.currentText()
        task = reversed_task_dict[task]
        # description for review
        description = self.ui.plainTextEdit_description_review.toPlainText()   
        # preview path
        preview_path = self.preview_info['output_path']
        # link
        asset = ""
        shot = ""
        if "Asset" in self.ui.comboBox_task.currentText():
            asset = self.ui.comboBox_link.currentText()
            shot = None
        else:
            shot = self.ui.comboBox_link.currentText()
            asset = None
        
        version = self.sg.create_new_version_entity(version, task, description, preview_path, shot, asset)
        return version

    def _create_published_file(self, version):
        """ (4) 샷그리드 published_file 에 pub 파일들 올리는 메서드 """
        print (f"PUBLISHED /// {self.publish_dict}")
        published_file_dict, _ = self._separate_pub_review()
        if not published_file_dict:
            return

        # preview path : Lighting 팀은 Pre-Comp 가 끝난 후에 썸네일을 업로드함
        if 'Lighting' in self.ui.comboBox_task.currentText():
            preview_path = None 
        else:
            preview_path = self.preview_info['output_path']

        for detail in published_file_dict.values():
            file_path = detail['path']
            description = description['description']
            published_file_type = detail['file type']
            self.sg.create_new_publish_entity(version, file_path, description, preview_path, published_file_type)

    def _task_setting(self):
        if self.user_data['task'].lower() in self.asset_steps_dict:
            self.ui.comboBox_task.setCurrentText(self.asset_steps_dict[self.user_data['task'].lower()])
        else:
            self.ui.comboBox_task.setCurrentText(self.shot_steps_dict[self.user_data['task'].lower()])


if __name__ == "__main__":
    app = QApplication(sys.argv) 
