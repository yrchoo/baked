from shotgun_api3 import Shotgun

import os

class FolderStructure():
    def __init__(self):
        self._set_init_value()
        self._get_auth()
        self._make_project_folder("baked")

    def _set_init_value(self):
        self.show_path = "/home/rapa/baked/show"
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
        
        self.project_data.update(self.sg.find_one("Project", [['name', 'is', self.project_data['name']]]))
        
    def _make_project_folder(self, project_name):
        addr = f"{self.show_path}/{project_name}"
        self._check_file_exist(addr)
        self._make_asset_folder(f"{addr}/AST")
        self._make_seq_folder(f"{addr}/SEQ")

    def _check_file_exist(self, addr):
        print(addr)
        # os.system(f"touch {addr}/.gitkeep")
        if os.path.exists(addr) : return
        os.makedirs(addr)

    def _get_entity_from_project(self, entity_name):
        filters = [['project', 'is', self.project_data]]
        fields = ['code']
        result = self.sg.find(entity_name, filters, fields)
        return result
    
    def _get_shot_from_sequence(self, seq):
        filters = [['sequence', 'is', seq]]
        result = self.sg.find("Shot", filters)
        return result
    
    def _get_entity_from_another(self, entity_type, field, from_ent):
        filters = [[field, 'is', from_ent]]
        fields = ['code', 'content']
        result = self.sg.find(entity_type, filters, fields)
        return result

    def _make_seq_folder(self, addr):
        addr = f"{addr}"
        self._check_file_exist(f"{addr}")
        seqs = self._get_entity_from_project("Sequence")
        for seq in seqs:
            seq_name = seq['code']
            self._check_file_exist(f"{addr}/{seq_name}")
            self._make_shot_folder(f"{addr}/{seq_name}", seq)

    def _make_shot_folder(self, addr, seq):
        shots = self._get_entity_from_another("Shot", "sg_sequence", seq)
        for shot in shots:
            shot_name = shot['code']
            self._check_file_exist(f"{addr}/{shot_name}")
            self._make_task_folder(f"{addr}/{shot_name}", shot)

    def _make_asset_folder(self, addr):
        addr = f"{addr}"
        self._check_file_exist(f"{addr}")
        # asset_types = self.sg.schema_field_read("Asset", "sg_asset_type", self.project_data)['sg_asset_type']['properties']['valid_values']['value']
        asset_types = ["Character", "Prop", "Environment"]
        
        for asset_type in asset_types:
            asset_addr = f"{addr}/{asset_type.title()}"
            self._check_file_exist(asset_addr)
            assets = self.sg.find('Asset', [['project', 'is', self.project_data],['sg_asset_type', 'is', asset_type]], ['code'])
            for ast in assets:
                ast_name = ast['code']
                self._check_file_exist(f"{asset_addr}/{ast_name}")
                self._make_task_folder(f"{asset_addr}/{ast_name}", ast)


    def _make_task_folder(self, addr, obj):
        tasks = self._get_entity_from_another("Task", "entity", obj)
        for task in tasks:
            task_name = task['content'].upper()
            self._check_file_exist(f"{addr}/{task_name}")
            self._make_dev_pub(f"{addr}/{task_name}")

    def _make_dev_pub(self, addr):
        dev_path = f"{addr}/dev"
        pub_path = f"{addr}/pub"
        self._check_file_exist(dev_path)
        self._check_file_exist(pub_path)



if __name__ == "__main__":
    FolderStructure()