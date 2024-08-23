import os

from load_scripts.nuke_file_load import LoadNukeFile

class FileOpen():
    def __init__(self, path, tool = None):
        self.path = path
        self._set_tool_program_val()

        if tool :
            pass
        else: # 현재 사용중인 툴이 없을 때
            tool = self._get_tool_data(tool)
            self._run_open_file_cmd(tool)


    def _set_tool_program_val(self):
        self.tools = {
            "nuke" : [".nknc", "nk"],
            "maya" : [".mb", ".ma"]
        }

    def _get_tool_data(self):
        _, file_ext = os.path.splitext(self.path)
        print(file_ext)
        for tool, ext_list in self.tools.items():
            if file_ext in ext_list:
                return tool
            
    def _run_open_file_cmd(self, tool):
        print (tool)
        if tool == "nuke":
            try :
                cmd = f"source /home/rapa/baked/toolkit/config/core/env/nuke.env && /opt/Nuke/Nuke15.1v1/Nuke15.1 --nc {self.path}"
            except :
                print(f"Nuke에서 파일 '{self.path}'를 여는 작업을 하려고 했습니다")
        elif tool == "maya":
            try :
                cmd = f"source /home/rapa/baked/toolkit/config/core/env/maya.env && /usr/autodesk/maya2023/bin/maya {self.path}"
            except :
                print(f"Maya에서 파일 '{self.path}'를 여는 작업을 하려고 했습니다")
        print(cmd)
        os.system(cmd)

    def _load_file(self, tool):
        if tool == "nuke":
            LoadNukeFile(self.path)
