try :
    from PySide6.QtCore import Slot
except:
    from PySide2.QtCore import Slot

import nuke
import os

import loader
import get_shotgrid_data
import save
import file_tracker

sg = get_shotgrid_data.Shotgrid_Data("baked")
load_win = loader.Loader(sg, "nuke")
save_win = save.SaveFile()
tracker_win = file_tracker.Tracker(sg)

def init():
    load_win.OPEN_FILE.connect(open_file)
    save_win.SAVE_FILE.connect(save_file)

def show_loader():
    load_win.show()

@ Slot()
def open_file(path):
    nuke.scriptOpen(path)

def pop_save_file_ui():
    path = nuke.root().knob("name").value()
    print(path)
    save_win.save_file(path)

@ Slot()
def save_file(path):
    print("save file method")
    print(path)
    nuke.scriptSaveAs(path)

init()
if nuke.root().knob("name").value() == "" : 
    show_loader()
