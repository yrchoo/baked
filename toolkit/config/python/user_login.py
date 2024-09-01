from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtWidgets import QWidget, QListWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from offline_login import Login
from ui_files.ui_Shotgrid_user import Ui_Form
from shotgun_api3 import Shotgun
from shotgrid.user_env_val import Make_User_Data
import sys
import shotgrid_total_profile

class UserProfile(QWidget):
    def __init__(self):
        super().__init__()
        self.sg = self.connect_sg()
        
        if not self.sg:
            self.open_offline_login_window()
            return

        self.setup_ui()
        
        self.user_tasks = None
        self.seq_shot = []
        # Baked project ID
        self.project_id = 155
        self.project_user_dict = {}

        self.load_user_data()
        self.insert_user_name_combobox()
        self.setup_ui_connect()

        self.show()
        
    def setup_ui(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    def setup_ui_connect(self):
        self.ui.comboBox_user.currentIndexChanged.connect(self.handle_user_selection)
        self.ui.comboBox_user.currentIndexChanged.connect(self.insert_seq_shot_asset_combobox)
        self.ui.comboBox_shot_asset.currentIndexChanged.connect(self.refresh_asset_info_and_notes)
        self.ui.pushButton_add.clicked.connect(self.show_total_user_list)
        self.ui.pushButton_login.clicked.connect(self.save_and_close)
        self.ui.listWidget_note_subject.currentItemChanged.connect(self.display_selected_note_content)

    def connect_sg(self):
        try:
            URL = "https://4thacademy.shotgrid.autodesk.com"
            script_name = "baked"
            script_key = "p)ghhlikzcyzwq4gdgZpnhmkz"
            sg = Shotgun(URL, script_name, script_key)
            return sg
        
        # except Shotgun.AuthenticationFault: # ***** 주소 오류나면 여기서 멈추는데... 확인 부탁드립니다!
        #     self.show_error_message("Failed to login to ShotGrid")
        #     return None
        except Exception as e:
            self.show_error_message(f"Error : {e}")
            return None
        
    #프로젝트에 대한 사용자 정보를 가져옵니다.
    def load_user_data(self):
        filters = [["projects", "is", {"type": "Project", "id": self.project_id}]]
        fields = ["id", "login", "name", "sg_step", "projects"]
        self.project_user_dict = {user["name"]: user for user in self.sg.find("HumanUser", filters, fields)}
    
    #사용자의 이름 등록.
    def insert_user_name_combobox(self):
        self.ui.comboBox_user.clear()
        self.ui.comboBox_user.addItem("")
        self.ui.comboBox_user.addItems(self.project_user_dict.keys())

    #사용자의 프로필 정보 
    def update_user_profile_info(self):
        # self.ui.comboBox_shot_asset.clear()

        selected_name = self.ui.comboBox_user.currentText()
        user_data = self.project_user_dict.get(selected_name)
        if user_data:
            self.ui.label_name.setText(user_data["name"])
            self.ui.label_email.setText(user_data["login"])
            project_names = [project["name"] for project in user_data.get("projects", [])]
            self.ui.label_project.setText(", ".join(project_names))
        else:
            self.ui.label_name.clear()
            self.ui.label_email.clear()
            self.ui.label_project.clear()
    
    #선택된 사용자에 따른 데이터 업데이트.
    def handle_user_selection(self):
        self.update_user_profile_info()
        selected_name = self.ui.comboBox_user.currentText()
        user_data = self.project_user_dict.get(selected_name)
        
        self.ui.comboBox_shot_asset.clear()
        self.ui.label_shot_asset.clear()
        self.ui.label_asset_type.clear()
        self.ui.listWidget_note_subject.clear()

        if user_data:
            self.user_tasks = self.get_project_data()
            self.insert_task_data()
            self.insert_seq_shot_asset_combobox()
            self.update_notes_list_for_user()
        else:
            self.ui.comboBox_shot_asset.clear()
            self.ui.label_shot_asset.clear()
            self.ui.label_asset_type.clear()
            self.ui.listWidget_note_subject.clear()
    
    
     ######################################################################################
            
    #선택된 사용자에 대한 프로젝트 정보를 가져온다.
    def get_project_data(self):
        selected_name = self.ui.comboBox_user.currentText()
        user_data = self.project_user_dict.get(selected_name)
        if not user_data:
            return []
        filters = [["task_assignees", "is", user_data]]
        fields = ["content", "sg_status_list", "entity"]
        self.user_tasks = self.sg.find("Task", filters, fields)
        return self.user_tasks

    #사용자에 등록된 TASK 업데이트
    def insert_task_data(self):
      
        if self.user_tasks is None: 
            self.user_tasks = self.get_project_data()

        if self.user_tasks:
            self.ui.lineEdit_task.setText(self.user_tasks[0]["content"])
        else:
            self.ui.lineEdit_task.clear()
            
    #사용자의 TASK 를 기반으로 SHOT,ASSET 의 콤보박스 데이터 업데이트.
    def insert_seq_shot_asset_combobox(self):
        if self.user_tasks is None: 
            self.user_tasks = self.get_project_data()

        self.seq_shot = [task["entity"] for task in self.user_tasks] if self.user_tasks else []
        self.ui.comboBox_shot_asset.clear()

        shot_names = [entity["name"] for entity in self.seq_shot if entity["type"] == "Shot"]
        asset_names = [entity["name"] for entity in self.seq_shot if entity["type"] == "Asset"]
        
        if shot_names and not asset_names:
            self.ui.comboBox_shot_asset.addItems(shot_names)
            self.ui.label_shot_asset.setText("Shot:")
            self.ui.label_asset_type.clear()
        elif asset_names and not shot_names:
            self.ui.comboBox_shot_asset.addItems(asset_names)
            self.ui.label_shot_asset.setText("Asset:")
        elif shot_names and asset_names:
            self.ui.comboBox_shot_asset.addItems(shot_names + asset_names)
            self.ui.label_shot_asset.setText("Shot and Asset:")

    #comboBox_shot_asset 값의 변경에 따른 업데이트
    def refresh_asset_info_and_notes(self):
        self.update_asset_type_info()
        self.update_notes_for_selected_entity()
        

    #선택된 데이터가 ASSET 데이터일 경우 type 디스플레이.
    def update_asset_type_info(self):
        selected_asset = self.ui.comboBox_shot_asset.currentText()
        if not selected_asset:
            self.ui.label_asset_type.clear()
            return
        is_asset = self.ui.label_shot_asset.text() == "Asset:"
        if is_asset:
            filters = [["code", "is", selected_asset], ["project", "is", {"type": "Project", "id": self.project_id}]]
            fields = ["sg_asset_type"]
            data = self.sg.find("Asset", filters, fields)
            if data and data[0].get("sg_asset_type"):
                asset_type = data[0]["sg_asset_type"]
                self.ui.label_asset_type.setText(f"Type: {asset_type}")
        else:
            self.ui.label_asset_type.clear()
            
    #엔티티 id 값 가져오기.
    def get_entity_id_by_code(self, entity_type, entity_code):
        filters = [["code", "is", entity_code], ["project", "is", {"type": "Project", "id": self.project_id}]]
        fields = ["id"]
        try:
            entity_data = self.sg.find_one(entity_type, filters, fields)
            return entity_data["id"] if entity_data else None
        except Exception as e:
            self.show_error_message(f"Error : {e}")
            return None

    ##########################################################################################


    #선택된 SHOT,ASSET 에 대한 OPEN_NOTE
    def update_notes_for_selected_entity(self):
        selected_entity = self.ui.comboBox_shot_asset.currentText()
        entity_type = "Shot" if "Shot" in self.ui.label_shot_asset.text() else "Asset"
        entity_id = self.get_entity_id_by_code(entity_type, selected_entity)
        if entity_id:
            notes = self.get_open_notes_generic(entity=(entity_type, entity_id))
            self.get_note_list(notes)

            
    #선택된 사용자에 대한 Open Note 데이터 업데이트.
    def update_notes_list_for_user(self):
        selected_name = self.ui.comboBox_user.currentText()
        if not selected_name:
            self.ui.listWidget_note_subject.clear()  
            return
        user_data = self.project_user_dict.get(selected_name)
        if not user_data:
            self.ui.listWidget_note_subject.clear() 
            return
        
        open_notes = self.get_open_notes_generic(user=user_data)
        self.get_note_list(open_notes)
    
    #선택된 사용자에 따른 Open Note 데이터를 가져옵니다.
    def get_open_notes_generic(self, entity=None, user=None):
        filters = []
        if user:
            filters = [
                ["note_links", "is", user],
                ["project", "is", {"type": "Project", "id": self.project_id}]
            ]
        elif entity:
            entity_type, entity_id = entity
            filters = [
                ["note_links", "is", {"type": entity_type, "id": entity_id}],
                ["project", "is", {"type": "Project", "id": self.project_id}]
            ]
        
        fields = ["subject", "content", "created_at"]

        try:
            return self.sg.find("Note", filters, fields)
        except Exception as e:
            self.show_error_message(f"Error: {e}")
            return []

    #Open Note Subject 디스플레이
    def get_note_list(self, notes):
        self.ui.listWidget_note_subject.clear()
        if notes:
            for note in notes:
                item = QListWidgetItem(note["subject"]) 
                item.note_content = note["content"]  
                self.ui.listWidget_note_subject.addItem(item)
        else: self.ui.listWidget_note_subject.clear()
        
    #선택된 Open Note subject 에 대한 content 디스플레이
    def display_selected_note_content(self, current ):
        if current:
            self.ui.plainTextEdit_note_content.setPlainText(current.note_content) 
        else:
            self.ui.plainTextEdit_note_content.clear()
            
##########################################################################################

    #전체 사용자 프로필을 서브윈도우에 등록.
    def show_total_user_list(self):
        try:
            users = self.get_all_user_profiles()
            self.sub_window = shotgrid_total_profile.TotalProfile(users) 
            self.sub_window.show()
        except Exception as e:
            self.show_error_message(f"Error : {e}")

    #전체 사용자 프로필 가져오기.
    def get_all_user_profiles(self):
        fields = ["id", "login", "name", "sg_step", "projects"]
        return self.sg.find("HumanUser", [], fields)
    
    #사용자의 정보를 저장, 전달합니다.
    def save_and_close(self):
        name = self.ui.comboBox_user.currentText()
        project = self.ui.label_project.text()
        task = self.ui.lineEdit_task.text()
        if self.ui.label_shot_asset.text() == "Shot":
            seq = shot.split("_")[0]
            shot = self.ui.comboBox_shot_asset.currentText()
            asset = None
            asset_type = None
        else :
            seq = None
            shot = None
            asset =self.ui.label_shot_asset.text()
            asset_type = self.ui.label_asset_type.text()

        Make_User_Data(name, project, seq, shot, asset, task, asset_type)
        self.close()
        
    #샷그리드가 작동하지 않을경우 새로운 로그인창 연결.
    def open_offline_login_window(self):
        self.login = Login()
        self.login.show()
     
    #에러메시지.
    def show_error_message(self, message):
        QMessageBox.critical(self, "Error", message)


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    win = UserProfile()
    # win.show()
    sys.exit(app.exec())