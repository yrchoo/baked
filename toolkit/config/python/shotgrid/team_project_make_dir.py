import os
from shotgun_api3 import Shotgun
try :
    from team_project_fetch_data import ShotGridDataFetcher
except :
    from shotgrid.team_project_fetch_data import ShotGridDataFetcher


class FolderStructureCreator:
    def __init__(self, SERVER_URL, SCRIPT_NAME, SCRIPT_KEY, base_path):
        self.base_path = base_path
        self.fetcher = ShotGridDataFetcher(SERVER_URL, SCRIPT_NAME, SCRIPT_KEY)
        self.project_id = self.fetcher.fetch_project_id()

# 에셋 폴더를 만드는 툴
    def asset_folder_making_tool(self, asset_type, asset_code, asset_task_content):
        path = os.path.join(self.base_path, "Asset", asset_type, asset_code, asset_task_content)
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Folder Created: {path}")
        else:    
            pass
            print(f"Folder Already Exists: {path}")

        for subfolder in ['dev', 'pub']:
            subfolder_path = os.path.join(path, subfolder)
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)
                print (f"Folder Created: {subfolder_path}")
            else:
                pass
                print (f"Folder Already Exists: {subfolder_path}")



# 시퀀스 폴더를 만드는 툴
    def seq_folder_making_tool(self, base_folder, folder_code, task_content=None):
        path = os.path.join(self.base_path, base_folder, folder_code, task_content or '')
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Folder Created: {path}")
        else:    
            pass
            print(f"Folder Already Exists: {path}")

            for subfolder in ['dev', 'pub']:
                subfolder_path = os.path.join(path, subfolder)
                if not os.path.exists(subfolder_path):
                    os.makedirs(subfolder_path)
                    print(f"Folder Created: {subfolder_path}")
                else:
                    pass
                    print(f"Folder Already Exists: {subfolder_path}")

    

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
            self.seq_folder_making_tool('Sequence', seq_code)

            for shot in all_shots:
                if shot['sg_sequence']['id'] == seq['id']:
                    shot_code = shot['code']
                    self.seq_folder_making_tool(os.path.join('Sequence', seq_code), shot_code)

                    for task in seq_tasks:
                        if task['entity']['id'] == shot['id']:
                            seq_task_content = task['content'] 
                            self.seq_folder_making_tool(os.path.join('Sequence',seq_code, shot_code), seq_task_content)



if __name__ == "__main__":

    SCRIPT_NAME = "baked"    
    SCRIPT_KEY = "p)ghhlikzcyzwq4gdgZpnhmkz"
    SERVER_URL = "https://4thacademy.shotgrid.autodesk.com"
    base_path = "/home/rapa2/SHOW/baked/"

    # client = FolderStructureCreator(base_path)
    creator = FolderStructureCreator(SERVER_URL, SCRIPT_NAME, SCRIPT_KEY, base_path) 
    creator.create_asset_folder()
    creator.create_seq_folders()
    