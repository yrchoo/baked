import json
from datetime import datetime
import os
from fetch_shotgrid_data import ShotGridDataFetcher


class PubDataJsonCreator:
    # ***** 파일 이름은 shotgrid_pub_data_json.py로 바꿔주시고
    # ***** class 이름은 PubDataJsonCreator로 변경해주시면 감사하겠습니당
    # version이랑 pub_file 가져오는 코드는 fetchdata에 있다고 함.
    
    def __init__(self, sg=None): # 여기서 받아오는 값은 publish file과 link될 version에 대한 dictionary 입니다 pub_dict로 변경해주세요
        self.sg = sg
        self.dir = "/home/rapa/baked/toolkit/config/python/shotgrid/unpublished_files/"          #임의 경로 지정
        
        # ***** 이 부분은 Publisher에서 pub이 될 때 shotgrid 연결이 없으면 pub하려던 정보값을 전달해줄 것이기 때문에
        # Publisher를 선언하는 부분은 필요치 않을 것 같아요..!
        # self.previous_data = None


    def save_to_json(self, data):
        """
        pub_data를 JSON파일로 저장합니다. 파일명은 타임스탬프로 저장됩니다. == 메인 태스크1
        """
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(self.dir, f"pub_data_{timestamp}.json")

        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)   


    def upload_all_json_files(self, sg):
        """
        모든 JSON파일을 읽어와서 ShotGrid서버에 업로드하는 메서드입니다. == 메인 태스크 2
        """
        if not os.path.exists(self.dir):
            print("There is no directory")
            return
        
        all_files = os.listdir(self.dir)

        json_files = []
        for file in all_files:
            if file.endswith('.json'):
                json_files.append(file)
                
        for json_file in json_files:
            file_path = os.path.join(self.dir, json_file)
            with open(file_path, "r") as f:
                self.pub_data = json.load(f)

            self.launch_process()

            os.remove(file_path)
            print("Task Complete!")

    def find_project(self):
        """
        pub_data의 project 이름에 대응하는 프로젝트를 찾는 메서드입니다.
        """
        project_code = self.pub_data.get("project", {}).get("name")

        if not project_code:
            raise ValueError("Project code not found")
        
        self.project = self.sg.find_one(
            "Project",
            [["name", "is", project_code]],
            ["id", "name"]
        )

        if not self.project:
            raise ValueError(f"Project '{project_code}' not found") 
        

    def find_user(self):
        """
        pub_data의 HumanUser 이름에 대응하는 사용자를 찾는 메서드입니다.
        """
        user_name = self.pub_data.get("HumanUser", {}).get("name")
        if not user_name:
            raise ValueError("User name not found")
        
        if not self.project:
            raise ValueError("Project not found")

        self.user = self.sg.find_one(
            "HumanUser", 
            [["name", "is", user_name], ["projects", "is", self.project]],
            ["id", "name", "email"]
        )

        if not self.user:
            raise ValueError(f"user '{user_name}' not found")
        
        


    def launch_process(self):
        """
        주어진 작업들을 모두 실행합니다.
        """

        if not self.pub_data:
            raise ValueError("There is no pub_data")
        
        self.find_project()
        self.find_user()

        # version을 생성하고, create_new_version_entity를 구동해줍니다.
        version = self.tool.create_new_version_entity(
            version = self.pub_data["version"]["code"],
            shot_code = self.pub_data["version"]["shot_code"],
            task_name = self.pub_data["version"]["task"],
            description = self.pub_data["version"]["description"],
            thumbnail_file_path = self.pub_data["version"]["thumbnail_file_path"]
        )

        #published_file을 생성하고, create_new_publish_entity를 구동해줍니다.
        published_file = self.tool.create_new_publish_entity(
            version = version,
            shot_code = self.pub_data["version"]["shot_code"],
            file_path = self.pub_data["PublishedFile"]["file_path"],
            description = self.pub_data["PublishedFile"]["description"],
            thumbnail_file_path = self.pub_data["PublishedFile"]["preview_path"],
            published_file_type = self.pub_data["PublishedFile"]["published_file_type"]
        )

        print(f"Version created: {version}")    
        print(f"Published file created: {published_file}")


test_pub_data = {
    "version" : {
        "code" : "v001",
        "task" : "CMP",
        "description" : "test version",
        "thumbnail_file_path" : "/home/rapa/...",
        "shot_code" : "ABC_0010",
        "asset" : None,
    },
    "project" : {
        "name" : "baked"
    },
    "HumanUser" : {
        "name" : "임 호진",
    },
    "PublishedFile" : {
        "name" : "ABC_0010_CMP_v001.nknc",
        "file_path": "/home/rapa/...",
        "description" : "test pub file", 
        "preview_path" : "/home/rapa/...", 
        "published_file_type" : "Comp Script",
    }
}               # 파일 예시 -  추후 제거


