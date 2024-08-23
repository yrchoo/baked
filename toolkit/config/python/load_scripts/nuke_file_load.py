try :
    import nuke
except :
    print("import nuke failed...")

class LoadNukeFile():
    def __init__(self, path):
        self._make_read_node(path)

    def _make_read_node(self, path):
        try :
            read_node = nuke.createNode("Read")
            read_node.knob("file").setValue(path)
        except :
            print("nuke에서 제대로 동작하지 않음")
        
