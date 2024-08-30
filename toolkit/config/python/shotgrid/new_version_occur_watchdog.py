import time
import json

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

try:
    from PySide6.QtCore import Signal, QObject
except:
    from PySide2.QtCore import Signal, QObject

class VersionUpdateHandler(FileSystemEventHandler):
    def __init__(self, observer):
        super().__init__()
        self.observer = observer
        

    def on_created(self, event):
        # 새 파일이 생성될 때 호출됨
        if event.is_directory:
            return
        
        if event.src_path.endswith('.json'):
            # json 파일인 경우에만 처리
            try:
                with open(event.src_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.observer.NEW_FILE_OCCUR.emit(data)
            except Exception as e:
                print(f"Error reading JSON file : {e}")

class VersionUpdateObserver(QObject):
    NEW_FILE_OCCUR = Signal(dict)

    def __init__(self, dir_path):
        super().__init__()
        self.start_observer(dir_path)

    def start_observer(self, dir_path):
        observer = Observer()
        observer.schedule(VersionUpdateHandler(self), dir_path, recursive=False)

        observer.daemon = True
        observer.start()
        print(f"Monitoring directory : {dir_path}")
