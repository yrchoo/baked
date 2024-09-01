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
import subprocess
reload(department_publish)
reload(work_in_maya)
reload(shotgrid.fetch_shotgrid_data)


from shotgrid.fetch_shotgrid_data import ShotGridDataFetcher
class Review(QWidget):
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
        pass

        self.ui.pushButton_cancel.clicked.connect(self._close_ui)
        self.ui.pushButton_upload.clicked.connect(self._create_version_data)
        self.ui.pushButton_thumbnail.clicked.connect(self._make_thumbnail)

        self.ui.comboBox_task.currentIndexChanged.connect(self._show_link_entity)
        self.ui.comboBox_task.currentTextChanged.connect(self._connect_department)

        self.button_group = QButtonGroup()
        button_list = [self.ui.radioButton_playblast, self.ui.radioButton_capture, self.ui.radioButton_render]
        for button in button_list:
            self.button_group.addButton(button)
        self.button_group.buttonClicked.connect(self._show_thumbnail)

    def _set_ui(self):
        """ui 셋업해주는 메서드"""
        ui_file_path = '/home/rapa/baked/toolkit/config/python/upload_review.ui' 
        ui_file = QFile(ui_file_path)

        loader = QUiLoader()
        self.ui = loader.load(ui_file, self)  
        ui_file.close()

    def _initial_ui_setting(self):
        """초기 ui 세팅하는 메서드"""
        self.show()

        user_data = self.sg.user_info
        self.user_data = self._get_user_info(user_data) ## 현재 유저 정보, 작업 파일 딕셔너리로 저장
        print("**************************************")
        print (self.user_data)
        print("**************************************")

        if self.user_data['shot'] != "":
            self.ui.comboBox_link.setCurrentText(self.user_data['shot'])
        else:
            self.ui.comboBox_link.setCurrentText(self.user_data['asset'])

    def _link_setting(self):
        self._show_link_entity()
        if self.user_data['task'].lower() in self.asset_steps_dict:
            self.ui.comboBox_link.setCurrentText(self.user_data['asset'])
        else:
            self.ui.comboBox_link.setCurrentText(self.user_data['shot'])

    def _task_setting(self):
        if self.user_data['task'].lower() in self.asset_steps_dict:
            self.ui.comboBox_task.setCurrentText(self.asset_steps_dict[self.user_data['task'].lower()])
        else:
            self.ui.comboBox_task.setCurrentText(self.shot_steps_dict[self.user_data['task'].lower()])

    def _get_user_info(self, user_data):
        """ 유저에 대한 정보 가저오는 메서드 """ # 임시 설정 
        """ 유저 커스텀 버튼 있으면 좋을듯 """
        
        user_data['tool'] = self.tool
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

    def _close_ui(self):
        """UI창 끄는 메서드"""
        self.close()
              
    ################################### get shotgrid data ##########################################
        
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

    ############################# Flow: publish/versions에 올리기 ########################################
    
    def _show_thumbnail(self, button):
        """썸네일 보여주는 메서드"""

        image_path = ""
        if button.text() == "PlayBlast":
            image_path = self._get_path_using_template("playblast")
        elif button.text() == "Capture":
            image_path = self._get_path_using_template("capture")
        elif button.text() == "Render":
            image_path = self._get_path_using_template("render") # 부서별로 펍할 external 입력받기

        path = self._check_validate(image_path)    
        files = glob.glob(f"{path}/*")
        print (path, "---------------------------------------")
        print (files, "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        if not files:
            self.ui.label_thumbnail.setText("No Thumbnail Found")
            self.ui.label_thumbnail.setAlignment(Qt.AlignCenter)
            return

        if len(files) > 1:
            recent_image_file = max(files, key=os.path.getmtime)
            start_frame, last_frame = self._get_frame_number(files) # 프레임 넘버, 경로 정보 저장하기
            self.preview_info = {'input path' : image_path, 
                                 'start frame' : int(start_frame),
                                 'last frame' : int(last_frame)}
        else:
            recent_image_file = image_path
            self.preview_info = {'input path' : image_path}

        pixmap = QPixmap(recent_image_file) 
        scaled_pixmap = pixmap.scaled(288, 162) 
        self.ui.label_thumbnail.setPixmap(scaled_pixmap) # 가장 최근 사진으로 뽑기
        self.ui.label_thumbnail.repaint()
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
            image_path = self._get_path_using_template("playblast")
            print (f"image_path : {image_path}")
            self._check_validate(image_path)
            MayaAPI.make_playblast(self, image_path)
            self._show_thumbnail(self.ui.radioButton_playblast)

        elif self.ui.radioButton_capture.isChecked():
            image_path = self._get_path_using_template("capture")
            self._check_validate(image_path)
            print (image_path, "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz")
            self.cap = SubWindow_Open(image_path) ### qq
            self.cap.show()
            self._show_thumbnail(self.ui.radioButton_capture)

        elif self.ui.radioButton_render.isChecked():
            image_path = self._get_path_using_template("render")
            self._check_validate(image_path)  
            self._show_thumbnail(self.ui.radioButon_render)

    def _apply_ffmpeg(self, input_path, project_name):
        """ (3) ffmpeg 만드는 메서드"""
        """ 예린님 코드로 연결시키기"""
        output_path = self._get_path_using_template("ffmpeg")
        start_frame = self.preview_info['start frame']
        last_frame = self.preview_info['last frame']
        MayaAPI.make_ffmpeg(self, input_path, output_path, project_name, start_frame, last_frame)
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

if __name__ == "__main__":
    app = QApplication(sys.argv) 
