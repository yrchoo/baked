
from PySide6.QtWidgets import QApplication, QMessageBox, QWidget
from PySide6.QtWidgets import QListWidgetItem

from PySide6.QtCore import Qt

from PySide6.QtGui import QPixmap

import shotgrid_total_profile
from login import Login
import sys

from shotgrid.user_env_val import Make_User_Data
from shotgun_api3 import shotgun
import requests

from ui_files.ui_Shotgrid_user import Ui_Form
from loader import Loader

class UserProfile(QWidget):
    def __init__(self):
        super().__init__()
      
        self.setup_ui()
        self.sg = self.connect_sg()

        #샷그리드가 다운되었을 경우.
        if not self.sg:
            print ("failed connect")

        #Baked project ID
        self.project_id = 155
    
        self.get_user_profile()
        self.get_user_name_list()
        self.get_total_user_profile()
        self._set_ui()
        
    def _set_ui(self):
        self.ui.comboBox_user.currentIndexChanged.connect(self.baked_name)
        self.ui.comboBox_user.currentIndexChanged.connect(self.baked_email)
        self.ui.comboBox_user.currentIndexChanged.connect(self.baked_project)
        self.ui.comboBox_user.currentIndexChanged.connect(self.baked_role)
        self.ui.comboBox_user.currentIndexChanged.connect(self.get_project_data)
        self.ui.comboBox_user.currentIndexChanged.connect(self.get_task_data)
        self.ui.comboBox_user.currentIndexChanged.connect(self.get_seq_shot_asset_data)
        self.ui.comboBox_shot_asset.currentIndexChanged.connect(self.find_asset_type_data)
        self.ui.comboBox_shot_asset.currentIndexChanged.connect(self.get_asset_type_data)
        # self.ui.comboBox_shot_asset.currentIndexChanged.connect(self.display_image)
        self.ui.comboBox_shot_asset.currentIndexChanged.connect(self.update_notes_display_reviewer)
        self.ui.listWidget_note_subject.itemClicked.connect(self.update_notes_display_asset_shot_content)
        self.ui.pushButton_add.clicked.connect(self.get_total_user_list)
        self.ui.pushButton_login.clicked.connect(self.update_login)
      
    def connect_sg(self):
        try:
            URL = "https://4thacademy.shotgrid.autodesk.com"
            script_name =  "baked"
            script_key =  "p)ghhlikzcyzwq4gdgZpnhmkz"
            sg = shotgun.Shotgun(URL,script_name,script_key)
            return sg
        
        except shotgun.AuthenticationFault:
            self.show_error_message("failed to login")
            return False
        except Exception as e:
            self.show_error_message(f"error : {e}")
            return False
        
    #Shot 과 Asset 에 대한 썸네일.
    def display_image(self):
        asset = self.ui.comboBox_shot_asset.currentText()
        filters_for_asset = [["code", "is", asset], ["project", "is", {"type": "Project", "id": self.project_id}]]
        fields_for_asset = ["image"]

        #Find Asset Image
        datas = self.sg.find("Asset", filters_for_asset, fields_for_asset)
        if datas and "image" in datas[0]:
            image_url = datas[0]["image"]
            if image_url:
                response = requests.get(image_url)
                if response.status_code == 200: # It's a HTTP status code, it means "OK"
                    image_data = response.content
                    pixmap = QPixmap()
                    pixmap.loadFromData(image_data)
                    self.ui.label_image.setPixmap(pixmap)
                    self.ui.label_image.setScaledContents(True)
                    return
            else:""
                # print("썸네일 이미지가 없습니다. : ", image_url)

        self.ui.label_image.clear()
        self.ui.label_image.setText("No Image")

        shot = self.ui.comboBox_shot_asset.currentText()
        filters_for_asset = [["code", "is", shot], ["project", "is", {"type": "Project", "id": self.project_id}]]
        fields_for_asset = ["image"]

        #Find Shot Image
        datas = self.sg.find("Shot", filters_for_asset, fields_for_asset)
        if datas and "image" in datas[0]:
            image_url = datas[0]["image"]
            if image_url:
                response = requests.get(image_url)
                if response.status_code == 200:
                    image_data = response.content
                    pixmap = QPixmap()
                    pixmap.loadFromData(image_data)
                    self.ui.label_image.setPixmap(pixmap)
                    self.ui.label_image.setScaledContents(True)
                    return
            else:""
                # print("썸네일 이미지가 없습니다. : ", image_url)

        self.ui.label_image.clear()
        self.ui.label_image.setText("No Image")

    #프로젝트 아이디로 HumanUser 의 정보를 가져온다.
    def get_user_profile(self):
        filters = [["projects", "is", {"type": "Project", "id": self.project_id}]]
        fields = ["id", "login", "name", "sg_role", "projects"] 
        # sg_role 말고 sg_step으로 변경해서 가져온 다음에 role을 빼고 task 정보 하나만 뜨게 해주세요 *****
        # projects 말고 유저 정보에 현재 진행중인 프로젝트 이름 하나만 뜨게 해주세요 *****
        self.project_user_datas = self.sg.find("HumanUser", filters=filters, fields=fields)
        # 사람 이름을 key로 하는 dictionary 형식으로 바꿔주세요 *****
        # 위에 self 변수로 저장해놓고 왜 여기서 또 리스트로 반환하는지???????????????????????? *****
        baked_profile = []
        if self.project_user_datas:
            for data in self.project_user_datas:
                if isinstance(data, dict):
                    baked_profile.append(data)
        return baked_profile

    #사용자 이름과의 매치를 통해 사용자에 대한 Task, entity field 의 Shot,Asset 정보를 가져온다.
    def get_project_data(self):
        user_name = self.ui.comboBox_user.currentText()

        for user in self.project_user_datas: # 딕셔너리로 self.project_user_datas 바꿔서 for문 줄여주세요 *****
            if user['name'] == user_name:
                user_ent = user

        # shotgrid_data *********************
        filters_for_data = [["task_assignees", "is", user_ent]]
        fields_for_data = ["content", "sg_status_list","entity"]
        datas = self.sg.find("Task", filters_for_data, fields_for_data)
        return datas

    #content 의 Task 정보 입력.
    def get_task_data(self):
        datas = self.get_project_data() # 이 값이 필요할 때 마다 계산하지 말고 해당 사람한테 assign된 데이터들을 따로 딕셔너리 같은 곳에 저장해놓고 불러와서 사용해주세요... *****
        task = [i["content"] for i in datas]
        if task != "":
            self.ui.lineEdit_task.setText(str(task[0]))
        
    #entity 의 Shot,Asset 정보 입력.
    def get_seq_shot_asset_data(self):
        datas = self.get_project_data() # 이 값이 필요할 때 마다 계산하지 말고 해당 사람한테 assign된 데이터들을 따로 딕셔너리 같은 곳에 저장해놓고 불러와서 사용해주세요... *****
        self.seq_shot = [i["entity"] for i in datas]
        self.shot_list = []
        self.asset_list = []

        for i in self.seq_shot:

            self.ui.comboBox_shot_asset.clear()

            if i["type"] == "Shot":
                self.shot_list.append(i["name"])
            
                for j in self.shot_list:
                    self.ui.comboBox_shot_asset.addItem(str(j))
                    self.ui.label_shot_asset.clear()
                    self.ui.label_shot_asset.setText("Shot :")

            if i["type"] == "Asset":
                self.asset_list.append(i["name"])

                for j in self.asset_list:
                    self.ui.label_shot_asset.clear()
                    self.ui.comboBox_shot_asset.addItem(str(j))
                    self.ui.label_shot_asset.setText("Asset :")

    # asset 데이터와 프로젝트 아이디로 asset type 조회.
    def find_asset_type_data(self):
        
        asset = self.ui.comboBox_shot_asset.currentText()
        filters_for_asset = [["code", "is", asset], ["project", "is", {"type": "Project", "id": self.project_id}]]
        fields_for_asset = ["sg_asset_type"]
        
        datas = self.sg.find("Asset", filters_for_asset, fields_for_asset)
        return datas
    
    #asset type 데이터 입력.
    def get_asset_type_data(self):
        datas = self.find_asset_type_data() 
        if datas:
            asset_type = [i["sg_asset_type"] for i in datas]
            self.ui.label_asset_type.clear()
            self.ui.label_type.setText("Type :")
            self.ui.label_asset_type.setText(','.join(asset_type))

    #사용자정보를 조회한 데이터에서 name 데이터를 가져와 입력.
    def get_user_name_list(self):
        baked_profile = self.get_user_profile() #????????????????????*****
        self.ui.comboBox_user.addItem("")
        self.ui.comboBox_user.setCurrentText("")
        name_list = []
        for data in baked_profile:
            if "name" in data:
                name_list.append(data["name"])
        self.ui.comboBox_user.addItems(name_list)
   
    def baked_name(self):
        name = self.ui.comboBox_user.currentText()
        self.ui.label_name.setText(name)

    #사용자정보를 조회한 데이터에서 이메일 데이터를 가져와 이름과 매치.
    def baked_email(self):
        baked_profile = self.get_user_profile() # ????????????????????????????????*****
        l_name = [d["name"] for d in baked_profile]
        email = [d["login"] for d in baked_profile]
        name_email = { i:r for i,r in zip(l_name,email)}
    
        for key, value in name_email.items():
            if key == self.ui.comboBox_user.currentText():
                self.ui.label_email.setText(str(value))

    #사용자정보를 조회한 데이터에서 프로젝트 데이터를 가져와 이름과 매치.
    def baked_project(self):
        baked_profile = self.get_user_profile() # ????????????????????????????????*****
        l_name = [d["name"] for d in baked_profile]
        Project = [d["projects"] for d in baked_profile]
        name_project = {i:r for i,r in zip(l_name,Project)}
        
        for key, value in name_project.items():
            if key == self.ui.comboBox_user.currentText():
                project_name_list = []
                for i in range(len(value)):
                    project_name = value[i]["name"]
                    project_name_list.append(project_name)
                    self.ui.label_project.setText((','.join(project_name_list)))
                    
    #사용자정보를 조회한 데이터에서 Role 데이터를 가져와 이름과 매치.
    def baked_role(self):
        baked_profile = self.get_user_profile() # ?????????????????????????*****
        l_name = [d["name"] for d in baked_profile]
        Role = [d["sg_role"] for d in baked_profile]

        name_Role = {i:r for i,r in zip(l_name,Role)}
        for key, value in name_Role.items():
            if key == self.ui.comboBox_user.currentText():
                self.ui.label_role.setText(str(value))
              
    #모든 프로젝트의 HumanUser 데이터 조회.
    def get_total_user_profile(self):
        filters = []
        fields = ["id", "login", "name", "sg_role","projects"]
        datas = self.sg.find("HumanUser", filters=filters, fields=fields)
        return datas
    
    #모든 프로젝트 사용자 데이터를 서브윈도우로 전달.
    def get_total_user_list(self):
        datas = self.get_total_user_profile()
        if datas:  
            self.sub_window = shotgrid_total_profile.TotalProfile(datas) 
            self.sub_window.show() 
        else:
            print("데이터가 비어 있습니다.")
            
    #Shot 과 Asset 에 대한 Reviewer Comment 
    def update_notes_display_reviewer(self):
        shot = self.ui.comboBox_shot_asset.currentText()
        asset = self.ui.comboBox_shot_asset.currentText()

        # 이렇게 나눠서 찾지 말고 notes라는 엔티티에 연결된 shot, asset 이름을 가지고서 Task를 찾고 해당 task에 연결된 Note를 검색해와주세요.. *****

        # Shot에 대한 Comment 업데이트
        self.ui.listWidget_note_subject.clear()
        if shot:
            shot_id = self.get_entity_id_by_code("Shot", shot)
            if shot_id:
                notes_data = self.get_open_notes("Shot", shot_id)
                # 노트 데이터가 있는 경우,'subject'와 'content' 필드에서 comment 의 주제와 내용을 가져옴
                if notes_data:  
                    subject = [d["subject"] for d in notes_data]
                    content = [d["content"] for d in notes_data]
                    date = [d["created_at"] for d in notes_data]
                    
                    self.subject_date = {i:r for i,r in zip(subject,date)}
                    self.subject_content = { i:r for i,r in zip(subject,content)}
                    
                    for sub,date in self.subject_date.items():
                        text = f"{sub} ({date.strftime('%Y-%m-%d %H:%M:%S')})"
                        item = QListWidgetItem(text)
                        item.setData(Qt.UserRole, sub)
                        self.ui.listWidget_note_subject.addItem(item)
                        self.ui.label_opennote.setText("Shot OpenNote")
        
                else: self.ui.plainTextEdit_note_content.clear()
                
            # 필요없는 else는 지워주세요 ****************8
            else:
                ""
        else:
            ""

        # Asset에 대한 Comment 업데이트
        if asset:
            asset_id = self.get_entity_id_by_code("Asset", asset)
            if asset_id:
                notes_data = self.get_open_notes("Asset", asset_id)
                # 노트 데이터가 있는 경우, 'subject'와 'content' 필드에서 노트의 주제와 내용을 가져옴
                if notes_data:  
                    
                    subject = [d["subject"] for d in notes_data]
                    content = [d["content"] for d in notes_data]
                    date = [d["created_at"] for d in notes_data]
                    
                    self.subject_date = {i:r for i,r in zip(subject,date)}
                    self.subject_content = { i:r for i,r in zip(subject,content)}
                
                    for sub,date in self.subject_date.items():
                        text = f"{sub} ({date.strftime('%Y-%m-%d %H:%M:%S')})"
                        item = QListWidgetItem(text)
                        item.setData(Qt.UserRole, sub)
                        self.ui.listWidget_note_subject.addItem(item)
                        self.ui.label_opennote.setText("Asset OpenNote")
                  
                else: self.ui.plainTextEdit_note_content.clear()
            
            else:
               ""
        else:
           ""

    #사용자가 선택한 Reviewer 제목에 대한 내용 입력.
    def update_notes_display_asset_shot_content(self):
        # 현재 선택된 Reviewer 제목.
        selected_item = self.ui.listWidget_note_subject.currentItem()
      
        if selected_item:
            selected_subject = selected_item.data(Qt.UserRole)
            content = self.subject_content.get(selected_subject, "No Comment")
            self.ui.plainTextEdit_note_content.clear()
            self.ui.plainTextEdit_note_content.setPlainText(content)
        else:
            self.ui.plainTextEdit_note_content.clear()
            self.ui.plainTextEdit_note_content.setPlainText("No Comment")

    #Entity type의 Asset 과 Shot 에 대한 id 조회.
    def get_entity_id_by_code(self, entity_type, entity_code):
    
        filters = [["code", "is", entity_code], ["project", "is", {"type": "Project", "id": self.project_id}]]
        fields = ["id"]
        try:
            entity_data = self.sg.find_one(entity_type, filters, fields)
            return entity_data["id"] if entity_data else None
        except Exception as e:
            self.show_error_message(f"Error entity Id: {e}")
            return None

    #note link 필드의 entity type과 id , 프로젝트 아이디로 comment 정보조회.
    def get_open_notes(self, entity_type, entity_id):

        if not entity_id:
            return []
            
        # note_links 필드의 엔티티 타입과 ID를 사용하여 comment 조회.
        filters_for_notes = [
            ["note_links", "is", {"type": entity_type, "id": entity_id}], 
            ["project", "is", {"type": "Project", "id": self.project_id}]
        ]
        # 'subject'와 'content' 필드를 사용하여 comment 의 주제와 내용을 가져옴
        fields_for_notes = ["subject", "content","created_at"]  

        try:
            notes_data = self.sg.find("Note", filters_for_notes, fields_for_notes)
            return notes_data
        except shotgun.Fault as e:
            self.show_error_message(f"Error notes: {e}")
            return []

    #샷그리드가 작동할경우,사용자 정보를 sh파일로 Loader에 전달하고 login
    def update_login(self):
        
        # sg = self.connect_sg() # 여기서 또 호출하지 마세요... 처음에 연결해서 데이터를 가져올 때 해당 sg를 self 변수로 생성해서 그걸로 판단하세요 임시로 고쳐두었습니다 *****
        if self.sg: # 제대로 로그인 안됩니다.....
            name = self.ui.label_name.text()
            project = "baked" 
            shot = self.ui.comboBox_shot_asset.currentText()
            asset = self.ui.comboBox_shot_asset.currentText()
            task = self.ui.lineEdit_task.text()
            asset_type = self.ui.label_asset_type.text()

            #사용자 데이터 전달.
            Make_User_Data(name=name,project=project,shot=shot,asset=asset,task=task,asset_type=asset_type)
            self.close()

        #샷그리드가 다운되었을경우 , 오류메시지를 내보내고 새로운 로그인 창으로 연결.
        
        # 이런 구조 말고 처음에 로그인 창이 뜰 때 샷그리드가 연결되지 않은 경우 바로 새로운 로그인 창이 뜨게 해주세요 *****
        # 샷그리드가 죽어있으면 이미 처음부터 로그인창에 필요한 사람 데이터를 못 불러옴... *****
        else:
            self.show_error_message("ShorGrid Error")
            self.sub_window = Login(self)
            self.sub_window.show() 
            

               
    #오류메시지.
    def show_error_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("ShotGrid Error")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()



    def setup_ui(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)



if __name__ == "__main__":
     app = QApplication(sys.argv)
     win = UserProfile()
     win.show()
     app.exec()




