try :
    import nuke
except :
    print("import nuke failed...")

import os
import re
import glob

class LoadNukeFile():
    def __init__(self, path):
        self._make_read_node(path)

    def _get_frame_num(self, path):
        _, ext = os.path.splitext(path)
        if ext not in [".png", ".exr"] :
            return path

        path_for_glob = path.replace("####", "%04d")

        file_list = glob.glob(path_for_glob)
        file_list.sort()

        p = re.compile("[.]\d{4}[.]")
        first_frame = p.search(file_list[0]).group().split('.')[1]
        last_frame = p.search(file_list[-1]).group().split('.')[1]
        
        new_path = f"{path} {first_frame}-{last_frame}"

        return new_path
        


    def _make_read_node(self, path):
        new_path = self._get_frame_num(path)
        try :
            read_node = nuke.createNode("Read")
            read_node.knob("file").setValue(new_path)
        except :
            print("nuke에서 제대로 동작하지 않음")
        
