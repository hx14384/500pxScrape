#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

This program creates the first SubWindow which handle one picture in one time.

Author: JeffXu
Last edited: Feb 2019
"""

from PyQt5.QtWidgets import (QFrame, QLabel, QLineEdit, 
    QTextEdit, QGridLayout, QVBoxLayout, QHBoxLayout,
                             QApplication, QPushButton)

from PyQt5.QtCore import (QThread, QObject, pyqtSignal)

import FileDialog
import sys
sys.path.append('./Util/')
#print(sys.path)
import BaseUtil
sys.path.append('./Ctrller/')
import SingleCtrller
import OverlayLoading
import sys
import time

class SubFrame(QFrame):

    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.fileDialog = mainWindow.fileDialog
        self.initUI()
        
        def onDesPathSave(desPath):
            print(desPath)
            self.outputDesEdit.setText(desPath)
            #need to add suffix if "desPath" dose not contain it!
        self.onDesPathSave = onDesPathSave
        self.ctrller = SingleCtrller.Ctrller()
        self.scrape_thread = SubFrame.Start2ScrapeThread(self.ctrller)
        #self.scrape_thread .finished.connect(self.onSuccess)
        self.scrape_thread.expSignal.connect(self.onException)
        self.scrape_thread.successSignal.connect(self.onSuccess)
        
    def initUI(self):               
        
        picId = QLabel('图片ID')
        outputDes = QLabel('输出地址')
        self.startButton = QPushButton("开始")
        self.startButton.clicked.connect(self.onStartBtnClick)
        #self.startButton.setEnabled(False)
        fileLogButton = QPushButton("...")
        fileLogButton.clicked.connect(self.onFileLogBtnClick)

        self.picIdEdit = QLineEdit()
        self.outputDesEdit = QLineEdit()

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.setVerticalSpacing(10)

        grid.addWidget(picId, 1, 0)
        grid.addWidget(self.picIdEdit, 1, 1)

        grid.addWidget(outputDes, 2, 0)
        grid.addWidget(self.outputDesEdit, 2, 1, 3, 1)
        grid.addWidget(fileLogButton, 2, 2)

        grid.setRowStretch(3, 1)

        self.loading = OverlayLoading.Window()
        self.loading.hide()
       
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.startButton)
        hbox.addStretch(1)
        
        vbox = QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addWidget(self.loading)
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.show()

        self.setDefaultVal()

    def setDefaultVal(self):
        self.outputDesEdit.setText("./output.xlsx")
        self.picIdEdit.setText("")

    def onFileLogBtnClick(self):
        self.fileDialog.showSaveFileDialog(self.onDesPathSave)

    class Start2ScrapeThread(QThread):
        expSignal = pyqtSignal(str)
        successSignal = pyqtSignal()

        def __init__(self, ctrller):
            QThread.__init__(self)
            self.ctrller = ctrller

        def __del__(self):
            self.wait()

        def run(self):
            try:          
                self.ctrller.start2Scrape()
            except BaseException as e:
                self.expSignal.emit(str(e));
            else:
                self.successSignal.emit();
                
            

    def onStartBtnClick(self):
        
        photoId = self.picIdEdit.text().strip()
        outputPath = BaseUtil.ensureXlSuffix(self.outputDesEdit.text().strip())
        if photoId == "" or outputPath == "":
            self.mainWindow.popUpMessageBox(False, "照片ID或输出地址不可为空")
            return
        self.loading.show()
        self.setEnabled(False)
        self.ctrller.setPhotoId(photoId)
        self.ctrller.setOutputPath(outputPath)          
        self.scrape_thread.start()
        
        #start2Scrape()

    def onSuccess(self):    
        self.loading.hide()
        self.setEnabled(True)
        self.mainWindow.popUpMessageBox(True, "爬取成功")

    def onException(self, e):
        self.loading.hide()
        self.setEnabled(True)
        self.mainWindow.popUpMessageBox(False, "异常: {0}".format(e))
