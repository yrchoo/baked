import nuke
import os

import loader
import get_shotgrid_data
import save

sg = get_shotgrid_data.Shotgrid_Data("baked")
load = loader.Loader(sg, "nuke")
save = save.SaveFile()

def init():
    load.OPEN_FILE.connect(open_file)
    save.SAVE_FILE.connect(save_file)

def show_loader():
    load.show()

def open_file(path):
    nuke.scriptOpen(path)

def pop_save_file_ui():
    save.save_file(nuke.root().knob("name"))

def save_file(path : str):
    nuke.scriptSave(path)

init()
show_loader()
