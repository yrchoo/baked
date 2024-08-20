import nuke
import os

import loader
import get_shotgrid_data

sg = get_shotgrid_data.Shotgrid_Data("baked")
load = loader.Loader(sg)

def init():
    pass

def _path_validate(path):
    if os.path.exists(path):
        return
    os.makedirs(path)

def show_loader():
    load.show()

init()
show_loader()
