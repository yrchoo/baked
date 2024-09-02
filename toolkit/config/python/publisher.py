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
from department_publish import DepartmentWork, MOD, RIG
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
import subprocess
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

        self.ui.pushButton_collapse.clicked.connect(self._collapse_tree)
        self.ui.pushButton_expand.clicked.connect(self._expand_tree)
        self.ui.pushButton_publish.clicked.connect(self._publish_file_data)
        self.ui.pushButton_cancel.clicked.connect(self._close_ui)
        self.ui.pushButton_load.clicked.connect(self._load_publish_summary)
        self.ui.pushButton_thumbnail.clicked.connect(self._make_thumbnail)

        self.ui.comboBox_task.currentIndexChanged.connect(self._show_link_entity)
        self.ui.comboBox_task.currentTextChanged.connect(self._connect_department)
        self.ui.comboBox_type.currentIndexChanged.connect(self._put_publish_type_info_dict)

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
        ui_file_path = '/home/rapa/baked/toolkit/config/python/publisher_final.ui' 
        ui_file = QFile(ui_file_path)
        loader = QUiLoader()
        self.ui = loader.load(ui_file, self)  
        ui_file.close()

    def _initial_ui_setting(self):
        """
        초기 ui 세팅하는 메서드
        """
        self.tree = self.ui.treeWidget
        self.work = DepartmentWork(self.tree, self.tool)
        self.publish_dict = self.work.put_data_in_tree()
        self.show()

        self.ui.pushButton_load.setIcon(QIcon(f"/home/rapa/baked/toolkit/config/python/icons/reload.png"))
        self.user_data = self._get_user_info(self.sg.user_info) # 현재 유저 정보, 작업 파일 딕셔너리로 저장

    def _get_user_info(self, user_data):
        """ 유저에 대한 정보 가저오는 메서드 """ # 임시 설정 
        """ 유저 커스텀 버튼 있으면 좋을듯 """
        
        if self.tool == 'maya':
            _, yaml_key = self._import_yaml_template()
            user_data['maya_extension'] = yaml_key['maya_extension']['default']

        user_data['tool'] = self.tool
        current_file_name = self.work.get_current_file_name()
        version = self._get_version_from_current_file(current_file_name)
        user_data['version'] = version
        if user_data["asset"]:
            user_data["seq/asset"] = "asset"
        else:
            user_data["seq/asset"] = "sequence"
            
        return user_data
    
    def _get_version_from_current_file(self, file):
        """ 
        현재 작업하는 파일 버전 가져오는 메서드
        """
        p = re.compile("[v]\d{3}")      
        p_version = p.search(file)  
        if p_version:
            version = p_version.group()[1:]
            return version   
    
    def _task_setting(self):
        """
        task 를 유저에 맞게 설정해주는 메서드 입니다.
        """
        if self.user_data['shot']:  # 현재 link 타입 설정하기
            self.ui.comboBox_link.setCurrentText(self.user_data['shot'])
        elif self.user_data['asset']:
            self.ui.comboBox_link.setCurrentText(self.user_data['asset'])

        if self.user_data['task'].lower() in self.asset_steps_dict:
            self.ui.comboBox_task.setCurrentText(self.asset_steps_dict[self.user_data['task'].lower()])
        else:
            self.ui.comboBox_task.setCurrentText(self.shot_steps_dict[self.user_data['task'].lower()])
            
    def _link_setting(self):
        """
        링크할 asset/shot 을 유저에 맞게 설정해주는 메서드 입니다
        """
        self._show_link_entity()
        if self.user_data['task'].lower() in self.asset_steps_dict:
            self.ui.comboBox_link.setCurrentText(self.user_data['asset'])
        else:
            self.ui.comboBox_link.setCurrentText(self.user_data['shot'])

    def _show_file_detail(self, item, _):
        """ 
        선택한 treewidget 아이템 정보 크게 보여주는 메서드
        """
        text = item.text(0)
        if not item.parent():
            pixmap = QPixmap("/home/rapa/baked/toolkit/config/python/icons/scene.png")         
        else:
            pixmap = QPixmap("/home/rapa/baked/toolkit/config/python/icons/object.png") 
        scaled_pixmap = pixmap.scaled(30, 30) 
        self.ui.label.setPixmap(scaled_pixmap)
        self.ui.label_name.setText(text)

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
        print (f"+++++ _get_path_using_template : {current}")
        
        new_path = ""
        if current in yaml_path:
            root_path = yaml_path[f"{level}_root"]
            new_path = yaml_path[current]["definition"].replace(f"@{level}_root", root_path)
            new_path = new_path.format(**file_info_dict)
            self._check_validate(new_path)
        print ("###", new_path)
        return new_path

    def _get_version_each_node(self):
        # pub파일에 있는 cache 버전
        pass
    
    def _connect_department(self):
        """
        나중에는 ui에서 가져오는 거롤
        """
        reversed_task_dict = dict(map(reversed, self.task_dict.items()))
        task = self.ui.comboBox_task.currentText()
        self.department = reversed_task_dict[task].upper()
        self.dep_class = getattr(department_publish, self.department)(self.tree, self.tool) # 부서 클래스를 인스턴스화 하기
        self._customize_file_type()    

    def _customize_file_type(self):
        """ 
        유저에 맞게 파일 타입 선택지를 좁혀주는 메서드 입니다.
        """
        published_file_type_sg = self.sg.sg.find("PublishedFileType", [["sg_level", "is_not", None]], fields=["code", "sg_task", "sg_ext"])
        filtered_types = [""]
        self.file_type_ext = {}
        for info in published_file_type_sg:
            if info['sg_task'] in [self.department, None]:
                filtered_types.append(info['code'])
                self.file_type_ext[info['code']] = info['sg_ext']
        self.ui.comboBox_type.clear()
        self.ui.comboBox_type.addItems(filtered_types)
        
    def _import_yaml_template(self):
        """ 
        각 파일별로 경로 설정해주는 template.yml 파일을 import 하는 메서드입니다
        """
        with open('/home/rapa/baked/toolkit/config/core/env/sy_template.yml') as f:
            yaml_data = yaml.load(f, Loader=yaml.FullLoader)
            yaml_path = yaml_data["paths"]
            yaml_key = yaml_data["keys"]
        return yaml_path, yaml_key
    
    def _check_validate(self, new_path):
        """저장할 파일 경로가 유효한지 확인하는 메서드 (폴더가 존재하지 않으면 생성해주기)"""
        print (new_path)
        file_path = "/".join(new_path.split("/")[:-1])
        print (f"206/_check_validate : {file_path}")
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        return file_path
        
    def _close_ui(self):
        self.close()

    def _expand_tree(self):
        self.tree.expandAll()
        
    def _collapse_tree(self):
        self.tree.collapseAll()

    def _connect_item_and_type(self, item, _):
        """
        Treewidget item누를 때마다 콤보박스에 내가 선택한 타입 뜨게 하기
        """
        file = item.text(0)
        if not self.publish_dict[file]['file type']:
            self.ui.comboBox_type.setCurrentText('')
        self.ui.comboBox_type.setCurrentText(self.publish_dict[file]['file type'])
        
    def _show_description(self, item, _):
        """
        treewidget 각 아이템별로 저장된 description 보여주는 메서드
        """
        file = item.text(0)
        self.ui.plainTextEdit_description.setPlainText(self.publish_dict[file].get('description', ""))
        
    def _write_description(self):
        """
        수정된 description 딕셔너리에 저장하는 메서드
        """
        item = self.tree.currentItem()
        file = item.text(0)
        if self.ui.plainTextEdit_description.toPlainText():
            self.publish_dict[file]['description'] = self.ui.plainTextEdit_description.toPlainText()
        
    ################################### get shotgrid data ##########################################
        
    def _get_task_type(self):
        """
        shotgrid에서 task 종류 가져오는 메서드
        """
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
        """
        shotgrid 에서 task 와 링크된 entity 가져오는 메서드
        """
        self.ui.comboBox_link.clear()
        task = self.ui.comboBox_task.currentText()[9:]
        link_list = []
        step = self.sg.sg.find("Step", [['description', 'is', task]], fields=["code"])[0]['code']
        link = self.sg.sg.find("Task", [['step.Step.code', 'is', step], ['project.Project.name', 'is', 'baked']], fields=["entity"])
        for item in link:
            link_list.append(item['entity'].get('name'))
        self.ui.comboBox_link.addItems(link_list)
    
    def _put_publish_type_info_dict(self, index):
        """ treewidget 아이템 별로 published type 기록하는 메서드 """
        item = self.tree.currentItem()
        file = item.text(0)
        file_type = self.ui.comboBox_type.currentText()

        if file_type != "":
            self.publish_dict[file]['file type'] = file_type
            item.setText(1, "O")
            item.setForeground(1, QBrush(QColor("light pink")))
    
    def _load_publish_summary(self):
        """ 퍼블리쉬할 데이터 보여주는 메서드 """

        self.ui.textEdit.clear()
        for file, value in self.publish_dict.items(): 
            self.ui.textEdit.append(f'<b>{file}</b>')
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
            image_path = self._get_path_using_template("playblast")
        elif button.text() == "Capture":
            image_path = self._get_path_using_template("capture")
        elif button.text() == "Render":
            ext = self.work.set_render_ext()
            image_path = self._get_path_using_template("render", ext) # 부서별로 펍할 external 입력받기

        path = self._check_validate(image_path)    
        files = glob.glob(f"{path}/*")
        print (path, "---------------------------------------")
        print (files, "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        if not files:
            self.ui.label_thumbnail.setText("No Thumbnail Found")
            self.ui.label_thumbnail.setAlignment(Qt.AlignCenter)
            return

        if button.text() in ["PlayBlast", "Render"]:
            recent_image_file = max(files, key=os.path.getmtime)
            start_frame, last_frame = self._get_frame_number(files) # 프레임 넘버, 경로 정보 저장하기
            self.preview_info = {'input path' : image_path, 
                                 'start frame' : int(start_frame),
                                 'last frame' : int(last_frame)}
        else:
            parse = re.compile("[v]\d{3}")
            for file in files:
                version = parse.search(os.path.basename(file)).group()[1:]
                if version == self.user_data["version"]:
                    recent_image_file = file
                    self.preview_info = {'input path' : image_path,
                                    'start frame' : 1,
                                    'last frame' : 1}
                    pass

        pixmap = QPixmap(recent_image_file) 
        scaled_pixmap = pixmap.scaled(288, 162) 
        self.ui.label_thumbnail.setPixmap(scaled_pixmap) # 가장 최근 사진으로 뽑기
        self.ui.label_thumbnail.repaint()
        print (f"420:: self.preview_info {self.preview_info}")

    def _get_frame_number(self, files):
        """ 
        플레이블라스트, 렌더, 캡처를 통해 받은 파일 경로로 프레임 넘버 가져오기 
        """
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
            image_path = self._get_path_using_template("playblast")
            print (f"image_path : {image_path}")
            self._check_validate(image_path)
            MayaAPI.make_playblast(self, image_path)
            self._show_thumbnail(self.ui.radioButton_playblast)

        elif self.ui.radioButton_capture.isChecked():
            image_path = self._get_path_using_template("capture")
            self._check_validate(image_path)
            print (image_path)
            self.cap = SubWindow_Open(image_path) ### qq
            self.cap.show()
            self._show_thumbnail(self.ui.radioButton_capture)

        elif self.ui.radioButton_render.isChecked():
            ext = self.work.set_render_ext()
            image_path = self._get_path_using_template("render", ext)
            self._check_validate(image_path)  
            self._show_thumbnail(self.ui.radioButon_render)
    
    ######################### PUBLISH 버튼 누르면 발생하는 이벤트 ############################

    def _publish_file_data(self): ########## MAIN ############
        """publish 눌렀을 때 발생하는 이벤트"""

        self._connect_department()
        self._save_file_pub()
        input_path = self.preview_info['input path']
        self._apply_ffmpeg(input_path, self.user_data['project'])
        version = self._create_version_data()
        self._create_published_file(version)
        self._save_file_dev_version_up()
        self.close()
    
    def _save_file_pub(self):
        """ (1) pub 파일에 저장하는 메서드 (scene파일, cache만) (version 작업 파일 그대로) """
        """ 펍할때는 무조건 scene파일 올리는거니까 scene파일 선택되어있지 않으면 versions로만 올린다는 이야기 """
        """ 펍한다고 하면 펍한다고 체크한 데이터들로만 진행 """

        print ("----------", list(self.publish_dict.keys()))
        scene_file = list(self.publish_dict.keys())[0]
        print (f"--------451 scene_file {scene_file}---------")
        try:
            self._get_path_for_selected_files()
        except:
            return
        
        for file in self.publish_dict: # publish dict에 있는 확장자를 이용해서 pub 경로 만들기
            try:
                ext = self.publish_dict['ext']
            except:
                ext = ''
            self._get_path_using_template('pub', ext)

        self.dep_class.save_data(self.publish_dict)
        print (f"476: save_file_pub: {self.publish_dict}")
    
    def _get_path_for_selected_files(self):
        """ 선택된 파일 타입에 따라 경로 만들어서 딕셔너리에 넣어주기 """
        self.ui.label_info_2.clear()
        for file, file_info in self.publish_dict.items():
            print (file,  file_info['file type'])
            try:
                file_info['file type']### check empty data
            except:
                self.ui.label_file_info_2.setText(f"Please select file type")
                return False
            print (3333, file_info['ext'], self.file_type_ext, self.file_type_ext[file_info['file type']])
            file_info['ext'] = self.file_type_ext[file_info['file type']]
            self.user_data['group'] = file
            path = self._get_path_using_template("pub", file_info['ext'])
            file_info['path'] = path
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
        self.preview_info['output_path_jpg'] = self._export_slate_image(output_path)
        print(f"%%%%%%%%%%%%%%%%%%%%%{self.preview_info}")

    def _export_slate_image(self,  input_mov):
        """ffmpeg 이미지로 한장 가져오기"""
        mov_dir = os.path.dirname(input_mov)
        mov_name = os.path.basename(input_mov)
        mov_name, _ = os.path.splitext(mov_name)
        img_path = f"{mov_dir}/{mov_name}.jpg"
        frame_number = 24
        command = ['ffmpeg', '-y', '-i', input_mov, '-vf', f"select='eq(n\,{frame_number})'", '-vsync', 'vfr', '-frames:v', '1', img_path]
        subprocess.run(command)
        return img_path

    def _save_file_dev_version_up(self):
        """ (2) dev 파일에 저장하는 메서드 (dev 폴더에 저장할) """
        """ dev에는 scene파일만 cache들은 저장 안됨 + 썸네일 저장 """
        self.user_data['version'] = self._make_version_up() # scene 파일
        new_path = self._get_path_using_template('dev')
        self.work.save_scene_file(new_path)
    
    def _make_version_up(self):
        """버전 업해주는 메서드"""
        user_info = self.user_data
        file_path = self._get_path_using_template('dev')
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~``")
        print (file_path)
        if os.path.exists(file_path):
            version = int(user_info["version"])
            version += 1
            str_version = str(version)
            new_version = f"{str_version.zfill(3)}" 
        print (new_version)
        return new_version
    
    ############### 샷그리드에 파일 올리는 메서드들은 따로 파일 만들예정 ###############
    
    def _create_version_data(self):
        """ (5) 샷그리드 versions에 오리는 메서드 """
        print (f"REVIEW     /// {self.publish_dict}")

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
        if "Asset" in self.ui.comboBox_task.currentText():
            asset = self.ui.comboBox_link.currentText()
            shot = None
        else:
            shot = self.ui.comboBox_link.currentText()
            asset = None
        print("#####################################")
        print(version, task, description, preview_path, shot, asset)
        version = self.sg.create_new_version_entity(version, task, description, preview_path, shot, asset)
        return version

    def _create_published_file(self, version):
        """ (4) 샷그리드 published_file 에 pub 파일들 올리는 메서드 """
        print (f"PUBLISHED /// {self.publish_dict}")
        print (version)
        # 현재 나와 버전 code를 가진 version을 가져온다
        last_version = self.sg.sg.find_one("Version", 
                                           [['code', 'is_not', f"v{self.user_data['version']}"], ['sg_task', 'is', version['sg_task']], ['entity', 'is', version['entity']]],
                                           ['published_files', 'code'], 
                                           order=[{'field_name': 'created_at', 'direction': 'desc'}])
        print ("****", last_version)
        # 구한 version에 연결된 PublishedFiles 리스트를 가져온다
        pub_files_list = {}
        if last_version:
            for file in last_version['published_files']:
                pub_files_list[file['name']] = file
            # for file in last_version['published_files']:
            #     file = self.sg.sg.find_one("PublishedFile", 
            #                                 [['id','is',file['id']]], 
            #                                 ['id', 'code'])
            #     pub_files_list[file['code']] = file # pub_files_list['ABC_0010_ANI_v001.abc] = {Published_File_Entity}

        for detail in self.publish_dict.values():
            # 현재 새로 올리려는 파일의 v000을 제외한 앞 부분을 읽어와서 비교한 뒤
            file_path = detail['path']
            if pub_files_list :
                parse = re.compile("[v]\d{3}")
                ver = parse.search(os.path.basename(file_path)).group()
                key_str = os.path.basename(file_path).split(ver)[0]
                key = next((k for k in pub_files_list.keys() if key_str in k), None)
                if key :
                    pub_files_list.pop(key)
                    # 같은 이름의 파일이라면 pub_files_list에서 제외해준다
            description = detail['description']
            published_file_type = detail['file type']
            preview_path = self.preview_info['output_path_jpg']

            self.sg.create_new_publish_entity(version, file_path, description, preview_path, published_file_type)

        for pub_file in pub_files_list.values():
            # 새로운 값이 create되지 않은 파일들은 새로운 version을 version field에 업데이트 해준다
            print (f"res = {pub_file}")
            self.sg.sg.update("PublishedFile", pub_file['id'], {"version" : version})

if __name__ == "__main__":
    app = QApplication(sys.argv) 
