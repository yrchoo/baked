print("*" * 30)
print ("baked_menu.py")
print("Menu Script is executed.")
print("*" * 30)


import nuke
from python import baked_pipeline_script

menu_bar = nuke.menu("Nuke")
baked_menu = menu_bar.addMenu("BAKED MENU")

# menu.addCommand(메뉴 라벨(이름), 명령어, 바로가기, 순서) 뒤에 두 개는 생략 가능
# menu_4th.addCommand("hello world", pipeline_script.test_func, "F8")

baked_menu.addCommand("Load Files", baked_pipeline_script.show_loader)