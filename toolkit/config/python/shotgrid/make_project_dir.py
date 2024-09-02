import os
from shotgun_api3 import Shotgun
# from fetch_shotgrid_data import ShotGridDataFetcher

class FolderStructureCreator:
    def __init__(self, fetcher, base_path): # ***** shotgridDataFetcher가 선언될 때 현재 작업물이 저장될 경로들을 체크하는 게 좋을 것 같아서
                                   # shotgridDataFetcher에서 FolderStructureCreator를 호출하고 fetcher 객체를 넘겨주는 걸로 수정했습니다
        self.base_path = base_path
        self.fetcher = fetcher
        self.project_id = self.fetcher.project['id'] # ***** 수정했습니다

        self.create_project_folder()

    # ***** 프로젝트 이름으로 된 폴더부터 만들어야됩니다! 수정 부탁드려욥
    # 폴더가 존재하는 지를 확인하고 파일을 만드는 과정이 각 메서드에서 반복되는데 
    # 이 부분을 또 하나의 메서드로 빼두면 나중에 폴더 안만들고 테스트만 해보거나 할 때 유용할 것 같아요

    def create_project_folder(self):
        """프로젝트 폴더를 생성하는 메서드입니다."""
        self.check_folder_exists_or_create(self.base_path)
        self.create_asset_folders()
        self.create_sequence_folders()


    def generate_asset_path(self, asset_type, asset_code, task_content=''):
        """에셋 폴더 경로를 생성하는 메서드입니다."""
        return os.path.join(self.base_path, "AST", asset_type, asset_code, task_content)

    

    def generate_sequence_path(self, seq_code, shot_code='', task_content=''):
        """시퀀스 폴더 경로를 생성하는 메서드입니다."""
        return os.path.join(self.base_path, "SEQ", seq_code, shot_code, task_content)

    

    def check_folder_exists_or_create(self, path):
        """폴더가 존재하는지 확인하고 존재여부에 따라 폴더를 생성합니다."""
        if not os.path.exists(path):
            os.makedirs(path)
            print (f"Folder Created: {path}")
        else:
            pass
            # print (f"Folder Already Exists: {path}")


    def create_subfolders(self, base_path, subfolders):
        """dev, pub과 같은 하위 폴더들을 생성하는 메서드입니다."""
        for subfolder in subfolders:
            subfolder_path = os.path.join(base_path, subfolder)
            # print (subfolder_path)
            self.check_folder_exists_or_create(subfolder_path)


    def process_tasks(self, base_path, tasks):
        """메서드를 호출해 폴더를 만들어주는 메서드입니다."""
        for task in tasks:
            task_path = os.path.join(base_path, task['content'])
            self.check_folder_exists_or_create(task_path)
            self.create_subfolders(task_path, ['dev', 'pub'])

    

    def create_asset_folders(self):
        """에셋 폴더를 생성하는 메서드입니다"""
        assets = self.fetcher.fetch_assets()
        for asset in assets:
            asset_type = asset['sg_asset_type']
            asset_code = asset['code']  
            base_asset_path = self.generate_asset_path(asset_type, asset_code)
            self.check_folder_exists_or_create(base_asset_path)
            
            tasks = self.fetcher.fetch_tasks_from_linked_entity(asset)
            self.process_tasks(base_asset_path, tasks)
            

    def create_sequence_folders(self):
        """시퀀스 폴더를 생성하는 메서드입니다"""
        seqs = self.fetcher.fetch_seq()
        for seq in seqs:
            seq_code = seq['code']  
            base_seq_path = self.generate_sequence_path(seq_code)
            self.check_folder_exists_or_create(base_seq_path)

            shots = self.fetcher.fetch_shot_from_seq(seq)
            for shot in shots:
                shot_code = shot['code']    
                base_shot_path = self.generate_sequence_path(seq_code, shot_code)
                self.check_folder_exists_or_create(base_shot_path)

                tasks = self.fetcher.fetch_tasks_from_linked_entity(shot)
                self.process_tasks(base_shot_path, tasks)




if __name__ == "__main__":

    

    SCRIPT_NAME = "baked"    
    SCRIPT_KEY = "p)ghhlikzcyzwq4gdgZpnhmkz"
    SERVER_URL = "https://4thacademy.shotgrid.autodesk.com"
    base_path = "/home/rapa2/SHOW/baked/"

    # client = FolderStructureCreator(base_path)
    fetcher = ShotGridDataFetcher(SERVER_URL, SCRIPT_NAME, SCRIPT_KEY)
    creator = FolderStructureCreator(fetcher, base_path) 
    creator.create_asset_folders()
    creator.create_sequence_folders()
    