from shotgun_api3 import Shotgun

import os

import re

import pprint

class MakeVersionTest():
    def __init__(self):
        self._set_init_value()
        self._get_auth()
        self._set_entity_data()
        # self._make_new_version_pub_file()
        self._print_data()

    def _set_init_value(self):
        self.sg = "" # Shotgun()
        self.project_data = {
            "name" : "baked"
        }
        self.template = {
            "Shot" : 'Baked Shot Template', "Asset" : 'Baked Character Asset Template'
        }

    def _get_auth(self):
        script_name = "baked"
        script_key = "p)ghhlikzcyzwq4gdgZpnhmkz"

        self.sg = Shotgun("https://4thacademy.shotgrid.autodesk.com/", 
                    script_name, 
                    script_key)
        

    def _set_entity_data(self):
        self.project = self.sg.find_one("Project", [["name", "is", "baked"]], ["id"])

        self.open_folder_path = "/home/rapa/baked/show/baked/SEQ/ABC/ABC_0010/LGT/pub/nuke/images/ABC_0010_LGT_v001/ABC_0010_LGT_v001.####.exr"
        file_name = os.path.basename(self.open_folder_path)
        dir_name = os.path.dirname(self.open_folder_path)

        p = re.compile("[v]\d{3}")
        file_ver = p.search(file_name).group()
        # file_name, file_ext = os.path.splitext(self.open_folder_path)

        self.task = self.sg.find_one("Task", [["content", "is", "LGT"], ["project", "is", self.project]], ["id"])
        self.shot = self.sg.find_one("Shot", [["code", "is", "ABC_0010"], ["project", "is", self.project]], ["id"])

        new_version_data = {
            "project" : self.project,
            "code": file_ver,
            "description": "tracker test를 위해 생성한 version입니당",
            "entity" : self.shot,
            "sg_task": self.task,
            # "user": self.sg.find_one("HumanUser", [["login", "is", "추예린"]], ["id"]),
        }

    def _make_new_version_pub_file(self):

        version = self.sg.create("Version", new_version_data)
        print(f"version : {version}")


        published_file = {
            "project": self.project,
            "code": file_name,
            "description": "Description of the published file",
            "task": self.task,
            "entity" : self.shot,
            "version": {"type": "Version", "id": version["id"]},  # 버전과 연결
            "path": {"local_path": self.open_folder_path},
            # "published_file_type": {"type": "PublishedFileType", "id": 2},  # 필요에 따라 유형 ID를 조정
        }

        publish = self.sg.create("PublishedFile", published_file)
        print(f"publish : {publish}")
        
    def _print_data(self):
        print('-' * 50)
        filters = [
            ["project", "is", self.project],
            ["task", "is", self.task],
            ["entity", "is", self.shot]
        ]
        fields = ["id", "code", "path", "task", "version"]

        last_file = self.sg.find_one("PublishedFile", filters, fields, order=[{'field_name': 'created_at', 'direction': 'desc'}])
        pprint.pprint(last_file)


if __name__ == "__main__":
    MakeVersionTest()