
from PySide6.QtWidgets import QApplication, QWidget, QTableWidgetItem
from ui_files.ui_Shotgrid_total_profile import Ui_Form

import sys
from shotgun_api3 import shotgun

class TotalProfile(QWidget):
    def __init__(self, datas, parent = None):
        super().__init__(parent)

        #메인윈도우에서 전달받은 전체사용자 프로필정보
        self.datas = datas
        self.parent_widget = parent
        self.setup_ui()

        self.sg = self.connect_sg()
        self.get_total_user_profile()
        self.insert_user_profile()

        #Baked project Id
        self.project_id = 155

        self.task_mapping = {}
        self.load_tasks_shots_assets()

        self.ui.comboBox_task.currentIndexChanged.connect(self.insert_task_name_changed)
        self.ui.comboBox_shot.currentIndexChanged.connect(self.insert_shot_id_changed)
        self.ui.comboBox_asset.currentIndexChanged.connect(self.insert_asset_id_changed)
        
        self.selected_task_id = None
        self.selected_shot_id = None
        self.selected_asset_id = None

        self.ui.pushButton_insert.clicked.connect(self.assign_selected_items_to_user)
        self.table.cellClicked.connect(self.select_user_name)
        self.table.cellClicked.connect(self.add_selected_user_profile)
       
    def connect_sg(self):

        URL = "https://4thacademy.shotgrid.autodesk.com"
        script_name =  "baked"
        script_key =  "p)ghhlikzcyzwq4gdgZpnhmkz"
        self.sg = shotgun.Shotgun(URL,script_name,script_key)
        return self.sg
    
    #메인윈도우에서 전달받은 전체사용자 프로필정보 리스트로 저장.
    def get_total_user_profile(self):
        total_data = []
        for data in self.datas:
            name = ""
            user_id = ""
            email = ""
            project_names = ""
            role = ""
            if "name" in data:
                name = data["name"]
            if "id" in data:
                user_id = str(data["id"])
            if "login" in data:
                email = data["login"]
            else:
                email = ""
            if "projects" in data:
                project_list = []
                for project in data["projects"]:
                    project_list.append(project["name"])
                project_names = ', '.join(project_list)
            else:
                project_names = ""
            if "sg_role" in data:
                role = data["sg_role"]
            else:
                role = ""
            total_data.append([name, user_id, email, project_names, role])
        return total_data
    
    #전체 사용자 프로필 목록 테이블위젯에 입력.
    def insert_user_profile(self):
        total_data = self.get_total_user_profile()
        for row, data in enumerate(total_data):
            for col, value in enumerate(data):
                self.table.setItem(row, col, QTableWidgetItem(value))
        self.table.resizeColumnsToContents()  
            

    #프로젝트에 등록할 새로운 사용자 선택.
    def select_user_name(self,row):
        name_item  = self.table.item(row,0)
        name = name_item.text()
        self.ui.lineEdit_name.setText(name)

    #프로젝트에 등록할 새로운 사용자 정보 조회.
    def add_selected_user_profile(self):
        col_data = []
        fields = ["name", "id", "login","projects,", "sg_role"] 
        for row in range(self.table.rowCount()):
            item = self.table.item(row,0)
            if item and item.text() == self.ui.lineEdit_name.text():
                for col in range(self.table.columnCount()):
                    data = self.table.item(row,col)
                    col_data.append(data.text())
        if col_data:
            user_dict = {key : value for key,value in zip(fields,col_data)}
            return user_dict
        
    #프로젝트 아이디로 task,shot,asset 데이터들을 불러온다.
    def load_tasks_shots_assets(self):

        tasks = self.sg.find("Task", [["project", "is", {"type": "Project", "id": self.project_id}]], ["id", "content", "entity"])
        shots = self.sg.find("Shot", [["project", "is", {"type": "Project", "id": self.project_id}]], ["id", "code"])
        assets = self.sg.find("Asset", [["project", "is", {"type": "Project", "id": self.project_id}]], ["id", "code"])

        unique_tasks = {}

        # Task ID와 연결된 Shot, Asset ID 매칭.
        for task in tasks:
            task_name = task["content"]
            task_id = task["id"]
            entity_type = task["entity"]["type"]
            entity_id = task["entity"]["id"]
            
            if task_name not in unique_tasks:
                unique_tasks[task_name] = []
            unique_tasks[task_name].append({
                "task_id": task_id,
                "entity_type": entity_type,
                "entity_id": entity_id
            })

        self.task_mapping = unique_tasks

        #콤보박스에 task content와 shot,asset id 에 맞게 데이터 입력.
        self.ui.comboBox_task.clear()
        self.ui.comboBox_task.addItem("", None)  
        for task_name in unique_tasks.keys():
            self.ui.comboBox_task.addItem(task_name, task_name)

        self.ui.comboBox_shot.clear()
        self.ui.comboBox_shot.addItem("", None)  
        for shot in shots:
            self.ui.comboBox_shot.addItem(shot["code"], shot["id"])

        self.ui.comboBox_asset.clear()
        self.ui.comboBox_asset.addItem("", None)  
        for asset in assets:
            self.ui.comboBox_asset.addItem(asset["code"], asset["id"])


    #콤보박스에서 내가 원하는 사용자에게 assign 할 데이터를 선택.
    def insert_task_name_changed(self, index):
        self.selected_task_name = self.ui.comboBox_task.itemData(index)
        print(f"Task : {self.selected_task_name}")  

    def insert_shot_id_changed(self, index):
        self.selected_shot_id = self.ui.comboBox_shot.itemData(index)
        print(f"Shot : {self.selected_shot_id}")  

    def insert_asset_id_changed(self, index):
        self.selected_asset_id = self.ui.comboBox_asset.itemData(index)
        print(f"Asset : {self.selected_asset_id}")  


    # 기존에 존재하던 사용자 찾기
    def get_user_id_from_name(self, name):

        filters = [["name", "is", name]]
        fields = ["id"]
        user = self.sg.find_one("HumanUser", filters, fields)
        if user:
            return user["id"]
        else:
            print(f"해당이름의 사용자가 없습니다 : {name}")
            return None

    #기존에 존재하던 사용자에 겹치지 않게 추가로 프로젝트에 새로운 사용자 업데이트
    def assign_selected_items_to_user(self):
        user_name = self.ui.lineEdit_name.text()
        user_id = self.get_user_id_from_name(user_name)
        if not user_id:
            print("사용자가 없습니다.")
            return
        if not self.selected_task_name:
            print("Task 가 없습니다.")
            return

        # 선택된 Task와 매칭되는 Shot,Asset 찾기
        matching_task = None
        for task_info in self.task_mapping[self.selected_task_name]:
            if self.selected_shot_id and task_info["entity_type"] == "Shot" and task_info["entity_id"] == self.selected_shot_id:
                matching_task = task_info
                break
            elif self.selected_asset_id and task_info["entity_type"] == "Asset" and task_info["entity_id"] == self.selected_asset_id:
                matching_task = task_info
                break

        if matching_task:
            task_id = matching_task["task_id"]

            #Task에 기존의 할당된 사용자 목록 가져오기
            task_data = self.sg.find_one("Task", [["id", "is", task_id]], ["task_assignees"])
            current_assignees = task_data.get("task_assignees", [])

            # 사용자 ID를 중복 없이 추가
            if not any(assignee["id"] == user_id for assignee in current_assignees):
                current_assignees.append({"type": "HumanUser", "id": user_id})

                # Task에 사용자를 할당
                self.sg.update("Task", task_id, {"task_assignees": current_assignees})
                print(f"User ID : {user_id}, Task ID : {task_id}")

            # Task에 Shot , Asset 연결
            entity_id = matching_task["entity_id"]
            entity_type = matching_task["entity_type"]
            
            #새로운 사용자의 데이터가 존재할경우 프로젝트에 추가 업데이트.
            if entity_id and entity_type:
                self.sg.update("Task", task_id, {"entity": {"type": entity_type, "id": entity_id}})
                print(f"Task ID : {task_id} with {entity_type} ID {entity_id}")
            else:
                print("")
        else:
            print("error")


    def setup_ui(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.table = self.ui.tableWidget
        self.table.setRowCount(25) 
        self.table.setColumnCount(5)  
       
        self.table.setHorizontalHeaderLabels(["name", "id", "email", "project","Role"])
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

if __name__ == "__main__":

    app = QApplication(sys.argv) 
    datas = []
    win = TotalProfile(datas)
    win.show()  
    app.exec()
        


