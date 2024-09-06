print ("*" * 30)
print ("meny.py")
print ("menu script is processed")
print ("*" * 30)

import maya.cmds as cmds
import maya.mel as mel

try :
    from PySide6.QtCore import Slot
except:
    from PySide2.QtCore import Slot

import sys
import os
from importlib import reload

sys.path.append("/home/rapa/baked/toolkit/config/python")
sys.path.append("/home/rapa/baked/toolkit/config/python/shotgrid")

from fetch_shotgrid_data import ShotGridDataFetcher
from load_scripts.maya_file_load import LoadMayaFile

sg = ShotGridDataFetcher()

import loader
import save


import file_tracker

from importlib import reload
import publisher
import upload_review

def init():
    load_win.OPEN_FILE.connect(open_file)
    save_win.SAVE_FILE.connect(save_file)
    tracker_win.RELOAD_FILE.connect(reload_file)
    tracker_win.LOAD_FILE.connect(open_file)
    tracker_win.RELATED_FILE_DATA_CHANGED.connect(load_win.set_content_tree_widget_by_shotgrid)
    pass

def loader_func():
    """
    메뉴를 선언하는 함수보다 윗쪽에 이 코드를 적어주세요.
    add_custom_menu보다 밑으로 내려가면 함수를 찾지 못해요~!
    이 함수는 메뉴를 테스트하는 함수입니다.
    """
    # ### 예린님 로더에 input값 연결해주기 ###
    # reload(loader)
    load_win.show()

def save_func():
    path = cmds.file(query=True, sceneName=True)
    save_win.save_file(path)

def tracker_func():
    tracker_win.get_opened_file_list(get_ref_file_path_list())
    tracker_win.show()

def open_file(path):
    current_file_path = cmds.file(query=True, sceneName=True)
    if current_file_path :
        LoadMayaFile().load_file(path)
        tracker_win.get_opened_file_list(get_ref_file_path_list())
        
    else :
        current_file_path = path
        # 해상도 설정
        if sg.width and sg.height:
            cmds.setAttr('defaultResolution.width', int(sg.width))
            cmds.setAttr('defaultResolution.height', int(sg.height))

        # 언디스토션 사이즈 설정
        if sg.undistortion_width and sg.undistortion_height:
            cmds.setAttr('defaultResolution.deviceAspectRatio', float(sg.undistortion_width) / float(sg.undistortion_height))
            cmds.setAttr('defaultResolution.pixelAspect', 1)

        # 프레임 설정
        if sg.frame_start and sg.frame_end:
            cmds.playbackOptions(min=int(sg.frame_start), max=int(sg.frame_end))
            
            # cmds.currentTime(sg.frame_start)
            cmds.setAttr('defaultRenderGlobals.startFrame', int(sg.frame_start))
            cmds.setAttr('defaultRenderGlobals.endFrame', int(sg.frame_end))

        else:
            cmds.playbackOptions(min=1001, max=1096)
            # cmds.currentTime(sg.frame_start)
            
            cmds.setAttr('defaultRenderGlobals.startFrame', 1001)
            cmds.setAttr('defaultRenderGlobals.endFrame', 1096)

        # 렌더 프레임 설정
        
        cmds.file(path, open=True, force=True)

    _check_dir(current_file_path)

@ Slot()
def save_file(path):
    cmds.file(rename=path)
    cmds.file(save=True, type='mayaBinary')

def reload_file(cur_path, new_path):
    LoadMayaFile().reload_maya_file(cur_path, new_path)

def get_ref_file_path_list():
    path_list = []

    ref_nodes = cmds.ls(type='reference')
    # ref_nodes = [ref for ref in ref_nodes if not ref.endswith("RN")]

    for ref in ref_nodes:
        if ref == 'sharedReferenceNode':
            continue
        reference_file_path = cmds.referenceQuery(ref, filename=True)
        path_list.append(reference_file_path)
    return path_list
        

def publisher_func():
    global win
    reload(publisher)
    win = publisher.Publisher(sg, "maya")
    win.show()

def review_func():
    global win
    reload(upload_review)
    win = upload_review.Review(sg, "maya")
    win.show()
    
def add_custom_menu():
    """
    마야의 메인 윈도우에 메뉴를 추가하는 함수 입니다.
    lambda 함수는 함수의 실행을 허용하지 않고, 이벤트가 발생했을때 함수를 실행시킵니다.
    """
    gMainWindow = mel.eval('$window=$gMainWindow')
    custom_menu = cmds.menu(parent=gMainWindow, tearOff = True, label = 'BAKED') 
    cmds.menuItem(label="Loader", parent=custom_menu, command=lambda *args: loader_func())
    cmds.menuItem(label="Save File", parent=custom_menu, command=lambda *args: save_func())
    cmds.menuItem(label="Publisher", parent=custom_menu, command=lambda *args: publisher_func())
    cmds.menuItem(label="Upload Review", parent=custom_menu, command=lambda *args: review_func())
    cmds.menuItem(label="Tracker", parent=custom_menu, command=lambda *args: tracker_func())

def _check_dir(external_path):
    # 외부 경로 안에 'maya' 폴더를 추가
    maya_project_dir = external_path.split("/maya/")[0] + "/maya"
    
    # 파일 시스템에서 경로의 존재 여부를 확인
    if not os.path.exists(maya_project_dir):
        os.makedirs(maya_project_dir) 
        print(f"Created Maya project directory at: {maya_project_dir}")

    # Maya 프로젝트 workspace 설정
    cmds.workspace(maya_project_dir, openWorkspace=True)
    print(f"Maya workspace set to: {maya_project_dir}")

    # 필요한 디렉토리 생성
    subdirectories = [
        "scenes", 
        "images", 
        "sourceimages", 
        "assets", 
        # "renderData", 
        # "clips", 
        # "sound", 
        "scripts", 
        "data", 
        "movies", 
        # "data", 
        # "Time Editor", 
        "autosave", 
        # "sceneAssembly"
    ]

    for subdir in subdirectories:
        dir_path = os.path.join(maya_project_dir, subdir)
        if not os.path.exists(dir_path):
            print(f"Checking directory: {dir_path}")  # 각 디렉토리 경로를 확인

            os.makedirs(dir_path)
            print(f"Created directory: {dir_path}")
        else:
            print(f"Directory already exists: {dir_path}")


save_win = save.SaveFile()
load_win = loader.Loader(sg, "maya")
tracker_win = file_tracker.Tracker(sg, get_ref_file_path_list(), load_win.related_tasks)

init()