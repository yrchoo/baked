try :
    import maya.cmds as cmds
    import maya.mel as mel
except :
    print("import maya failed...")

import os
import re
import glob
import json


class LoadMayaFile():
    def __init__(self, path):
        self._load_file(path)

    def _load_file(self, path):
        _, file_ext = os.path.splitext(path)
        if file_ext in [".ma"]:
            self._get_shader_file(path)
        elif file_ext in [".mb"]:
            self._get_maya_binary_by_reference(path)
        elif file_ext in [".abc"]:
            self._import_maya_file(path)

    def _make_group_name(self, path):
        file_name = os.path.basename(path)
        file_name.split('_')
        new_name = f"{file_name[0]}_{file_name[1]}_grp" # Asset_TASK_grp
        return new_name

    def _get_maya_binary_by_reference(self, path): # .mb
        file_name, _ = os.path.splitext(os.path.basename(path))

        name_space = self._make_group_name(path)
        cmds.file(path, reference=True, mergeNamespacesOnClash=False, namespace=name_space)


    def _get_shader_file(self, path):
        # 뭔가.. 내가 불러온 shader를 자동으로 mod에 매핑해주는 일을 해야됨!!
        # 자동으로 shader를 mapping해주기 위해서 maya ascii로 저장했읍니다
        file_path = os.path.dirname(path)
        file_name, _ = os.path.splitext(os.path.basename(path))
        name_space = self._make_group_name(path)
        cmds.file(path, i=True, type="mayaAscii", mergeNamespacesOnClash=False, namespace=name_space)


        with open(f"{file_path}{file_name}.json", "r") as f:
            shader_data = json.load(f)

        object_list = cmds.ls(type="mesh")
        all_shaders = cmds.ls(materials=True)

        for shader, obj_list in shader_data.items():
            matching_shader = next((s for s in all_shaders if shader in s), None)
            if not matching_shader:
                continue
            for obj_name in obj_list:
                obj = next((s for s in object_list if obj_name in s), None)
                if not obj:
                    continue
                cmds.select(obj, add=True)
            cmds.hyperShade(assign=matching_shader)
            cmds.select(clear=True)
            
    def _import_maya_file(self, path):
        cmds.ABCImport(path, mode="import")
                




