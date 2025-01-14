from PyQt6.QtWidgets import QMainWindow,QApplication,QLabel,QStatusBar,QToolBar,QColorDialog,QFileDialog
from PyQt6.QtGui import QPixmap,QPainter,QPen,QAction,QIcon
from PyQt6.QtCore import Qt,QPoint,QRect,QSize  # this class (qt) has all the colour which is known as Qcolours and is mostly used by fill method 
import sys 
import os # used because we have to save a file in a path so os is used
class Canvas(QLabel):   # label is used for both writing and painting
    def __init__(self,parent):
     super().__init__(parent)
     self.parent=parent
     self.initUI()
    def initUI(self):
       self.pixmap=QPixmap(600,600)
       self.pixmap.fill(Qt.GlobalColor.white)
       self.setPixmap(self.pixmap)
       self.setMouseTracking(True)
       self.drawing=False  # this is set to false because when we enter the app we dont want the cursor drawing on the canvas
       self.last_mouse_position=QPoint()
       self.status_label=QLabel()
       self.eraser=False
       self.pen_color=Qt.GlobalColor.black
       self.pen_width=1
# event means mouse is moving or stoping or etc its for capturing event 
    def mouseMoveEvent(self,event): #when we move the mouse this event is triggered
        mouse_position=event.pos() # this gives the position of the mouse
        status_text=f"Mouse coordinates are:{mouse_position.x(),mouse_position.y}"
        self.status_label.setText(status_text)
        self.parent.statusbar.addWidget(self.status_label)
        if(event.buttons() and Qt.MouseButton.LeftButton ) and self.drawing:# event.buttons means if button is clicked 
            # draw something
            self.draw(mouse_position)
        print(mouse_position)
        
    def mousePressEvent(self,event):
        if event.button()==Qt.MouseButton.LeftButton:
            self.last_mouse_position=event.pos()
            self.drawing=True  # once the mouse is pressed then the drawing is set to true 
            print("Left click at position:"+str(event.pos()))
        
    def mouseReleaseEvent(self,event): 
        if event.button()==Qt.MouseButton.LeftButton:
            self.drawing=False
            print("mouse released at positon:"+str(event.pos()))

    def draw(self,points): # these are the point where pixels will be drawn 
        painter=QPainter(self.pixmap)
        if self.eraser==False:

            
            pen=QPen(self.pen_color,self.pen_width)  # 5 is the thickness of the pen
            painter.setPen(pen)   

            painter.drawLine(self.last_mouse_position,points)  # last mouse positon is the 1st positon and points is the last positon 
            self.last_mouse_position=points # then from above points will become 1st positon points and it is assigned to last mouse positon
            
        elif self.eraser==True:
            eraser=QRect(points.x(),points.y(),12,12)  
            painter.eraseRect(eraser)  
        self.update()
    def paintEvent(self,event):
        painter=QPainter(self)
        target_rect=QRect()
        target_rect=event.rect()
        painter.drawPixmap(target_rect,self.pixmap,target_rect)
        painter.end()
    def selecttool(self,tool):
        if tool=="pencil":
            self.pen_width=2
            self.eraser=False
        elif tool=="marker":
            self.pen_width=4
            self.eraser=False
        elif tool=="eraser":
            self.eraser=True    
        elif tool=="color":
            self.eraser=False
            color=QColorDialog.getColor()     # this gives the wagon of colors 
            self.pen_color=color  
    def new(self):
        self.pixmap.fill(Qt.GlobalColor.white)
        self.update()
    def save (self):
        file_name,_=QFileDialog.getSaveFileName(self,"Save As",os.path.curdir+"Sample.png","PNG FILE(*.png)")
        if file_name:
            self.pixmap.save(file_name,"png")

class MainWindow(QMainWindow):
    def __init__(self):
      
      super().__init__()
      self.initUI()
    def initUI(self):
        self.setMinimumSize(600,600)
        self.setWindowTitle("Paint App")
        #creating a canvas
        canvas=Canvas(self)
        self.setCentralWidget(canvas)
        self.statusbar=QStatusBar()
        self.setStatusBar(self.statusbar)
        #adding a toolbar
        tool_bar=QToolBar("Toolbar")
        tool_bar.setIconSize(QSize(24,24))
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea,tool_bar)  # this sets toolbar to the top of the window 
        tool_bar.setMovable(False) # this will not let the toolbar to move 
        pencil_act=QAction(QIcon("icons/pencil.png"),"Pencil",tool_bar)
        pencil_act.triggered.connect(lambda:canvas.selecttool("pencil"))
        marker_act=QAction(QIcon("icons/brush.png"),"Marker",tool_bar)
        marker_act.triggered.connect(lambda:canvas.selecttool("marker"))
        eraser_act=QAction(QIcon("icons/eraser.png"),"Eraser",tool_bar)
        eraser_act.triggered.connect(lambda:canvas.selecttool("eraser"))
        color_act=QAction(QIcon("icons/colors.png"),"Colors",tool_bar)
        color_act.triggered.connect(lambda:canvas.selecttool("color")) 

        tool_bar.addAction(pencil_act)
        tool_bar.addAction(marker_act)
        tool_bar.addAction(eraser_act)
        tool_bar.addAction(color_act)

        self.new_act=QAction("New")
        self.new_act.triggered.connect(canvas.new)
        self.save_file_act=QAction("Save")
        self.save_file_act.triggered.connect(canvas.save)
        self.quit_act=QAction("Exit")
        self.quit_act.triggered.connect(self.close)

        self.menuBar().setNativeMenuBar(True)
        file_menu=self.menuBar().addMenu("File")
        file_menu.addAction(self.new_act)
        file_menu.addAction(self.save_file_act)
        file_menu.addAction(self.quit_act)
         

app=QApplication(sys.argv)
window=MainWindow()
window.show()
app.exec()