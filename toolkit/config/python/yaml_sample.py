import yaml
import os
import json

class MakePath():
    def __init__(self):
        self._get_path_using_template()

    def _get_path_using_template(self):
        """템플릿을 이용해서 저장할 경로, 파일 이름 만드는 메서드"""
        
        # yaml_path 불러오기
        yaml_path = self._import_yaml_template()

        ## 얘네는 로그인 정보들을 file_info_dict에 넣어주면 거기서 가져오는 겁니당 
        file_info_dict = self._get_user_info()
        tool = file_info_dict["tool"]
        level = file_info_dict["seq/asset"]
        step = file_info_dict["dev/pub"]
        
        ### 정보들 조합해서 템플릿에서 서칭할 키 만들어주고 ~
        current = f"{tool}_{level}_{step}"

        # yaml 파일이용해서 new_path 만들어주기
        if current in yaml_path:
            root_path = yaml_path[f"{level}_root"]
            new_path = yaml_path[current]["definition"].replace(f"@{level}_root", root_path)
            new_path = new_path.format(**file_info_dict)   ### 각 키 이름 별로 딕셔너리랑 매칭되게 하는 겁니당
            self._check_validate(new_path)

        print (new_path)
        return new_path, tool

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
    
    def _get_user_info(self):
        """로그인 정보 환경변수로부터 가져오는 메서드"""
        # if sequence:
        file_info = {"project":"baked",
                    "seq/asset":"sequence",
                    "sequence" : "ABC",
                    "shot":"ABC_0010",
                    "task":"CMP",
                    "dev/pub":"dev",
                    "tool":"nuke",
                    "version":"001",
                    "filename":"ABC_0010_CMP_v001",
                    "extension":"nknc"}
        
        # if asset:
        #     file_info = {"project":"baked",
        #                  "seq/asset":"asset",
        #                 "asset type": "character",
        #                 "asset":"desk",
        #                 "task":"MOD",
        #                 "dev/pub":"dev",
        #                 "tool":"maya",
        #                 "version":"004",
        #                 "filename":"desk_MOD_v001",
        #                 "extension":"nknc"}
        return file_info

        pass

MakePath()
        