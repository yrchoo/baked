from shotgun_api3 import Shotgun

class AddShotgridData():
    def __init__(self):
        self._set_init_value()
        self._get_auth()
        self._get_project_entity()
        self._create_asset()
        self._create_seq()

        # self._edit_shot_entity()

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
        
    def _get_project_entity(self):
        filters = [['name', 'is', self.project_data['name']]]
        project = self.sg.find_one("Project", filters, ['id'])
        self.project_data.update(project)

    def _get_entity_by_code(self, entity, code):
        filters = [['code', 'is', code]]
        val = self.sg.find_one(entity, filters, ['id', 'code'])
        return val

    def _create_seq(self):
        seq_list = ["ABC", "DEF", "GHI"]
        for seq in seq_list:
            seq_code = seq
            data = {
                'project' : self.project_data,
                'code' : seq_code
            }
            entity = self._get_entity_by_code('Sequence', data['code'])
            if not entity : 
                print("Create Sequence : " + seq_code)
                self.sg.create("Sequence", data)
            self._create_shot(seq_code)

    def _create_asset(self):
        template = self._get_task_template('Baked Character Asset Template')
        seq_list = ["Apple", "Banana", "Melon"]
        for asset_code in seq_list:
            data = {
                'project' : self.project_data,
                'code' : asset_code,
                'task_template' : template
            }
            entity = self._get_entity_by_code('Asset', data['code'])
            if entity : continue
            print("Create Asset : " + asset_code)
            self.sg.create("Asset", data)


    def _get_task_template(self, code):
        filters = [['code', 'is', code]]
        template = self.sg.find_one('TaskTemplate', filters)
        return template

    def _create_shot(self, seq_code):
        seq = self._get_entity_by_code('Sequence', seq_code)
        template = self._get_task_template('Baked Shot Template')
        for num in [10, 20, 30] :
            shot_code = '%s_%04d' % (seq['code'], num)
            data = {
                'project' : self.project_data,
                'code' : shot_code,
                'task_template' : template, 
                'sg_sequence' : seq
            }
            entity = self._get_entity_by_code('Shot', data['code'])
            if entity : 
                continue
            print("Create Shot : " + shot_code)
            print(data)
            self.sg.create("Shot", data)

    def _edit_shot_entity(self):
        filters = [['project', 'is', self.project_data]]
        shots = self.sg.find("Shot", filters)
        for shot in shots:
            self._update_entity_template(shot)

    def _update_entity_template(self, entity):
        template = self._get_task_template(self.template[entity['type']])
        self.sg.update(entity['type'], entity['id'], {'task_template' : template})
            

if __name__ == "__main__":
    AddShotgridData()