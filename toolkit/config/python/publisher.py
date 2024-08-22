try:
    from PySide6.QtWidgets import QApplication, QWidget
    from PySide6.QtWidgets import QTreeWidgetItem, QMessageBox
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import QFile, Qt
    from PySide6.QtGui import QIcon, QPixmap, QFont
    import sys, os, yaml
    from shotgun_api3 import shotgun
    from work_in_maya import MayaAPI
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
        selected_objects = MayaAPI.get_selected_objects(self)
        print (selected_objects)
        if not selected_objects:
            self._show_message_to_select_item()
            return
        self.show()
        self._show_publish_item()
        self._get_published_file_type()
        self.ui.checkBox_check.setChecked(True)

    def _show_publish_item(self):
        """퍼블리쉬할 파일을 보여주는 메서드"""
        self.tree = self.ui.treeWidget
        self.tree.setColumnCount(3)
        self.tree.setColumnWidth(0,200)
        self.tree.setColumnWidth(1,20)
        self.tree.setColumnWidth(2,20)
        self.tree.setStyleSheet("QTreeWidget::item { margin:5px; height: 40px}")

        items = MayaAPI.get_selected_objects(self)
        file_name = MayaAPI.get_file_name(self)
        file_parent = QTreeWidgetItem(self.tree)
        file_parent.setText(0, file_name)
        self._set_text_bold(file_parent)

        for item in items:
            parent = QTreeWidgetItem(file_parent)
            parent.setText(0, item)
            parent.setText(1, "")
            parent.setText(2, "")
            parent.setFlags(parent.flags() | Qt.ItemIsUserCheckable)
            parent.setCheckState(1, Qt.Checked)
            self._set_image_icon(parent, "/home/rapa/baked/toolkit/config/python/3d.png")
            self._set_text_bold(parent)
            self._make_tree_item("Publish to Flow", parent)
            self._make_tree_item("Upload for reivew", parent)
            self.tree.setStyleSheet("QTreeWidget {font-size:12px}")
        self.tree.expandAll()

    def _set_text_bold(self, item):
        font = QFont()
        font.setBold(True)
        item.setFont(0, font)
    
    def _set_image_icon(self, item, path):
        icon = QIcon(QPixmap(path))
        item.setIcon(0, icon)
    
    def _show_file_detail(self):
        text = self.tree.currentItem().text(0)
        self.ui.lineEdit_file_info.setText(text)

    def _make_tree_item(self, text, parent):
        """트리 위젯 아이템 만드는 메서드"""
        item = QTreeWidgetItem(parent)
        item.setText(0, text)
        item.setText(1, "")
        item.setText(2, "")
        item.setFlags(parent.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(2, Qt.Checked)
        font = QFont()
        font.setPointSize(10)
        item.setFont(0, font)

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
        yaml_path = self._import_yaml_template()
        file_info_dict = self._get_user_info()
        tool = file_info_dict["tool"]
        level = file_info_dict["seq/asset"]
        step = file_info_dict["dev/pub"]
        current = f"{tool}_{level}_{step}"

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
                    "asset_type": "character",
                    "asset":"desk",
                    "task":"MOD",
                    "dev/pub":"dev",
                    "tool":"maya",
                    "version":"004",
                    "filename":"desk_MOD_v001",
                    "maya_extension":"mb"}
        return user_file_info

    def _make_version_up(self):
        """버전 업해주는 메서드"""
        file_path = self.active_user_info["file path"]
        if os.path.exists(file_path):
            version = self.active_user_info["version"]
            version_number = int(version.split("v")[1])
            version_number += 1
            str_version = str(version_number)
            new_version = f"v{str_version.zfill(3)}" 
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
        asset_steps_list = []
        shot_steps_list = []
        asset_steps = sg.find("Step", [['entity_type', 'is', 'Asset']], fields=["description"])
        shot_steps = sg.find("Step", [['entity_type', 'is', 'Shot']], fields=["description"])
        for asset in asset_steps:
            asset_steps_list.append(f"[Asset]  {asset['description']}")
        for shot in shot_steps:
            shot_steps_list.append(f"[Shot]  {shot['description']}")
            
        self.ui.comboBox_task.addItems(asset_steps_list)
        self.ui.comboBox_task.addItems(shot_steps_list)
    
    #######################유저가 입력한 정보를 샷그리드에 넣어주기#################
    def _publish_file_data(self):
        new_path = self._get_path_using_template()
        MayaAPI.save_file(self, new_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)           
    # app.exec() 