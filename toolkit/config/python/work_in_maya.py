import maya.cmds as cmds 
import maya.mel as mel 
import os
import json
import subprocess
import datetime

class MayaAPI():
    def __init__(self):
        pass
    
    def get_file_name(self):
        """현재 열려있는 마야 파일 이름 가져오는 메서드"""
        filepath = cmds.file(q=True, sn=True)
        filename = os.path.basename(filepath)
        return filename

    def get_selected_objects(self):
        """선택한 오브젝트 리스트 가져오는 메서드"""
        assets = cmds.ls(sl=True)
        return assets # 리스트

    def export_alemibc(self, path):
        """
        알렘빅이 저장될 경로를(디렉토리) 이용
        """
        assets = self.get_selected_objects()    # 선택된 object 리스트 : ['pSphere1', 'pCube1', 'pCylinder1', 'pCone1']
        start_frame = int(cmds.playbackOptions(query=True, min=True))
        last_frame = int(cmds.playbackOptions(query=True, max=True))

        for asset in assets:
            abc_cache_path = f"/home/rapa/show/{asset}.abc"
            alembic_args = ["-renderableOnly", "-writeFaceSets", "-uvWrite", "-worldSpace", "-eulerFilter"]

            alembic_args.append(f"-fr {start_frame} {last_frame}")
            alembic_args.append(f"-file '{abc_cache_path}'")
            alembic_args.append(f"-root {asset}")
            abc_export_cmd = 'AbcExport -j "%s"' % " ".join(alembic_args)
            mel.eval(abc_export_cmd)
    
    def export_shader(self, export_path):
        """
        maya에서 오브젝트에 어싸인된 셰이더들을 ma 파일로 익스포트하고,
        그 정보들을 json 파일로 익스포트 하는 함수이다.
        """

        shader_dictionary = self.collect_shader_assignments()

        for shader, _ in shader_dictionary.items():
            cmds.select(shader, add=True)    

        ma_file_path = f"{export_path}/shader.ma"
        json_file_path = f"{export_path}/shader.json"

        cmds.file(ma_file_path, exportSelected=True, type="mayaAscii")
        with open(json_file_path, 'w') as f:
            json.dump(shader_dictionary, f)

        cmds.select(clear=True)
    
    def collect_shader_assignments(self):
        """
        셰이더와 오브젝트들을 컬렉션하는 함수.
        """
        shader_dictionary = {}
        shading_groups = cmds.ls(type="shadingEngine")
        for shading_group in shading_groups:
            shader = cmds.ls(cmds.listConnections(shading_group + ".surfaceShader"), materials=True)    
            if not shader:
                continue
            objects = cmds.sets(shading_group, q=True)
            shader_name = shader[0]
            if objects:
                if shader_name not in shader_dictionary:
                    shader_dictionary[shader_name] = []
                shader_dictionary[shader_name].extend(objects)
        return shader_dictionary

    def save_file(self, path):
        """마야 파일 저장하는 메서드"""
        file_path, name = os.path.split(path)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        cmds.file(rename=name)
        cmds.file(save=True)
