import os
import requests
from shotgun_api3 import Shotgun
import pickle

from datetime import datetime

import time

try :
    from get_user_data import Get_User_Data
    from make_project_dir import FolderStructureCreator
    from new_version_occur_watchdog import VersionUpdateObserver
except :
    from shotgrid.get_user_data import Get_User_Data
    from shotgrid.make_project_dir import FolderStructureCreator
    from shotgrid.new_version_occur_watchdog import VersionUpdateObserver



"""
*****
본 파일은 login이 되고 나서의 정보를 가지고
shotgrid 데이터 서버에 존재하는 정보들을 가져오는 메서드를 담은 모듈입니다
이 클래스를 모든 프로그램에서 공통적으로 사용할 것이기 때문에... 꼼꼼하게 작성해주세요
제가 이것저것 추가하고 수정할 부분을 적어두었습니다 ㅎ

프로젝트에 사용되는 모든 Shotgun API를 사용하는 코드가 꽤나 반복적이기 때문에
이 곳에 있는 메서드를 호출하여 사용해주시면 좋을 것 같아요
개인적으로 필요한 메서드가 있다면 아래에 추가해주시면 되는데
어느정도 재사용을 하는 경우를 염두하고 작성해주세요 :)

각 메서드가 어떤 기능인지 현재 작성되는 주석과 같은 방식으로 달아주세요!
"""

class ShotGridDataFetcher(): 
    
######################### Singleton #######################
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ShotGridDataFetcher, cls).__new__(cls)
            print("New shotgrid_file_fetcher created...")
        else:
            print("Load shotgrid_file_fetcher...")
        return cls._instance
###########################################################
    
    def __init__(self): # ***** 바꿈
        self._set_instance_val()
        self.sg = self._get_auth()
        if self.connected:
            self._fetch_project_id()
            FolderStructureCreator(self, "/home/rapa/baked/show/baked/") # 이건 나중에 yaml에 저장된 경로로 바꿔주세요!
            self.observer = VersionUpdateObserver("/home/rapa/baked/toolkit/config/python/shotgrid/new_data_json/")
        self._get_current_user_data()

    def _set_instance_val(self):
        """
        *****
        class 전체에서 사용될 self.val들을 모아두는 곳
        기본적으로 해당 변수에 어떤 값이 들어갈 건지 주석과 함께 달아주시면 좋습니다
        """
        self.sg = None # Shotgun() 객체가 저장되는 곳
        self.connected = False # Shotgun API가 잘 연결되었는지 값을 저장해줍니다

        # project나 현재 작업을 하고 있는 HumanUser entity들은 자주 사용되고 전체 프로젝트가 돌아가는 동안 변경되지 않으니
        # instance 변수에 저장해두는 것이 좋을 것 같습니다
        self.project = None # 현재 진행하고 있는 프로젝트의 기본적인 entity가 저장되는 곳
        self.user = None # 현재 작업을 하고 있는 HumanUser entity
        self.work = None # 현재 작업 shot, asset의 entity가 들어가는 곳
        self.task = None # 현재 작업 task의 entity가 들어가는 곳
        self.frame_start = None # 현재 작업에 프레임이 정해져있다면 시작 프레임 값이 저장되는 변수
        self.frame_last = None # 현재 작업에 프레임이 정해져있다면 마지막 프레임 값이 저장되는 변수
        self.height = None
        self.width = None
        self.undistortion_height = None
        self.undistortion_width = None


    def _get_auth(self):
        # shotgrid 서버에서 권한을 허가받는 script정보가 매개변수로 들어가는 건 뭔가.. 옳지 않은 것 같아요... *****
        # 이 데이터를 ~/.bashrc에 넣어서 불러와서 사용하도록 하는 걸로.. 바꾸면 안정적일 것 같습니다
        # 환경변수에 스크립트 데이터를 저장해두고 가져오면 모두가 이 스크립트로 작업하고
        # 스크립트 이름이 프로젝트 이름이라서 모든 곳에서 디폴트로 읽어와서 프로그램을 실행할 수 있을 것 같아요(좋은 방법인지는 선생님께.. 여쭤보기)
        shotgun_url = "https://4thacademy.shotgrid.autodesk.com/"
        script_name = "baked"
        script_key = "p)ghhlikzcyzwq4gdgZpnhmkz"

        try :
            # Shotgun 서버에 연결할 수 없다면 오류가 발생합니다
            sg = Shotgun(shotgun_url, 
                        script_name, 
                        script_key)
            self.connected = True
        except:
            sg = None
            self.connected = None

        return sg
    
    def _get_current_user_data(self):
        self.user_info = Get_User_Data().return_data() # 해당 클래스 메서드는 환경변수에 등록한 유저의 정보를 dictionary로 가져옵니다 *****
        """
        여기에 나중에 self.user_info dict 출력한 것 붙여두겠습니다
        """
        if self.connected:
            self.user = self.sg.find_one("HumanUser", [['name','is',self.user_info['name']], ['projects','is',self.project]], ['name', 'id']) # user의 entity를 가져오는 뭔가를 작성해야될듯요
            if self.user_info['asset']:
                self.work = self.get_asset_entity(self.user_info['asset'])
            elif self.user_info['shot']:
                self.work = self.get_shot_from_code(self.user_info['shot'])
                self.frame_start = self.work['sg_cut_in']
                self.frame_last = self.work['sg_cut_out']
                self.undistortion_height = self.work['sg_undistortion_height']
                self.undistortion_width = self.work['sg_undistortion_width']
                self.width = self.project['sg_resolutin_width']
                self.height = self.project['sg_resolution_height']
                self.task = self.get_task_from_ent(self.work)
                print(self.frame_start, self.frame_last, self.undistortion_height, self.undistortion_width, self.width, self.height)

    # 프로젝트 id 를 가져와서 지정해준다.
    def _fetch_project_id(self): # ***** 내부에서만 사용되는 메서드는 이름 앞에 _언더바를 붙여서 표시해주시면 좋아요
        """
        ***** 메서드 주석은 이렇게 달아주세요
        프로젝트 엔티티를 instance value에 넣어준다
        """
        project_name = 'baked'  # 나중에 self.user_info['project']로 변경
        filters = [['name', 'is', project_name]]
        fields = ['id', 'name', 'sg_resolutin_width', 'sg_resolution_height']
        project = self.sg.find_one('Project', filters, fields) # 프로젝트는 중복되는 값이 존재할 수 없기 때문에 find_one으로 수정 *****

        if not project:
            print("프로젝트를 찾을 수 없습니다.")
        else:
            # project_id = project[0]['id']
            # print(f"프로젝트 ID : {project_id}")
            print(f"Project : {project}")
        self.project = project

    """
    몇몇 메서드의 이름을... 바꾸었습니다...
    뭔가 명확하게 어디서 어떻게 무엇을 return하는지가 적혀있으면 좋겠어영
    """

    # 에셋을 읽어온다. 
    def fetch_assets(self, fields=[]): # ***** 현재 main으로 작업중인 프로젝트 외에는 접근할 일이 없으니 project_id가 매개변수인 것은 불필요 할 것 같아용
        filters = [["project", "is", self.project]] # ***** project entity를 self.project에 저장했으니 해당 값으로 대체 가능
        fields = ["code", "id", "sg_asset_type"] # ***** 저는 or 문장이 오류가 나서... 추가적으로 필요한 필드가 있다면 그냥 extend 해주심이..
        assets = self.sg.find("Asset", filters, fields)
        return assets
    

    # 에셋에 연결된 태스크를 읽어온다.
    def fetch_tasks_from_all_asset(self, assets):
        # ***** 이런 코드는 모든 asset에 연결된 모든 task를 다.. 가져오기 때문에 재사용성이 너무 떨어져요..
        # 하나의 asset에 연결된 task들을 구하는 메서드를 하나 짜서 모든 asset마다 해당 함수를 돌리는 게.. 좋을 것 같아요
        # 그러면 하나의 asset에 대한 데이터를 구할 때에도 여러 asset의 데이터를 구할때에도 둘다 호출해서 쓸 수 있음
        all_asset_tasks = []
        for asset in assets:
            asset_tasks = self.fetch_tasks_for_asset(asset)
            all_asset_tasks.extend(asset_tasks)
        return all_asset_tasks
    
    ################################################
    # ***** 사실... task의 entity를 구할때에는 링크된 entity가 shot이든 asset이든 구분없이 "entity"필드에 들어가기 때문에...
    # 하나의 메서드를 통해서 두 경우가 모두... 구해질 수 있다는 사실... 대박..이죠?!
    def fetch_tasks_from_linked_entity(self, entity): # ***** 재사용성이 좋은.. 코드의 예시입니다.. 하지만 주관적...
        filters = [["entity", "is", entity]]
        fields = ["content", "entity"]
        tasks = self.sg.find("Task", filters, fields)
        return tasks
    
    def fetch_cur_task_by_taskname_linkedentity(self, task_name, entity):
        filters = [['entity', 'is', entity], ['content', 'is', task_name]]
        fields = ['id', 'content', 'entity', 'sg_task']
        task = self.sg.find_one("Task", filters, fields)
        return task
    ################################################


    # 시퀀스를 읽어온다.
    def fetch_seq(self, fields=[]):
        filters = [["project", "is", self.project]] # ***** 이 부분도 지금 프로젝트에 존재하는 seq들을 가져오는 것이기 때문에 self.project로 바꿨습니다
        fields = ["code", "id"] # ***** fetch_assets와 동일한 이슈
        seqs = self.sg.find("Sequence", filters, fields)
        return seqs
        

    # # 샷들을 읽어온다.
    # def fetch_shots(self, seqs):
    #     self.all_shots = []
    #     for seq in seqs:
    #         filters = [["sg_sequence", "is", seq]]
    #         fields = ["code", "id", "sg_sequence"]
    #         seq_shots = self.sg.find("Shot", filters, fields)
    #         self.all_shots.extend(seq_shots)
    #     return self.all_shots # return으로 뽑아낼 값이라면... self를 지양합시다!
    
    #################################################
    # ***** 샷도 마찬가지로 프로젝트에 존재하는 모든 샷을 구해오기 보단...
    # 하나의 시퀀스에 존재하는 샷들을 가져오는 코드를 작성하고 그 코드를 for문을 돌리는 것이... 좋은 것 같아요...
    def fetch_shot_from_seq(self, seq):
        filters = [["sg_sequence", "is", seq]]
        fields = ["code", "id", "sg_sequence"]
        shots = self.sg.find("Shot", filters, fields)
        return shots
    #################################################

    # 시퀀스 - 샷에 연결된 태스크들을 읽어온다.
    def fetch_seq_tasks(self, seq): # ***** 메서드 이름이 이상따리해요 해당 함수도 fetch_task_from_linked_entity로 해결할 수 있을 것 같아요
        shots = self.fetch_shot_from_seq(seq)
        all_seq_tasks = []
        for shot in shots:
            seq_tasks = self.fetch_tasks_from_linked_entity(shot)
            all_seq_tasks.extend(seq_tasks)
        
        return all_seq_tasks # 이 정보가 왜.. 필요한지 이해가 안됩니다..! 설명 부탁드려요
    

    #####################################################################################
    #
    # 이 아래에는 Loader와 연결을 위해 Loader에서 필요한 shotgrid api 기능들을 메서드로 작성한 것입니다
    #
    #####################################################################################
    # 일단 다른 곳에 작성했던 코드를 긁어만 왔고... 위에 있는 메서드랑 중복되는 건 loader에서 이름 수정 후 아래 메서드는 지우겠습니다

    def get_sequences_entities(self) -> list[dict]:
        filters_for_seq = [['project', 'is', self.project]]
        fields_for_seq = ['type', 'id', 'code']
        result = self.sg.find("Sequence", filters_for_seq, fields_for_seq)
        return result
    
    def get_asset_entities(self) -> list[dict]:
        filters_for_seq = [['project', 'is', self.project]]
        fields_for_seq = ['type', 'id', 'code', 'sg_asset_type']
        result = self.sg.find("Asset", filters_for_seq, fields_for_seq)
        return result

    def get_shot_from_seq(self, seq_ent) -> list[dict]:
        filters_for_shot = [['sg_sequence', 'is', seq_ent]]
        fields_for_shot = ['type', 'id', 'code']
        shots = self.sg.find("Shot", filters_for_shot, fields_for_shot)
        return shots
    
    def get_task_from_ent(self, ent) -> list[dict]:
        if not ent :
            return []
        filters_for_task = [['entity', 'is', ent]]
        fields_for_task = ['type', 'id', 'content']
        tasks = self.sg.find("Task", filters_for_task, fields_for_task)
        return tasks
    
    def get_seq_from_shot(self, shot) -> dict:
        filters_for_seq = [['shots', 'is', shot]]
        fields_for_seq = ['type','id', 'code']
        seq = self.sg.find_one("Sequence", filters_for_seq, fields_for_seq)
        return seq

    def get_assigned_task(self, name=None) -> list[dict]:
        if name == None:
            name = self.user_info["name"]
        filters_for_humanuser = [['name', 'is', name]]
        user = self.sg.find_one("HumanUser", filters_for_humanuser)
        filters_for_task = [['task_assignees', 'is', user]]
        fields_for_task = ['content', 'entity', 'task_assignees']
        tasks = self.sg.find("Task", filters_for_task, fields_for_task)
        entity_list = []
        for task in tasks:
            # print(task)
            entity_list.append(task['entity'])
        return entity_list
    
    def get_asset_entity(self, asset_name) -> dict:
        filter_for_asset = [['code', 'is', asset_name]]
        fields_for_asset = ['id', 'sg_asset_type', 'code']
        asset = self.sg.find_one("Asset", filter_for_asset, fields_for_asset)
        return asset
    
    def get_shot_from_code(self, shot_code = None) -> dict:
        if not shot_code :
            shot_code = self.user_info["shot"]
        if not shot_code : return None
        filter_for_shot = [['code', 'is', shot_code]]
        fields_for_shot = ['sg_cut_in', 'sg_cut_out', 'sg_undistortion_height', 'sg_undistortion_width']
        shot = self.sg.find_one("Shot", filter_for_shot, fields_for_shot)
        return shot


    def get_assets_used_at_shot(self, shot_code = None)-> list[dict]:
        shot = self.get_shot_from_code(shot_code)
        filters_for_asset = [['shots', 'is', shot]]
        fields_for_asset = ['id', 'sg_asset_type', 'code']
        assets = self.sg.find("Asset", filters_for_asset, fields_for_asset)
        return assets
    
    ##################################################
    # publish 작업에서 필요한 메서드
    ##################################################
    def create_new_version_entity(self, version, task_name, description, thumbnail_file_path, shot_code=None, asset =None):
        if asset:
            link = self.get_asset_entity(asset)
        if shot_code:
            link = self.get_shot_from_code(shot_code)
        task = self.fetch_cur_task_by_taskname_linkedentity(task_name, link)

        version_ent = self.sg.find_one("Version", 
                                   [['project','is',self.project], ['code','is',version],['sg_task','is',task], ['entity','is',link]],
                                   ['project','code','description','entity','sg_task','created_by','sg_status_list'])
        
        print (self.project, task, link, shot_code)
        if version_ent:
            print("version already exists")
            return version_ent
        
        new_version_data = {
            "project" : self.project,
            "code": version, # 'v001'
            "description": description,
            "entity" : link,
            "sg_task": task,
            "created_by" : self.user,
            "sg_status_list" : "rev",
            "user" : self.user
        }

        print (new_version_data)
        version = self.sg.create("Version", new_version_data)
        self.sg.upload("Version", version['id'], thumbnail_file_path, field_name="sg_uploaded_movie")

        return version
    
    def update_version_for_review(self, version, task_name, review_movie_path, description, shot_code=None, asset =None):

        version_ent = self.create_new_version_entity(version, task_name, review_movie_path, description, shot_code, asset)
        
        data = {
                "description": description,
                }

        # ShotGrid에서 Version 엔터티 업데이트
        self.sg.upload("Version", version_ent['id'], review_movie_path, field_name="sg_uploaded_movie")
        self.sg.update("Version", version_ent["id"], data)



    def create_new_publish_entity(self, version, file_path, description, thumbnail_file_path, published_file_type):
        file_name = os.path.basename(file_path)
        published_file_type = self.sg.find_one("PublishedFileType", [['code', 'is', published_file_type]], ['id', 'name'])
        published_file = {
            "project": self.project,
            "code": file_name,
            "description": description,
            "task": version['sg_task'],
            "entity" : version['entity'],
            "version": version,  # 버전과 연결
            "path": {"local_path": file_path},
            "published_file_type": published_file_type,
            "created_by" : self.user
        }

        publish = self.sg.create("PublishedFile", published_file)
        self.sg.upload_thumbnail("PublishedFile", publish['id'], thumbnail_file_path)
        print(f"publish : {publish}")
        # self.send_data_to_webhook_server(version)

    def send_data_to_webhook_server(self, data:dict):
        url = ""

        header = {
            "accept": "application/json",
            "user-agent": "SG event-pipeline",
            "content-type": "application/json; charset=utf-8",
            "x-sg-webhook-id": "9441c2f0-3ed9-45cb-a1e0-9b6a5a5ae3db",
            "x-sg-event-batch-id": "49652721640407050916129894443709552046784423781841502850",
            "x-sg-event-batch-size": "1",
            "x-sg-webhook-site-url": "https://4thacademy.shotgrid.autodesk.com/"
            }
        try:
            response = requests.post(url, json=data, headers=header)
        except:
            print("Webhook Server Data sending failed")


    def add_new_version_to_playlist(self, version):
        playlist_code = datetime.today().strftime("%Y-%M-%d") # '2024-08-30'
        playlist = self.sg.find_one('Playlist', [['code', 'is', playlist_code]], ['versions'])
        if playlist:
            versions = playlist['versions']
            versions.append(version)
        else :
            playlist_data = {
                'project' : self.project,
                'code' : playlist_code,
            }
            playlist = self.sg.create("Playlist", playlist_data)
            versions = [version]
        
        self.sg.update('Playlist', playlist, { 'versions': versions })


if __name__ == "__main__":
    while True:
        time.sleep(5)

