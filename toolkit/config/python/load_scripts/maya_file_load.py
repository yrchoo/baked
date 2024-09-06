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
    def load_file(self, path):
        _, file_ext = os.path.splitext(path)
        if file_ext in [".ma"]:
            self._get_shader_file(path)
        elif file_ext in [".mb"]:
            self._get_file_by_reference(path, 'mayaBinary')
        elif file_ext in [".abc"]:
            self._get_file_by_reference(path, 'Alembic')

    def _make_group_name(self, path):
        file_name = os.path.basename(path)
        name = file_name.split("_v")[0]
        new_name = f"{name}_grp" # Asset_TASK_grp
        return new_name

    def _get_file_by_reference(self, path, file_type):
        name_space = self._make_group_name(path)
        cmds.file(path, reference=True, type=file_type, mergeNamespacesOnClash=False, namespace=name_space)

        if file_type == "Alembic":
            file_name = os.path.basename(path)
            if "aniCam" in file_name:
                cameras = cmds.ls(type='camera')
                for camera_ in cameras:
                    if "aniCam" in camera_:
                        cam_transform = cmds.listRelatives(camera_, parent=True)[0]
                        print(f"Checking camera transform: {cam_transform}")
                        model_panels = cmds.getPanel(type="modelPanel")
                        break
                if model_panels:
                    for panel in model_panels:
                        cmds.modelEditor(panel, e=True, displayLights="all")
                        cmds.modelEditor(panel, e=True, shadows=True)
                        cmds.modelEditor(panel, e=True, grid=False)
                        print("조명과 그림자가 활성화 되었고 그리드는 비활성화 되었습니다.")
                cmds.lookThru(cam_transform)


    def _get_shader_file(self, path):
        # 뭔가.. 내가 불러온 shader를 자동으로 mod에 매핑해주는 일을 해야됨!!
        # 자동으로 shader를 mapping해주기 위해서 maya ascii로 저장했읍니다
        name_space = self._make_group_name(path)
        cmds.file(path, i=True, type="mayaAscii", mergeNamespacesOnClash=False, namespace=name_space)

        json_path = path.replace(".ma", ".json")

        with open(json_path, "r") as f:
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

    def reload_maya_file(self, cur_path, new_path):
        references = cmds.ls(type='reference')

        matching_refs = []

        for ref in references:
            if ref == 'sharedRefereceNode':
                # reference 노드 자체는 포함하지 않기 때문에 기본 노드 필터링
                continue

            ref_path = cmds.referenceQuery(ref, file_name=True)
            if ref_path == cur_path:
                matching_refs.append(ref)

        for ref in matching_refs:
            cmds.file(new_path, loadReference=ref)
            # Reload
            cmds.file(ref, loadReference=True)



