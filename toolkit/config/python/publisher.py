try:
    from PySide6.QtWidgets import QApplication, QWidget
    from PySide6.QtWidgets import QTreeWidgetItem, QMessageBox
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import QFile, Qt
    from PySide6.QtGui import QIcon, QPixmap, QFont
    import sys, os, yaml
    from shotgun_api3 import shotgun
    # from work_in_maya import MayaAPI
    import department_publish 
except:
    from PySide2.QtWidgets import QApplication, QWidget
    from PySide2.QtWidgets import QTreeWidgetItem, QMessageBox
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtCore import QFile, Qt
    from PySide2.QtGui import QIcon, QPixmap, QFont
    import sys, os, yaml
    import maya.cmds as cmds
    from shotgun_api3 import shotgun
    from work_in_maya import MayaAPI
    import department_publish 
    from importlib import reload
    reload(department_publish)

class Publisher(QWidget):
    def __init__(self):
        super().__init__()
        self._set_ui()
        self._initial_setting()
        self._get_task_type()

        self.ui.checkBox_check.clicked.connect(self._select_all_items)
        self.ui.pushButton_collapse.clicked.connect(self._collapse_tree)
        self.ui.pushButton_expand.clicked.connect(self._expand_tree)
        self.ui.pushButton_publish.clicked.connect(self._publish_file_data)
        self.ui.pushButton_cancel.clicked.connect(self._cancel_and_close)
        self.ui.treeWidget.itemSelectionChanged.connect(self._show_file_detail)
        self.ui.comboBox_task.currentIndexChanged.connect(self._show_link_entity)

    def _set_ui(self):
        """ui 셋업해주는 메서드"""
        ui_file_path = '/home/rapa/baked/toolkit/config/python/publisher.ui' 
        ui_file = QFile(ui_file_path)
        ui_file.open(ui_file.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(ui_file, self)  
        ui_file.close()

    def _initial_setting(self):
        """초기 ui 세팅하는 메서드"""
        """tree에 데이터 넣기"""
        self.tree = self.ui.treeWidget
        self.tool = "maya" ##################
        department = self._get_user_info()['task']
        result = getattr(department_publish, department)(self.tree,'maya')
        if not result:
            return        
        self.show()
        self._get_published_file_type()
        self.ui.checkBox_check.setChecked(True)
    
    def _show_file_detail(self):
        text = self.tree.currentItem().text(0)
        if text in ["ㄴ Publish to Flow", "ㄴ Upload for reivew"]:
            return
        self.ui.lineEdit_file_info.setText(text) 

    def _expand_tree(self):
        """트리 위젯을 여는 메서드"""
        self.tree.expandAll()
        
    def _collapse_tree(self):
        """트리 위젯을 닫는 메서드"""
        self.tree.collapseAll()
    
    def _select_all_items(self):
        """모든 아이템 체크박스 선택되게 하는 메서드"""
        parent_count = self.tree.topLevelItemCount()
        for i in range(parent_count):
            parent_item = self.tree.topLevelItem(i)
            child_item_pub = parent_item.child(0)
            child_item_ver = parent_item.child(1)
            if self.ui.checkBox_check.isChecked():
                parent_item.setCheckState(1, Qt.Checked)
                child_item_pub.setCheckState(2, Qt.Checked)
                child_item_ver.setCheckState(2, Qt.Checked)
            else:
                parent_item.setCheckState(1, Qt.Unchecked)
                child_item_pub.setCheckState(2, Qt.Unchecked)
                child_item_ver.setCheckState(2, Qt.Unchecked)

    def _update_check_state(self):
        pass
    
    def _connect_check_state(self):
        parent_count = self.tree.topLevelItemCount()
        for i in range(parent_count):
            parent_item = self.tree.topLevelItem(i)
            child_item_pub = parent_item.child(0)
            child_item_ver = parent_item.child(1)
            if parent_item(1).isChecked():
                child_item_pub.setCheckState(2, True)
                child_item_ver.setCehcekd(2, True)
            else:
                child_item_pub.setChecked(False)
                child_item_ver.setChecked(False)
            if child_item_pub.isChecked() and child_item_ver.isChecked():
                parent_item.setChecked(True)
            else:
                parent_item.setChecked(False)

    def _show_message_to_select_item(self):
        msg = QMessageBox()
        msg.setWindowTitle("Important")
        msg.setText("Please select the objects to publish")
        msg.setIcon(QMessageBox.Information)
        msg.setDefaultButton(QMessageBox.Yes)
        msg.exec()
        
    def _work_in_nuke(self):
        pass

    def _work_in_maya(self):
        pass

    ##########################저장하고 버전 관리##################

    def _get_path_using_template(self):
        """템플릿을 이용해서 저장할 경로, 파일 이름 만드는 메서드"""

        ### abc 는 (버전그대로) 펍에 올라가고, mb파일, nknc 파일은 버전업돼서 저장되게
        yaml_path = self._import_yaml_template()
        file_info_dict = self._get_user_info()
        tool = file_info_dict["tool"]
        level = file_info_dict["seq/asset"]
        current = f"{tool}_{level}_pub"

        if current in yaml_path:
            root_path = yaml_path[f"{level}_root"]
            new_path = yaml_path[current]["definition"].replace(f"@{level}_root", root_path)
            new_path = new_path.format(**file_info_dict)   ### 각 키 이름 별로 딕셔너리랑 매칭되게 하는 겁니당
            self._check_validate(new_path)
        print (new_path)
        return new_path

    def _get_user_info(self):
        """유저에 대한 정보 가저오는 메서드"""
        user_file_info = {"project":"baked",
                    "seq/asset":"asset",
                    "asset_type": "Character",
                    "asset":"desk",
                    "task":"Modeling",
                    "dev/pub":"dev",
                    "tool":"maya",
                    "version":"004",
                    "filename":"desk_MOD_v001",
                    "maya_extension":"mb"}
        return user_file_info

    def _make_version_up(self):
        """버전 업해주는 메서드"""
        user_info = self._get_user_info()
        file_path = MayaAPI.get_current_path(self)
        if os.path.exists(file_path):
            version = user_info["version"]
            print(version)
            version_number = int(version.split("v")[1])
            version_number += 1
            str_version = str(version_number)
            new_version = f"{str_version.zfill(3)}" 
        return new_version
    
    def _import_yaml_template(self):
        """template.yml import 하는 메서드"""
        with open('/home/rapa/baked/toolkit/config/core/env/sy_template.yml') as f:
            yaml_data = yaml.load(f, Loader=yaml.FullLoader)
            yaml_path = yaml_data["paths"]
        return yaml_path
    
    def _check_validate(self, new_path):
        """저장할 파일 경로가 유효한지 확인하는 메서드 (폴더가 존재하지 않으면 생성해주기)"""
        file_path = "".join(new_path.split("/")[:-2])
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        
    def _cancel_and_close(self):
        self.close()
    
    ########################################shotgun part###############################################
    
    def _connect_sg(self):
        """샷그리드 연결시키는 메서드"""
        URL = "https://4thacademy.shotgrid.autodesk.com"
        SCRIPT_NAME = "pipeline key"
        API_KEY = "^axlq0daadimnwnatxrdoYfsm"
        sg = shotgun.Shotgun(URL,
                         SCRIPT_NAME,
                         API_KEY)
        return sg

    def _get_current_work_list(self):
        pass

    def _get_published_file_type(self):
        """published file type 콤보박스에 넣어주는 메서드"""
        sg = self._connect_sg()
        published_file_type = sg.find("PublishedFileType", [], fields=["code"])
        for info in published_file_type:
            self.ui.comboBox_type.addItem(info['code'])
        
    def _get_task_type(self):
        sg = self._connect_sg()
        asset_steps_list = ['-----------select------------']
        shot_steps_list = []
        asset_steps = sg.find("Step", [['entity_type', 'is', 'Asset']], fields=["description"])
        shot_steps = sg.find("Step", [['entity_type', 'is', 'Shot']], fields=["description"])

        for asset in asset_steps:
            asset_steps_list.append(f"[Asset]  {asset['description']}")
        for shot in shot_steps:
            shot_steps_list.append(f"[Shot]   {shot['description']}")
            
        self.ui.comboBox_task.addItems(asset_steps_list)
        self.ui.comboBox_task.addItems(shot_steps_list)
        return asset_steps_list, shot_steps_list

    def _show_link_entity(self):
        self.ui.comboBox_link.clear()
        task = self.ui.comboBox_task.currentText()[9:]
        sg = self._connect_sg()
        link_list = ['-----------select------------']
        step = sg.find("Step", [['description', 'is', task]], fields=["code"])[0]['code']
        link = sg.find("Task", [['step.Step.code', 'is', step], ['project.Project.name', 'is', 'baked']], fields=["entity"])
        for item in link:
            link_list.append(item['entity'].get('name'))
        if task == "-----------select------------":
            self.ui.comboBox_link.setCurrentIndex(0)
        self.ui.comboBox_link.addItems(link_list)
    
    #######################유저가 입력한 정보를 샷그리드에 넣어주기#################
    def _publish_file_data(self):
        new_path = self._get_path_using_template()
        print (new_path)
        if self.tool == "maya":
            MayaAPI.save_file(self, new_path)
        else:
            NukeAPI.save_file(slef, new_path)

    def _save_file_dev_version_up(self):
        new_path = self._get_path_using_template()

if __name__ == "__main__":
    app = QApplication(sys.argv)           
    # app.exec() 
