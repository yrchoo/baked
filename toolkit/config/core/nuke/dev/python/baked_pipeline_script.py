



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
import publisher
import upload_review

from importlib import reload


def init():
    load_win.OPEN_FILE.connect(open_file)
    save_win.SAVE_FILE.connect(save_file)
    tracker_win.RELOAD_FILE.connect(reload_file)
    tracker_win.LOAD_FILE.connect(LoadNukeFile().load_file_with_read_node)

def show_loader():
    load_win.show()

def show_tracker():
    tracker_win.show()

def show_publisher():
    reload(publisher)
    global publish_win
    publish_win = publisher.Publisher(sg, "nuke")
    publish_win.show()

def show_review():
    reload(upload_review)
    review_win = upload_review.Review(sg, "nuke")
    review_win.show()


@ Slot()
def open_file(path):
    if nuke.root().knob("name").value():
        LoadNukeFile().load_file_with_read_node(path)
        tracker_win.opened_file_path_list.append(path)
        tracker_win.get_opened_file_list()
    else : 
        nuke.scriptOpen(path)
        setup_nuke_project()
            
def create_undistortion_node():
    # Undistortion을 위한 노드 생성
    lens_distortion_node = nuke.createNode('LensDistortion')
    lens_distortion_node['invertDistortion'].setValue(True)

    reformat_node = nuke.createNode('Reformat')
    reformat_node['resize'].setValue('none')  # Resize 옵션을 None으로 설정 (리사이즈 방지)
    reformat_node['box_width'].setValue(sg.undistortion_width)
    reformat_node['box_height'].setValue(sg.undistortion_height)


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

def set_write_node_path():
    cur_path = nuke.root().knob("name").value()
    dir_name = os.path.dirname(cur_path)
    dir_name = dir_name.replace('/scenes', '/images/')
    base_name, ext = os.path.splitext(os.path.basename(cur_path))
    
    nodes = nuke.allNodes("Write")
    for node in nodes:
        node_name = node.knob("name").value()
        new_write_file = f"{base_name.split('.')[0]}_{node_name}"
        new_write_path = f"{dir_name}{new_write_file}/{new_write_file}.####.exr"
        if not os.path.exists(os.path.basename(new_write_path)):
            os.makedirs(os.path.basename(new_write_path))
        node.knob("file").setValue(f"{dir_name}{new_write_path}")

def setup_nuke_project():
    nuke.root().knob("colorManagement").setValue("OCIO")
    nuke.root().knob("OCIO_config").setValue("fn-nuke_cg-config-v1.0.0_aces-v1.3_ocio-v2.1")

    if sg.frame_start :
            nuke.root().knob("first_frame").setValue(int(sg.frame_start))
    else:
        nuke.root().knob("first_frame").setValue(1001)
    first_frame = nuke.root().knob("first_frame").value()
    print(f"Set Start Frame to {first_frame}")
    if sg.frame_last:
        nuke.root().knob("last_frame").setValue(int(sg.frame_last))
    else:
        nuke.root().knob("last_frame").setValue(nuke.root().knob("first_frame").value() + 100)
    last_frame = nuke.root().knob("last_frame").value()
    print(f"Set Last Frame to {last_frame}")
    
    if sg.width and sg.height:
        new_format = f"{sg.width} {sg.height} 1.0 {sg.project['name']}_{sg.height}"
        nuke.addFormat(new_format)
        nuke.root().knob("format").setValue(f"{sg.project['name']}_{sg.height}")
        print(f"Set Format to {new_format}")


sg = ShotGridDataFetcher()
load_win = loader.Loader(sg, "nuke")
save_win = save.SaveFile()
tracker_win = file_tracker.Tracker(sg, read_node_file_list())

init()
if nuke.root().knob("name").value() == "" : 
    show_loader()
