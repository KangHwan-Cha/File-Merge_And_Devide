#!/usr/bin/python3
#-*- coding: utf-8 -*-
# ref: https://github.com/2minchul/PyQt5-Examples/blob/master/%5BPyQt5%5D%20get%20filepath%20by%20Drag%26Drop/app.py

import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from abc import ABC, abstractmethod


class DropWidget(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(DropWidget, self).__init__(parent)
        self.setWindowTitle("title")
        self.resize(720,480)
        self.setAcceptDrops(True)

    @abstractmethod
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    @abstractmethod
    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            print(f)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = DropWidget()
    MainWindow.show()
    sys.exit(app.exec_())