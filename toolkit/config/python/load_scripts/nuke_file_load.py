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

    def _get_frame_num(self, read_node, path):
        _, ext = os.path.splitext(path)
        if ext not in [".png", ".exr"] :
            read_node.knob("file").setValue(path)
            return
        print(path)
        path_for_glob = path.replace("####", "*")
        print(path)
        file_list = glob.glob(path_for_glob)
        file_list.sort()

        p = re.compile("[.]\d{4}[.]")
        print(file_list[0], file_list[-1])
        first_frame = int(p.search(file_list[0]).group().split('.')[1])
        last_frame = int(p.search(file_list[-1]).group().split('.')[1])
        
        new_path = f"{path}"
        read_node.knob("file").setValue(new_path)
        read_node.knob("first").setValue(first_frame)
        read_node.knob("last").setValue(last_frame)
        

    def _make_read_node(self, path):
        try :
            read_node = nuke.createNode("Read")
            self._get_frame_num(read_node, path)
        except :
            print("nuke에서 제대로 동작하지 않음")


        
