try:
    import os
    import json
    import subprocess
    import datetime
    import nuke
except: 
    pass
    
def get_selected_write_nodes(): 
    """선택한 write node를 리스트로 가져오는 메서드"""
    nodes = nuke.selectedNodes()
    write_nodes = []
    if len(nodes) == 1:
        node = nodes[0]
        if node.Class() == 'Write': 
            write_node = node.knob("name").value()
            write_nodes.append(write_node)

    if not write_nodes:  
        print("there is no write nodes")
    return write_nodes

def get_file_name():
    """현재 작업중인 파일 이름을 가져오는 메서드"""
    script_path = nuke.scriptName()
    # print (script_path)
    if script_path:
        script_name = os.path.basename(script_path)
        # print (script_name)
        return script_name
    else:
        return None
    
def save_file(path):
    nuke.scriptSaveAs(path)

def save_as_current_script(path, filename):
    """현재 스크립트를 저장하는 메서드"""
    if not path or not filename:
        return False
    try:
        file_path = os.path.join(path, filename)
        nuke.scriptSaveAs(file_path)
        return True
    except Exception as e:
        return False
    
def render_selected_write_nodes_with_exr(start_frame, last_frame): # 프레임 값을 굳이 받아올 필요는 없을 것 같아영*****
    """exr 포맷으로 렌더링을 해주는 메서드"""
    write_node = get_selected_write_nodes()[0]
    start_frame = nuke.root().knob("first_frame").value() 
    last_frame = nuke.root().knob("last_frame").value()

    if not write_node:
        return

    nuke.execute(write_node, float(start_frame), float(last_frame), incr=1)
        
