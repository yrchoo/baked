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


def init():
    load_win.OPEN_FILE.connect(open_file)
    save_win.SAVE_FILE.connect(save_file)
    tracker_win.RELOAD_FILE.connect(reload_file)
    tracker_win.LOAD_FILE.connect(LoadNukeFile().load_file_with_read_node)

def show_loader():
    load_win.show()

def show_tracker():
    # tracker에 존재하는 리스트를 갱신해줘야함
    tracker_win.show()

def show_publisher():
    pass

@ Slot()
def open_file(path):
    if nuke.root().knob("name").value():
        LoadNukeFile().load_file_with_read_node(path)
        tracker_win.opened_file_path_list.append(path)
        tracker_win.get_opened_file_list()
    else : 
        nuke.scriptOpen(path)
        nuke.root().knob("first_frame").setValue(sg.frame_start)
        nuke.root().knob("last_frame").setValue(sg.frame_last)
        new_format = f"{sg.width} {sg.height} 1.0 {sg.project['name']}_{sg.height}"
        nuke.addFormat(new_format)
        nuke.root().knob("foramt").setValue(f"{sg.project['name']}_{sg.height}")

        # Undistortion을 위한 노드 생성
        lens_distortion_node = nuke.createNode('LensDistortion')
        lens_distortion_node['invertDistortion'].setValue(True)

        reformat_node = nuke.createNode('Reformat')
        reformat_node['resize'].setValue('none')  # Resize 옵션을 None으로 설정 (리사이즈 방지)
        reformat_node['box_width'].setValue(sg.undistortion_width)
        reformat_node['box_height'].setValue(sg.undistortion_height)


    # tracker에 존재하는 리스트를 갱신해줘야함

@ Slot()
def reload_file(cur_path, new_path):
    LoadNukeFile().reload_nuke_file(cur_path, new_path)

def pop_save_file_ui():
    path = nuke.root().knob("name").value()
    save_win.save_file(path)

@ Slot()
def save_file(path):
    print("save file method")
    nuke.scriptSaveAs(path)

def read_node_file_list():
    open_file_list = []
    open_file_list.extend(nuke.allNodes("Read"))
    open_file_list.extend(nuke.allNodes("ReadGeo"))

    return open_file_list

sg = ShotGridDataFetcher()
load_win = loader.Loader(sg, "nuke")
save_win = save.SaveFile()
tracker_win = file_tracker.Tracker(sg, read_node_file_list())


init()
if nuke.root().knob("name").value() == "" : 
    show_loader()
