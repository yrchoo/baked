# print ("*" * 30)
# print ("meny.py")
# print ("menu script is processed")
# print ("*" * 30)

# import maya.cmds as cmds
# import maya.mel as mel

# import sys
# import os
# from importlib import reload

# sys.path.append("/home/rapa/baked/toolkit/config/python")

# from shotgrid.get_shotgrid_data import Shotgrid_Data
# from load_scripts.maya_file_load import LoadMayaFile

# sg = Shotgrid_Data()

# import loader
# load_win = loader.Loader(sg, "maya")

# import save
# save_win = save.SaveFile()

# def init():
#     load_win.OPEN_FILE.connect(open_file)
#     save_win.SAVE_FILE.connect(save_file)

# def loader_func():
#     """
#     메뉴를 선언하는 함수보다 윗쪽에 이 코드를 적어주세요.
#     add_custom_menu보다 밑으로 내려가면 함수를 찾지 못해요~!
#     이 함수는 메뉴를 테스트하는 함수입니다.
#     """
#     ### 예린님 로더에 input값 연결해주기 ###
#     # reload(loader)
#     load_win.show()

# def open_file(path):
#     current_file_path = cmds.file(query=True, sceneName=True)
#     if current_file_path :
#         LoadMayaFile(path)
#     else :
#         current_file_path = path
#         cmds.file(path, open=True, force=True)

#     _check_dir(current_file_path)

# def save_file(path):
#     cmds.file(rename=path)
#     cmds.file(save=True, type='mayaBinary')
        

# def publisher_func():
#     global win
#     import publisher
#     reload(publisher)
#     win = publisher.Publisher()
#     # win.show()
    
# def add_custom_menu():
#     """
#     마야의 메인 윈도우에 메뉴를 추가하는 함수 입니다.
#     lambda 함수는 함수의 실행을 허용하지 않고, 이벤트가 발생했을때 함수를 실행시킵니다.
#     """
#     gMainWindow = mel.eval('$window=$gMainWindow')
#     custom_menu = cmds.menu(parent=gMainWindow, tearOff = True, label = 'BAKED') 
#     cmds.menuItem(label="Loader", parent=custom_menu, command=lambda *args: loader_func())
#     cmds.menuItem(label="Publisher", parent=custom_menu, command=lambda *args: publisher_func())

# def _check_dir(external_path):
#     # 외부 경로 안에 'maya' 폴더를 추가
#     maya_project_dir = os.path.join(os.path.dirname(external_path), "maya")

#     # 파일 시스템에서 경로의 존재 여부를 확인
#     if not os.path.exists(maya_project_dir):
#         os.makedirs(maya_project_dir) 
#         print(f"Created Maya project directory at: {maya_project_dir}")

#     # Maya 프로젝트 workspace 설정
#     cmds.workspace(maya_project_dir, openWorkspace=True)
#     print(f"Maya workspace set to: {maya_project_dir}")

#     # 필요한 디렉토리 생성
#     subdirectories = [
#         "scenes", 
#         "images", 
#         "sourceimages", 
#         "assets", 
#         "renderData", 
#         "clips", 
#         "sound", 
#         "scripts", 
#         "data", 
#         "movies", 
#         "data", 
#         "Time Editor", 
#         "autosave", 
#         "sceneAssembly"
#     ]

#     for subdir in subdirectories:
#         dir_path = os.path.join(maya_project_dir, subdir)
#         if not os.path.exists(dir_path):
#             print(f"Checking directory: {dir_path}")  # 각 디렉토리 경로를 확인

#             os.makedirs(dir_path)
#             print(f"Created directory: {dir_path}")
#         else:
#             print(f"Directory already exists: {dir_path}")


# init()

print ("*" * 30)
print ("menu.py")
print ("menu script is processed")
print ("*" * 30)


try: 
    import maya.cmds as cmds
    import maya.mel as mel
except:
    pass

import sys
sys.path.append("/home/rapa/baked/toolkit/config/python/")
sys.path.append("/home/rapa/baked/toolkit/config/python/shotgrid")


from fetch_shotgrid_data import ShotGridDataFetcher

from importlib import reload
import publisher

sg = ShotGridDataFetcher()

def test_func():
    global win
    
    reload(publisher)
    win = publisher.Publisher(sg, "maya")
    win.show()
    

def add_custom_menu():
    gMainWindow = mel.eval('$window=$gMainWindow')
    custom_menu = cmds.menu(parent=gMainWindow, tearOff = True, label = 'BAKED') 
    cmds.menuItem(label="Loader", parent=custom_menu, command='print("LOADER")')
    cmds.menuItem(label="Publisher", parent=custom_menu, command=lambda *args: test_func())