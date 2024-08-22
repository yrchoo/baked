import maya.cmds as cmds
import maya.mel as mel

def test_func(text):
    """
    메뉴를 선언하는 함수보다 윗쪽에 이 코드를 적어주세요.
    add_custom_menu보다 밑으로 내려가면 함수를 찾지 못해요~!
    이 함수는 메뉴를 테스트하는 함수입니다.
    """
    print ("test menu1 action")
    print (text)
    import PySide2
    print (PySide2)

def add_custom_menu():
    """
    마야의 메인 윈도우에 메뉴를 추가하는 함수 입니다.
    lambda 함수는 함수의 실행을 허용하지 않고, 이벤트가 발생했을때 함수를 실행시킵니다.
    """
    gMainWindow = mel.eval('$window=$gMainWindow')
    custom_menu = cmds.menu(parent=gMainWindow, tearOff = True, label = '4th Academy') 
    cmds.menuItem(label="Hello menu1", parent=custom_menu, command=lambda *args: test_func("여러분 힘내요."))
    cmds.menuItem(label="Hello menu2", parent=custom_menu, command="print('Helloworld22')")
