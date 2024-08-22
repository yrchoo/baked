print ("*" * 30)
print ("menu.py")
print ("menu script is processed")
print ("*" * 30)

import maya.cmds as cmds
import maya.mel as mel

import sys
from importlib import reload

sys.path.append("/home/rapa/baked/toolkit/config/python")

def loader_func():
    """
    메뉴를 선언하는 함수보다 윗쪽에 이 코드를 적어주세요.
    add_custom_menu보다 밑으로 내려가면 함수를 찾지 못해요~!
    이 함수는 메뉴를 테스트하는 함수입니다.
    """
    ### 예린님 로더에 input값 연결해주기 ###
    global win
    import loader
    reload(loader)
    win = loader.Loader(Shotgrid_Data)
    win.show()

def publisher_func():
    global win
    import publisher
    reload(publisher)
    win = publisher.Publisher()
    # win.show()
    
def add_custom_menu():
    """
    마야의 메인 윈도우에 메뉴를 추가하는 함수 입니다.
    lambda 함수는 함수의 실행을 허용하지 않고, 이벤트가 발생했을때 함수를 실행시킵니다.
    """
    gMainWindow = mel.eval('$window=$gMainWindow')
    custom_menu = cmds.menu(parent=gMainWindow, tearOff = True, label = 'BAKED') 
    cmds.menuItem(label="Loader", parent=custom_menu, command=lambda *args: loader_func())
    cmds.menuItem(label="Publisher", parent=custom_menu, command=lambda *args: publisher_func())