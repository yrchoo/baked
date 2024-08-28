import os
from shotgun_api3 import Shotgun

class FolderStructureCreator:
    def __init__(self, fetcher, base_path): # ***** shotgridDataFetcher가 선언될 때 현재 작업물이 저장될 경로들을 체크하는 게 좋을 것 같아서
                                   # shotgridDataFetcher에서 FolderStructureCreator를 호출하고 fetcher 객체를 넘겨주는 걸로 수정했습니다
        self.base_path = base_path
        self.fetcher = fetcher
        self.project_id = self.fetcher.project['id'] # ***** 수정했습니다

        self.create_asset_folder()
        self.create_seq_folders()

    # ***** 프로젝트 이름으로 된 폴더부터 만들어야됩니다! 수정 부탁드려욥
    # 폴더가 존재하는 지를 확인하고 파일을 만드는 과정이 각 메서드에서 반복되는데 
    # 이 부분을 또 하나의 메서드로 빼두면 나중에 폴더 안만들고 테스트만 해보거나 할 때 유용할 것 같아요

    # 에셋 폴더를 만드는 툴
    def asset_folder_making_tool(self, asset_type, asset_code, asset_task_content):
        path = os.path.join(self.base_path, "AST", asset_type, asset_code, asset_task_content)
        print(path)
        # if not os.path.exists(path):
        #     os.makedirs(path)
        #     print(f"Folder Created: {path}")
        # else:    
        #     pass
        #     print(f"Folder Already Exists: {path}")

        # for subfolder in ['dev', 'pub']:
        #     subfolder_path = os.path.join(path, subfolder)
        #     print(subfolder_path)
        #     if not os.path.exists(subfolder_path):
        #         os.makedirs(subfolder_path)
        #         print (f"Folder Created: {subfolder_path}")
        #     else:
        #         pass
        #         print (f"Folder Already Exists: {subfolder_path}")



    # 시퀀스 폴더를 만드는 툴
    def seq_folder_making_tool(self, base_folder, folder_code, task_content=None):
        path = os.path.join(self.base_path, base_folder, folder_code, task_content or '')
        print(path)
        # if not os.path.exists(path):
        #     os.makedirs(path)
        #     print(f"Folder Created: {path}")
        # else:    
        #     pass
        #     print(f"Folder Already Exists: {path}")

        #     for subfolder in ['dev', 'pub']:
        #         subfolder_path = os.path.join(path, subfolder)
        #         if not os.path.exists(subfolder_path):
        #             os.makedirs(subfolder_path)
        #             print(f"Folder Created: {subfolder_path}")
        #         else:
        #             pass
        #             print(f"Folder Already Exists: {subfolder_path}")

    

    def create_asset_folder(self):
        assets = self.fetcher.fetch_assets(self.project_id)
        asset_tasks = self.fetcher.fetch_asset_tasks(assets)
        for asset in assets:
            asset_type = asset['sg_asset_type']
            asset_code = asset['code']

            for task in asset_tasks:
                if task['entity']['id'] == asset['id']:
                    asset_task_content = task['content']
                    self.asset_folder_making_tool(asset_type, asset_code, asset_task_content)


    def create_seq_folders(self):
        seqs = self.fetcher.fetch_seq(self.project_id)
        all_shots = self.fetcher.fetch_shots(seqs)
        seq_tasks = self.fetcher.fetch_seq_tasks()

        for seq in seqs:
            seq_code = seq['code']
            self.seq_folder_making_tool('SEQ', seq_code)

            for shot in all_shots:
                if shot['sg_sequence']['id'] == seq['id']:
                    shot_code = shot['code']
                    self.seq_folder_making_tool(os.path.join('SEQ', seq_code), shot_code)

                    for task in seq_tasks:
                        if task['entity']['id'] == shot['id']:
                            seq_task_content = task['content'] 
                            self.seq_folder_making_tool(os.path.join('SEQ',seq_code, shot_code), seq_task_content)



if __name__ == "__main__":

    SCRIPT_NAME = "baked"    
    SCRIPT_KEY = "p)ghhlikzcyzwq4gdgZpnhmkz"
    SERVER_URL = "https://4thacademy.shotgrid.autodesk.com"
    base_path = "/home/rapa2/SHOW/baked/"

    # client = FolderStructureCreator(base_path)
    creator = FolderStructureCreator(SERVER_URL, SCRIPT_NAME, SCRIPT_KEY, base_path) 
    creator.create_asset_folder()
    creator.create_seq_folders()
    