from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimediaWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QMainWindow
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QCamera, QCameraViewfinderSettings
from PyQt5.QtGui import QImage, QPixmap
from utils.torch_utils import select_device, time_sync
import sys
import pyautogui
import handpose
import multiprocessing
import math
import cv2
from PIL import Image
import time


class Ui_Map(object):
    def __init__(self):
        self.crop = None
        self.tolist = None
        self.item = None
        self.name = None
        self.verticalLayout = None
        self.View2 = None
        self.View1 = None
        self.gridLayout = None

    def setupUi(self, Map):
        Map.setObjectName("Map")
        Map.resize(1300, 900)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Map.sizePolicy().hasHeightForWidth())
        Map.setSizePolicy(sizePolicy)
        self.widget = QtWidgets.QWidget(Map)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1300, 1000))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.View1 = QWebEngineView(self.widget)
        self.View1.load(QUrl(r"file:///C:/Users/Administrator.LAPTOP-JR38EVVS/Desktop/yolov5/高德地图.html"))
        # self.View1.load(QUrl("https://www.amap.com/"))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.View1.sizePolicy().hasHeightForWidth())
        self.View1.setSizePolicy(sizePolicy)
        self.View1.setMinimumSize(QtCore.QSize(950, 1000))
        self.View1.setAutoFillBackground(True)
        self.View1.setObjectName("View1")
        self.horizontalLayout.addWidget(self.View1)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.View2 = QtWidgets.QWidget(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.View2.sizePolicy().hasHeightForWidth())
        self.View2.setSizePolicy(sizePolicy)
        self.View2.setMinimumSize(QtCore.QSize(350, 350))
        # self.View2.setAutoFillBackground(True)
        self.View2.setObjectName("View2")
        self.l1 = QtWidgets.QLabel(self.View2)
        self.l1.setMinimumSize(350, 350)
        self.l1.setAlignment(Qt.AlignCenter)
        self.l1.setMargin(25)
        png = QtGui.QPixmap("image.png")
        pngw = png.width()
        pngh = png.height()
        if pngw > pngh:
            png = png.scaledToWidth(300)
        else:
            png = png.scaledToHeight(300)
        
        self.l1.setPixmap(png)
        self.verticalLayout.addWidget(self.View2)
        # self.View2 = QCamera()
        # self.View2.setCaptureMode(QCamera.CaptureViewfinder)
        # viewCamera = QtMultimediaWidgets.QCameraViewfinder(self)
        # self.View2.setViewfinder(viewCamera)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.View2.sizePolicy().hasHeightForWidth())
        # self.View2.setSizePolicy(sizePolicy)
        # self.View2.setAutoFillBackground(True)
        # self.View2.setObjectName("View2")
        # self.gridLayout.addChildWidget(self.View2, 0, 1, 1, 1)

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.name = QtWidgets.QLabel(self.widget)
        self.name.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name.sizePolicy().hasHeightForWidth())
        self.name.setSizePolicy(sizePolicy)
        self.name.setMouseTracking(False)
        self.name.setAcceptDrops(False)
        self.name.setAutoFillBackground(False)
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name, 0, 0, 1, 1)
        
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMouseTracking(False)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.item = QtWidgets.QLabel(self.widget)
        self.item.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.item.sizePolicy().hasHeightForWidth())
        self.item.setSizePolicy(sizePolicy)
        self.item.setMouseTracking(False)
        self.item.setAcceptDrops(False)
        self.item.setAutoFillBackground(False)
        self.item.setObjectName("item")
        self.gridLayout.addWidget(self.item, 1, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setMouseTracking(False)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.tolist = QtWidgets.QLabel(self.widget)
        self.tolist.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tolist.sizePolicy().hasHeightForWidth())
        self.tolist.setSizePolicy(sizePolicy)
        self.tolist.setMouseTracking(False)
        self.tolist.setAcceptDrops(False)
        self.tolist.setAutoFillBackground(False)
        self.tolist.setObjectName("tolist")
        self.gridLayout.addWidget(self.tolist, 2, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy)
        self.lineEdit_3.setMouseTracking(False)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 2, 1, 1, 1)
        self.crop = QtWidgets.QLabel(self.widget)
        self.crop.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.crop.sizePolicy().hasHeightForWidth())
        self.crop.setSizePolicy(sizePolicy)
        self.crop.setMouseTracking(False)
        self.crop.setAcceptDrops(False)
        self.crop.setAutoFillBackground(False)
        self.crop.setObjectName("crop")
        self.gridLayout.addWidget(self.crop, 3, 0, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_4.sizePolicy().hasHeightForWidth())
        self.lineEdit_4.setSizePolicy(sizePolicy)
        self.lineEdit_4.setMouseTracking(False)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout.addWidget(self.lineEdit_4, 3, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Map)
        QtCore.QMetaObject.connectSlotsByName(Map)

    def retranslateUi(self, Map):
        _translate = QtCore.QCoreApplication.translate
        Map.setWindowTitle(_translate("Map", "掌中宝"))
        self.name.setText(_translate("Map", "类型"))
        self.lineEdit.setText(_translate("Map", my_type))
        self.item.setText(_translate("Map", "置信度"))
        self.lineEdit_2.setText(_translate("Map", con))
        self.tolist.setText(_translate("Map", "X"))
        self.lineEdit_3.setText(_translate("Map", X))
        self.crop.setText(_translate("Map", "Y"))
        self.lineEdit_4.setText(_translate("Map", Y))

    def retranslate(self):
        _translate = QtCore.QCoreApplication.translate
        self.lineEdit.setText(_translate("Map", my_type))
        self.lineEdit_2.setText(_translate("Map", str(con)))
        self.lineEdit_3.setText(_translate("Map", str(X)))
        self.lineEdit_4.setText(_translate("Map", str(Y)))
        # rgbimg = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        # disimg = QImage(rgbimg, rgbimg.shape[1], rgbimg.shape[0], QImage.Format_RGB888)
        # piximg = QPixmap(disimg)

        data = Image.fromarray(im)
        data.save('image.png')  
        self.l1.setPixmap(QtGui.QPixmap("image.png"))
        # self.l1.setPixmap(QtGui.QPixmap(piximg))


class Mywindow(QMainWindow, Ui_Map):
    def __init__(self, parent=None):
        super(Mywindow, self).__init__(parent)
        self.setupUi(self)

def mouse(result, conf, rect, img):
    global pre, ex
    global my_type
    global con, X, Y, im, t1
    my_type = result
    pyautogui.PAUSE = 0
    con = conf
    X = rect[0]
    Y = rect[1]
    W = rect[2]
    H = rect[3]
    im = img
    if conf > 0.5 and W > 100:
        t2 = time_sync()
        ex.retranslate()
        if result == "index_pointing_up":

            if pre != (0, 0, 0, 0):
                x = int(pre[0] + pre[2] / 2)
                y = int(pre[1] + pre[3] / 2)

                x_new = int(rect[0] + rect[2] / 2)
                y_new = int(rect[1] + rect[3] / 2)

                dis_x = x_new - x
                dis_y = y_new - y

                pyautogui.dragRel(dis_x/2,dis_y/2, duration=0)  # 鼠标拖动

                pyautogui.moveRel(-dis_x/2,-dis_y/2, duration=0)  # 复原鼠标位置
            else:
                pre = rect

        if result == "hand_with_fingers_splayed" and t2 - t1 > 1:
            print(t2)
            t1 = t2
            # pyautogui.scroll(200)  # 向上滚动200  放大
            pyautogui.press('=')

        if result == "raised_fist" and t2 - t1 > 1:
            print(t2)
            t1 = t2
            pyautogui.press('-')
            # pyautogui.scroll(-200)  # 向下滚动200  缩小
            # time.sleep(2)


# def hand_pose():


    


pre = (0, 0, 0, 0)
my_type = " 1"
con = " 2"
X = " 3"
Y = " 4"
im = " "
t1 = 0
# if __name__ == '__main__':
# map_process = multiprocessing.Process(target=my_map, args=())

# map_process.start()
app = QApplication(sys.argv)
ex = Mywindow()
ex.show()
# handpose_process = multiprocessing.Process(target=hand_pose, args=())
# handpose_process.start()
hd = handpose.Handpose(handpose.WEIGHTS_PATH, handpose.DATA_PATH, handpose.IMAGE_SIZE)
hd.detectFromCamera(mouse)
# sys.exit(app.exec())
# map_process.join()
# handpose_process.join()
# my_map()
# hand_pose()