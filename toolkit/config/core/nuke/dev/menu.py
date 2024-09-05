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

baked_menu.addCommand("Loader", baked_pipeline_script.show_loader, "Alt+L")
baked_menu.addCommand("Save File", baked_pipeline_script.pop_save_file_ui, "Alt+S")
baked_menu.addCommand("Publisher", baked_pipeline_script.show_publisher)
baked_menu.addCommand("Upload Review", baked_pipeline_script.show_review)
baked_menu.addCommand("Tracker", baked_pipeline_script.show_tracker, "Alt+T")

############## 노드를 생성해주는 메뉴

menu_bar = nuke.menu("Nuke")
node_menu = menu_bar.addMenu("Nodes")
node_menu.addCommand("Lens Distortion Node", baked_pipeline_script.create_undistortion_node)


# Callback
nuke.addOnCreate(baked_pipeline_script.set_write_node_path, nodeClass='Write')
nuke.addOnScriptSave(baked_pipeline_script.set_write_node_path)
nuke.addOnScriptLoad(baked_pipeline_script.setup_nuke_project)