import nuke
import os

import loader
import get_shotgrid_data

sg = get_shotgrid_data.Shotgrid_Data("baked")
load = loader.Loader(sg)

def init():
    # cur_file_path = load.sg.user_info['file path']
    # if not cur_file_path:
    # cur_file_path = "/home/rapa/show/baked/SEQ/ABC/ABC_0010/CMP/dev/nuke/Scenes/ABC_0010_CMP_v001.nknc"
    # _path_validate(os.path.dirname(cur_file_path))
    # nuke.scriptSaveAs(cur_file_path)
    # nuke.scriptOpen(cur_file_path)
    # publish에서 경로에 저장하는 메서드만 따와서 여기서 호출하면 되겠다
    pass

def _path_validate(path):
    if os.path.exists(path):
        return
    os.makedirs(path)

def show_loader():
    load.show()

init()
show_loader()
