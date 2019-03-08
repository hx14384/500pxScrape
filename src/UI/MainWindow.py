#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

This program creates the main Window.

Author: JeffXu
Last edited: Feb 2019
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QAction, qApp,
                             QApplication, QVBoxLayout, QMessageBox)

import SingleSubWindow
import FileDialog
#sys.path.append('./UI/')
#import OverlayLoading

class Window(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()     
        self.fileDialog = FileDialog.Widget()
        #self.fileDialog.hide()
        self.addFrame(0, SingleSubWindow.SubFrame(self))
        
    def initUI(self):               
        
        singleAct = QAction('单张', self)
        #singleAct.triggered.connect(???)

        #multiAct = QAction('多张', self)
        #multiAct.triggered.connect(qApp.quit)
        
        self.toolbar = self.addToolBar('单张')
        self.toolbar.addAction(singleAct)
        #self.toolbar = self.addToolBar('多张')
        #self.toolbar.addAction(multiAct)   
        
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('500pxScraping')    
        self.show()

    def addFrame(self, index, frame):
        self.setCentralWidget(frame)

    def popUpMessageBox(self, flag, text):
        if flag:
            QMessageBox.information(self, "成功", text)
        else:
            QMessageBox.critical(self, "失败", text)
"""        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    mWindow = Window()
    mWindow.addFrame(0, SingleSubWindow.SubFrame())
    sys.exit(app.exec_())
"""
