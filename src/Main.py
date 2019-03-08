#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

This is the entrance.

Author: JeffXu
Last edited: Feb 2019
"""
from PyQt5.QtWidgets import QApplication

import sys
sys.path.append('./UI/')
import MainWindow

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    mWindow = MainWindow.Window()
    sys.exit(app.exec_())
    
