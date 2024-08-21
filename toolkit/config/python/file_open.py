import os

class FileOpen():
    def __init__(self, path):
        self.path = path
        self._set_tool_program_val()

        tool = self._get_tool_data()
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
            cmd = f"source /home/rapa/baked/toolkit/config/core/env/nuke.env && /opt/Nuke/Nuke15.1v1/Nuke15.1 --nc {self.path}"
        elif tool == "maya":
            pass
        print(cmd)
        os.system(cmd)