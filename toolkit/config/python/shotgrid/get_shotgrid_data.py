from shotgun_api3 import Shotgun
try :
    from get_user_data import Get_User_Data
except :
    from shotgrid.get_user_data import Get_User_Data

class Shotgrid_Data():
    def __init__(self, project_name : str):
        if not project_name or type(project_name) != str:
            raise Exception("Shotgrid_Data() needs 1 argument(str)")
        
        self._set_init_value(project_name)
        self._get_auth()
        self.get_assigned_task(self.user_info['USER_NAME'])

    def _set_init_value(self, project_name):
        self.connected = False
        self.sg = "" # Shotgun()
        self.project_data = {
            "name" : project_name
        }

        self.user_info = Get_User_Data().return_data()   
        print(self.user_info)

    def _get_auth(self):
        script_name = "baked"
        script_key = "p)ghhlikzcyzwq4gdgZpnhmkz"

        try :
            self.sg = Shotgun("https://4thacademy.shotgrid.autodesk.com/", 
                        script_name, 
                        script_key)
            self.connected = True
        except:
            return

        filter_for_project = [['name', 'is', self.project_data['name']]]
        fields_for_project = ['type', 'id', 'name', 'content']
        self.project_data.update(self.sg.find_one("Project", filter_for_project, fields_for_project))

    def get_sequences_entities(self) -> list[dict]:
        filters_for_seq = [['project', 'is', self.project_data]]
        fields_for_seq = ['type', 'id', 'code']
        result = self.sg.find("Sequence", filters_for_seq, fields_for_seq)
        return result
    
    def get_asset_entities(self) -> list[dict]:
        filters_for_seq = [['project', 'is', self.project_data]]
        fields_for_seq = ['type', 'id', 'code', 'sg_asset_type']
        result = self.sg.find("Asset", filters_for_seq, fields_for_seq)
        return result

    def get_shot_from_seq(self, seq_ent) -> list[dict]:
        filters_for_shot = [['sg_sequence', 'is', seq_ent]]
        fields_for_shot = ['type', 'id', 'code']
        shots = self.sg.find("Shot", filters_for_shot, fields_for_shot)
        return shots
    
    def get_task_from_ent(self, ent) -> list[dict]:
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
            name = self.user_info["USER_NAME"]
        filters_for_humanuser = [['name', 'is', name]]
        user = self.sg.find_one("HumanUser", filters_for_humanuser)
        filters_for_task = [['task_assignees', 'is', user]]
        fields_for_task = ['content', 'entity']
        tasks = self.sg.find("Task", filters_for_task, fields_for_task)
        entity_list = []
        for task in tasks:
            entity_list.append(task['entity'])
        return entity_list
    
    def get_asset_entity(self, asset) -> dict:
        filter_for_asset = [['id', 'is', asset['id']]]
        fields_for_asset = ['id', 'sg_asset_type', 'code']
        asset = self.sg.find_one("Asset", filter_for_asset, fields_for_asset)
        return asset
    
    def get_shot_from_code(self, shot_code = None) -> dict:
        if not shot_code :
            shot_code = self.user_info["SHOT"]
        filter_for_shot = [['code', 'is', shot_code]]
        fields_for_shot = []
        shot = self.sg.find_one("Shot", filter_for_shot, fields_for_shot)
        return shot


    def get_assets_used_at_shot(self, shot_code = None)-> list[dict]:
        shot = self.get_shot_from_code(shot_code)
        filters_for_asset = [['shots', 'is', shot]]
        fields_for_asset = ['id', 'sg_asset_type', 'code']
        assets = self.sg.find("Asset", filters_for_asset, fields_for_asset)
        return assets


if __name__ == "__main__":
    Shotgrid_Data("baked")