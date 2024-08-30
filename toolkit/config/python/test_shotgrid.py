
from shotgun_api3 import shotgun
file_info = {'Apple_MOD_v001.mb': {'pub': True, 'rev': True, 'description': 'tesing', 'file type': 'Model Geo', 'ext': 'None', 'path': '/home/rapa/show/baked/AST/Character/Apple/MOD/pub/maya/scenes/Apple_MOD_v001.mb'},
             'potato_cache_grp':{'pub': True, 'rev': True, 'description': 'sleeping', 'file type': 'Model Cache', 'ext': 'None', 'path': '/home/rapa/show/baked/AST/Character/Apple/MOD/pub/maya/data/alembic/Apple_MOD_potato_v001.mb'}}

class TestShotgrid():
    def __init__(self):
        self.file_info = {'Apple_MOD_v001.mb': {'pub': True, 'rev': True, 'description': 'tesing', 'file type': 'Model Geo', 'ext': 'None', 'path': '/home/rapa/show/baked/AST/Character/Apple/MOD/pub/maya/scenes/Apple_MOD_v001.mb'},
             'potato_cache_grp':{'pub': True, 'rev': True, 'description': 'tesing', 'file type': 'Model Cache', 'ext': 'None', 'path': '/home/rapa/show/baked/AST/Character/Apple/MOD/pub/maya/data/alembic/Apple_MOD_potato_v001.mb'}}
        for file in self.file_info:
            self._create_published_file(file)

    def _connect_sg(self):
        """샷그리드 연결시키는 메서드"""
        URL = "https://4thacademy.shotgrid.autodesk.com"
        SCRIPT_NAME = "pipeline key"
        API_KEY = "^axlq0daadimnwnatxrdoYfsm"
        sg = shotgun.Shotgun(URL,
                            SCRIPT_NAME,
                            API_KEY)
        return sg
    
    def upload_to_shotgrid(self):
        for file in self.file_info:
            self._create_published_file(file)

    def _create_published_file(self, file):
        """ (4) 샷그리드 published_file 에 pub 파일들 올리는 메서드 """
        sg = self._connect_sg()
        description = self.file_info[file]['description']
        path = self.file_info[file]['path']
        published_file_type = self.file_info[file]['file type']

        # pub_path = # pub 저장하고 나온 데이터로
        published_file_data = {'project': {'type':'Project', 'id':155},
                               'code': file,   # 이름 (추후 입력되는 데이터를 받아오는걸로 수정가능)
                               'sg_status_list': 'ip', # 상태 (추후 수정가능)
                               'description': description,
                               'entity': {'type':'Asset', 'id':1450},
                               'task': {'type':'Task', 'id':5930},
                               'version': {v001',
                               'path': path,
                               'created_by': 'Seoyeon Yoon',
                               'published_file_type' : published_file_type}
        result = sg.create('PublishedFile', published_file_data)
        print ("Well Done")
        return result

    def _create_version(self):
        """ (5) 샷그리드 versions에 오리는 메서드 """
        print (f"REVIEW     /// {self.publish_dict}")
        published_file_dict, review_file_dict = self._separate_pub_review()
        if not review_file_dict:
            return
        
        task = self.ui.comboBox_task.currentText()
        link = self.ui.comboBox_link.currentText()
        name = self.user_file_info['name']
        description = self.publish_dict['description']
        version = self.user_file_info['version']
        project = self.user_file_info['project']
        preview_path = self.preview_info['output_path']

        # 여기 버전은 옛날 버전인데..
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
                        'sg_upload_movie': preview_path,
                        'published_files': "pub된 경우",
                        'description': description,
                        'published_files' : pub_path,
                        'image': preview_path}
        
        version = self.sg.create('Version', version_data)
        self.sg.upload_thumbnail("Version", version['id'], thumbnail_path)
        return version
    

TestShotgrid()

from shotgun_api3 import Shotgun

import os

import re

import requests
url = "https://5370-1-11-90-40.ngrok-free.app/webhook"

import pprint

class MakeVersionTest():
    def __init__(self):
        self._set_init_value()
        self._get_auth()
        self._set_entity_data()
        self._make_new_version_pub_file()
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
        self.user = self.sg.find_one("HumanUser", [["name", "is", "추예린"]], ["id", "name"])

    def _make_new_version_pub_file(self):

        file_name = os.path.basename(self.open_folder_path)

        new_version_data = {
            "project" : self.project,
            "code": "v010",
            "description": "tracker test를 위해 생성한 version입니당",
            "entity" : self.shot,
            "sg_task": self.task,
            "user": self.user,
            "created_by" : self.user,
            "sg_status_list" : "rev",
            # "upload_file" : "review.mov"
        }

        version = self.sg.create("Version", new_version_data)
        print(f"version : {version}")# POST

        header = {
            "accept": "application/json",
            "user-agent": "SG event-pipeline",
            "content-type": "application/json; charset=utf-8",
            "x-sg-webhook-id": "9441c2f0-3ed9-45cb-a1e0-9b6a5a5ae3db",
            "x-sg-event-batch-id": "49652721640407050916129894443709552046784423781841502850",
            "x-sg-event-batch-size": "1",
            "x-sg-webhook-site-url": "https://4thacademy.shotgrid.autodesk.com/"
            }

        response = requests.post(url, json=version, headers=header)
        
        # response = requests.get(url)
        # print(response) # <Response [200]>
        # response.json()
        # print(response)

        # event_data = {
        #     'event_type': 'Shotgun_Version_New',
        #     'description': f"Version {version['code']} created by script",
        #     'entity': {'type': 'Version', 'id': version['id']},
        #     'project': self.project,
        #     'user' : self.user,
        #     'meta': {
        #         'new_value': version['code'],
        #         'entity_type': 'Version'
        #     },
        # }

        # event = self.sg.create('EventLogEntry', event_data)
        # print(f"Created Event: {event}")


        published_file = {
            "project": self.project,
            "code": file_name,
            "description": "Description of the published file",
            "task": self.task,
            "entity" : self.shot,
            "version": version,  # 버전과 연결
            "path": {"local_path": self.open_folder_path},
            # "published_file_type": {"type": "PublishedFileType", "id": 2},  # 필요에 따라 유형 ID를 조정
        }

        # publish = self.sg.create("PublishedFile", published_file)
        # print(f"publish : {publish}")

        # note_data = {
        #     "project": self.project,
        #     "note_links": [self.project, version],  # 노트를 생성할 버전과 연결
        #     "subject": f"New Version Created",  # 노트 제목
        #     "content": f"{self.user['name']} create new {version['code']} of {published_file['code']}",  # 노트 내용
        #     # "sg_note_type": "Internal",  # 노트 타입 (필요시)
        #     "user": self.user,  # 노트 작성자
        #     "created_by" : self.user,
        #     "tasks": [self.task],  # 태스크와 연결
        #     "addressings_to" : [self.user],
        # }
        # note = self.sg.create("Note", note_data)
        # print("Create Note : " + note['id'])
        
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