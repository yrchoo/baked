try :
    from PySide6.QtCore import Slot
except:
    from PySide2.QtCore import Slot

import nuke
import os

import loader
from fetch_shotgrid_data import ShotGridDataFetcher
import save
import file_tracker
from load_scripts.nuke_file_load import LoadNukeFile

sg = ShotGridDataFetcher()
load_win = loader.Loader(sg, "nuke")
save_win = save.SaveFile()
tracker_win = file_tracker.Tracker(sg)

def init():
    load_win.OPEN_FILE.connect(open_file)
    save_win.SAVE_FILE.connect(save_file)
    tracker_win.RELOAD_FILE.connect()

def show_loader():
    load_win.show()

@ Slot()
def open_file(path):
    if nuke.root().knob("name").value():
        LoadNukeFile().load_file_with_read_node(path)
    else : 
        nuke.scriptOpen(path)

@ Slot()
def reload_file(cur_path, new_path):
    LoadNukeFile().reload_nuke_file(cur_path, new_path)

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
