
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