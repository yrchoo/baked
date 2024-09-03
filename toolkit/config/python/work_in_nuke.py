try:
    import os
    import json
    import subprocess
    import datetime
    import nuke
except: 
    pass
class NukeAPI():
    def __init__(self):
        pass
    
    def get_selected_write_nodes(self):
        """선택한 write node를 리스트로 가져오는 메서드"""
        nodes = nuke.selectedNodes()
        write_nodes = []
        for node in nodes:
            if node.Class() == 'Write': 
                write_node = node.knob("name").value()
                write_nodes.append(write_node)

        if not write_nodes:  
            print("there is no write nodes")
        return write_nodes
   
    def get_file_name(self):
        """현재 작업중인 파일 이름을 가져오는 메서드"""
        script_path = nuke.scriptName()
        # print (script_path)
        if script_path:
            script_name = os.path.basename(script_path)
            # print (script_name)
            return script_name
        else:
            return None
    
    def save_as_current_script(self, path, filename):
        """현재 스크립트를 저장하는 메서드"""
        if not path or not filename:
            return False
        try:
            file_path = os.path.join(path, filename)

            nuke.scriptSaveAs(file_path)
            return True
        except Exception as e:
            return False
        
    def render_selected_write_nodes_with_exr(self, start_frame, last_frame):
        """exr 포맷으로 렌더링을 해주는 메서드"""
        write_nodes = self.get_selected_write_nodes()
        start_frame = 1     # 테스트용으로 임의로 값을 지정했지만, input받은 값으로 지정할 예정이라 없애도 무방
        last_frame = 100

        if not write_nodes:
            return
        
        for write_node in write_nodes:
            nuke.execute(write_node, start_frame, last_frame)
            
