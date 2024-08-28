try:
    from PySide6.QtCore import Qt, QRect
    from PySide6.QtGui import QPainter
    from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
except:
    from PySide2.QtCore import Qt, QRect
    from PySide2.QtGui import QPainter
    from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

import sys


class SubWindow_Open(QWidget):
   """
   엄... 이게 마우스가 드래그 되는 부분이 위젯 범위를 넘어가면
   드래그 되는 영역에 대한 페인트가 칠해지지 않아서,
   투명 위젯 클래스를 추가하였음.
   이렇게 하니 드래그 영역 페인트를 잘 칠해줌.
   """
   def __init__(self):
       super().__init__()
       self.start_pos = None
       self.end_pos = None

       QApplication.setOverrideCursor(Qt.CrossCursor) # 커서 오버라이드
       self.setWindowFlag(Qt.FramelessWindowHint) # 투명 윈도우인데 위에 제목표시줄 있으면 안되서 지우는 부분
       self.setWindowOpacity(0.3) # 윈도우 투명도 0.3
       self.setAttribute(Qt.WA_TranslucentBackground) # 투명도를 쓰겠다는 명령어
       self.showFullScreen() # 풀스크린 위젯

   def mousePressEvent(self, event):
       """
       마우스를 눌렀을때 발생하는 이벤트
       """
       if event.button() == Qt.LeftButton:
           self.start_pos = event.pos()
           self.end_pos = self.start_pos
           self.update()
  
   def mouseMoveEvent(self, event):
       """
       마우스를 움직일때 발생하는 이벤트 
       """
       if self.start_pos:
           self.end_pos = event.pos()
           self.update()


   def mouseReleaseEvent(self, event):
       """
       마우스 왼쪽 버튼을 땟을때 발생하는 이벤트
       """
       if event.button() == Qt.LeftButton:
           self.end_pos = event.pos()
           self.capture_screen()
           QApplication.restoreOverrideCursor()
           self.start_pos = None
           self.end_pos = None
           self.close()


   def paintEvent(self, event):
       """
       마우스가 드래그되는 곳에 사각형 그려주는 페인트 메서드
       """
       if self.start_pos and self.end_pos:
           rect = QRect(self.start_pos, self.end_pos)
           painter = QPainter(self)
           painter.setPen(Qt.white)
           painter.drawRect(rect)


   def capture_screen(self):
       """
       실제로 화면을 캡쳐하는 메서드
       """
       if self.start_pos and self.end_pos:
           x = min(self.start_pos.x(), self.end_pos.x())
           y = min(self.start_pos.y(), self.end_pos.y()) # X, Y는 드래그된 마우스 포인터의 좌상단 좌표
           w = abs(self.start_pos.x() - self.end_pos.x()) # 드래그 시작점과 끝점의 X 좌표간의 차이
           h = abs(self.start_pos.y() - self.end_pos.y()) # W, H는 드래그된 마우스 포인터의 가로와 세로 길이
           screen = QApplication.primaryScreen()
           screenshot = screen.grabWindow(0, x, y, w, h) # window 인덱스? 몰라, x

           screenshot.save("/home/rapa2/screen_capture/capture_kk.jpg", "jpg", quality=100)


class MakeScreenCapture(QWidget):
   def __init__(self):
       super().__init__()
       self.setWindowTitle("hello")
       self.setGeometry(100, 100, 300, 200)

       self.capture_button = QPushButton("찰칵", self)
       self.capture_button.clicked.connect(self.start_capture_mode)

       layout = QVBoxLayout()
       layout.addWidget(self.capture_button)
       self.setLayout(layout)

   def start_capture_mode(self):
       self.hide()
       

       self.overlay = SubWindow_Open()
       self.overlay.show()

if __name__ == "__main__":
   app = QApplication(sys.argv)
   window = MakeScreenCapture()
   window.show()
   sys.exit(app.exec())