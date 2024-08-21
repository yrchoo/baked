import nuke
import os

import loader
import get_shotgrid_data

sg = get_shotgrid_data.Shotgrid_Data("baked")
load = loader.Loader(sg, "nuke")

def init():
    load.OPEN_FILE.connect(open_file)

def show_loader():
    load.show()

def open_file(path):
    nuke.scriptOpen(path)

init()
show_loader()
