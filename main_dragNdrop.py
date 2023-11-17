#!/usr/bin/python3
#-*- coding: utf-8 -*-
#
# FileMergeNDivide - ver 0.1

import os
import sys
import json
import time
import shutil
import subprocess
from abc import ABC, abstractmethod

from pathlib import Path
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QProgressBar, QMessageBox,
                            QTableWidget, QTableWidgetItem)


class MainWidget(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.setWindowTitle("Title")
        self.resize(720,480)
        self.setAcceptDrops(True)
        self.statusBar().showMessage('Ready')

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    @abstractmethod
    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            print(f, '\n\n')


class FileMergeNDivide(MainWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("File Merge & Divide")
        icon = QtGui.QIcon('./ico/pastel_note.ico')  # 아이콘 파일 경로
        self.setWindowIcon(icon)

        self.setAcceptDrops(True)
        self.item_list = []
        self.dir_list = []
        self.file_list = []
        self.unuse_list = []
        self.dupli_list = []
        self.DESTINATION = dict()

        italic_font = QtGui.QFont()
        italic_font.setItalic(True)

        self.push_sht_style = "background-color: black; color: yellow;"
        self.pull_sht_style = "background-color: window; color: black;"

        # 상태 표시줄에 상태 표시 레이블 추가
        self.status_label = QtWidgets.QLabel("ver - 0.2", self)
        self.statusBar().addPermanentWidget(self.status_label)

        # 하단 툴바에 Combine, Divide, Clear 버튼 추가
        self.toolbar = self.addToolBar("toolbar")
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolbar)

        combine_button = QtWidgets.QPushButton("Combine", self)
        combine_button.clicked.connect(self.combine_files)
        self.toolbar.addWidget(combine_button)

        divide_button = QtWidgets.QPushButton("Divide", self)
        divide_button.clicked.connect(self.divide_files)
        self.toolbar.addWidget(divide_button)

        # 구분자 추가
        for _ in range(1):
            self.toolbar.addSeparator()

        drm_ch_button = QtWidgets.QPushButton("DRM Filter", self)
        drm_ch_button.clicked.connect(self.drm_check)
        self.toolbar.addWidget(drm_ch_button)

        # 구분자 추가
        for _ in range(5):
            self.toolbar.addSeparator()

        # clear_button 생성 및 글자색 입히기
        clear_button = QtWidgets.QPushButton("Clear", self)
        clear_button.setStyleSheet("color: blue")
        clear_button.clicked.connect(self.initialized_self_list)
        self.toolbar.addWidget(clear_button)

        browse_button = QtWidgets.QPushButton("Set path", self)
        browse_button.setGeometry(10, 10, 80, 20)
        browse_button.clicked.connect(self.browse_folder)
        self.toolbar.addWidget(browse_button)

        # save_button 생성
        save_button = QtWidgets.QPushButton("Save", self)
        save_button.clicked.connect(self.save_dict_to_json)
        self.toolbar.addWidget(save_button)
        
        # load_button 생성
        load_button = QtWidgets.QPushButton("Load", self)
        load_button.clicked.connect(self.load_dict_from_json)
        self.toolbar.addWidget(load_button)

        # 구분자 추가
        for _ in range(5):
            self.toolbar.addSeparator()

        exit_button = QtWidgets.QPushButton("Exit", self)
        exit_button.clicked.connect(self.close)
        self.toolbar.addWidget(exit_button)
        
        help_button = QtWidgets.QPushButton("Help", self)
        help_button.clicked.connect(self.save_html_file)
        self.toolbar.addWidget(help_button)

        test_button = QtWidgets.QPushButton("Test", self)
        test_button.clicked.connect(self.test)
        self.toolbar.addWidget(test_button)

        # inputbox와 test_button 생성하기
        self.input_box = QtWidgets.QLineEdit(self)
        self.input_box.setPlaceholderText \
            (" -- 합쳐질 폴더를 선택(Set path)하거나 경로를 붙여(ctrl+v) 넣으세요 -- ")
        # self.input_box.setFont(italic_font)

        # Title widget 추가
        self.title_widget = QtWidgets.QLabel(self)
        self.title_widget.setText("File List")
        self.title_widget.setAlignment(QtCore.Qt.AlignCenter)


        # list_widget 생성하기
        self.list_widget = QtWidgets.QListWidget(self)
        # self.list_widget.setDragEnabled(True)  # 다중 선택 문제떄문에..
        self.list_widget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.list_widget.itemDoubleClicked.connect(self.open_path)
        self.list_widget.itemChanged.connect(self.update_title_widget)
        # -- 주석 처리 -- 
        self.list_widget.addItem("옮기려는 폴더를 드래그 앤 드롭하세요!")
        item = self.list_widget.item(0)
        item.setFont(italic_font)


        # 위젯들을 수직으로 쌓을 수 있는 QVBoxLayout 생성
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.input_box)
        layout.addWidget(self.title_widget)
        layout.addWidget(self.list_widget)

        # QMainWindow의 중앙 위젯으로 레이아웃 설정
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)
            
    def update_title_widget(self):
        count = self.list_widget.count()
        if count >= 1:
            if self.list_widget.item(0).text(). \
                    startswith("옮기려는 폴더를"):
                return False
            else:
                count = self.list_widget.count()
                dupli_count = len(self.dupli_list)
                if dupli_count >= 1:
                    self.title_widget.setText(f"File List ({count}) - ▶중복 파일 수 : {dupli_count}")
                else:
                    self.title_widget.setText(f"File List ({count})")
        else:   # 개수가 없는 경우
            self.title_widget.setText(f"File List")
        return True
    
    def _origin_to_combine_dic(self):
        if self.input_box.text() == '':
            self.browse_folder()
        if self.input_box.text() == '':
            return False
        
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            origin_path = item.text()
            combin_path = self.input_box.text()
            self.DESTINATION[origin_path] = combin_path
        return True
    
    def combine_files(self):
        # 예외처리
        if self.list_widget.count() == 0:
            return False
        self._origin_to_combine_dic()
        if len(self.DESTINATION) == 0:
            self.statusBar().showMessage("합치는데에 실패했습니다")
            return False
            
        # progress_bar = QProgressBar()
        # progress_bar.setMaximum(0)
        # progress_bar.setMinimum(0)
        # progress_bar.show()
        # progress_bar.setGeometry(0, 0, self.width(), 20)
        # progress_bar.move(self.width()/2 - progress_bar.width()/2, self.height()/2 - progress_bar.height()/2)

        failed_files = []
        for src_path, dest_path in self.DESTINATION.items():
            try:
                shutil.move(src_path, dest_path)
            except (FileNotFoundError, PermissionError, shutil.SameFileError, shutil.Error, Exception) as e:
                print(f"An error occurred while copying {src_path}: {e}")
                failed_files.append(src_path)

        if len(failed_files) == 0:
            self.statusBar().showMessage("모든 파일을 합쳤습니다")
        else:
            message = f"{len(failed_files)}개 파일을 합치지 못했습니다"
            self.statusBar().showMessage(message)

        # Combine 버튼은 toolbar 안에서 첫 번째 버튼이므로 인덱스 0
        combine_button = self.toolbar.findChildren(QtWidgets.QPushButton)[0]
        combine_button.setStyleSheet(self.push_sht_style)
        combine_button = self.toolbar.findChildren(QtWidgets.QPushButton)[1]
        combine_button.setStyleSheet(self.pull_sht_style)
        return True

    def divide_files(self):
        self._origin_to_combine_dic()
        failed_files = []
        for dest_path, src_path in self.DESTINATION.items():
            # 아래 코드가 combine_files와 다른점 ★★★
            # # src_path는 combine했던 경로만 있기 때문에!
            src_path = os.path.join(src_path, os.path.basename(dest_path))
            try:
                shutil.move(src_path, dest_path)
            except Exception:
                failed_files.append(src_path)

        if len(failed_files) == 0:
            self.statusBar().showMessage("모든 파일을 분할하였습니다")
        else:
            message = f"{len(failed_files)}개 파일을 분할하지 못했습니다"
            self.statusBar().showMessage(message)
        # Combine 버튼은 toolbar 안에서 첫 번째 버튼이므로 인덱스 0
        combine_button = self.toolbar.findChildren(QtWidgets.QPushButton)[1]
        combine_button.setStyleSheet(self.push_sht_style)
        combine_button = self.toolbar.findChildren(QtWidgets.QPushButton)[0]
        combine_button.setStyleSheet(self.pull_sht_style)
        return True

    def drm_check(self):
        total = self.list_widget.count()
        items = list()
        for _ in range(0, total):
            items.append(self.list_widget.item(0).text())
            self.list_widget.takeItem(0)

        is_drm_list = list()
        for item in items:
            with open(item, 'rb') as f:
                try:
                    line = str(f.readline())
                    if "drm" in line.lower():
                        is_drm_list.append(item)
                except:
                    print(f"Failed: {item}")
        for drm_file in is_drm_list:
            self.list_widget.addItem(drm_file)

        self.update_title_widget()
        return True

    def initialized_self_list(self):
        self.item_list = []
        self.dir_list = []
        self.file_list = []
        self.unuse_list = []
        self.dupli_list = []
        self.DESTINATION = dict()
        self.title_widget.setText("File List")
        self.input_box.clear()
        self.clear_list_widget()

    def clear_list_widget(self):
        self.list_widget.clear()

    def browse_folder(self):
        folder_path = QtWidgets.QFileDialog. \
                    getExistingDirectory(self, "합쳐지기 위한 폴더를 선택하세요")
        self.input_box.setText(folder_path)
        return True

    def open_path(self, item):
        path: str
        path = item.text()
        # if os.path.exists()
        if os.path.isdir(path):
            os.startfile(path)
        else:
            os.startfile(os.path.dirname(path))

    def cre_time(self):
        now_time = time.strftime('%Y-%m-%d_%H%M%S')
        return now_time

    def save_dict_to_json(self):
        self._origin_to_combine_dic()
        # 현재 destination dict를 json 파일로 저장하기
        defulat_filename = self.cre_time()
        filename, _ = QtWidgets.QFileDialog. \
                    getSaveFileName(self, "Save JSON file", \
                    defulat_filename, "JSON Files (*.json)")
        if filename:
            with open(filename, "w") as f:
                json.dump(self.DESTINATION, f, indent=4)
    
    def load_dict_from_json(self):
        self.initialized_self_list()
        # JSON 파일을 불러와서 dict에 저장하기
        filename = ""
        filename, _ = QtWidgets.QFileDialog.getOpenFileName \
            (self, "Load JSON file", "", "JSON Files (*.json)")
        if filename:
            with open(filename, "r") as f:
                self.DESTINATION = json.load(f)
            self.statusBar().showMessage("JSON file loaded successfully.")
        else:
            self.statusBar().showMessage("JSON file loading was canceled.")
        self.add_keys_to_list_widget()
        self.list_widget_colored()

    def add_keys_to_list_widget(self):
        self.list_widget.clear()
        for key in self.DESTINATION.keys():
            item = QtWidgets.QListWidgetItem(key)
            self.list_widget.addItem(item)

    def test(self):
        self.list_widget.addItem("Testing...")
        count = self.list_widget.count()
        self.list_widget.item(0).setForeground(QtGui.QColor("blue"))

        pass
        
    def is_directory_or_file(self, path):
        if os.path.isdir(path):
            return "directory"
        elif os.path.isfile(path):
            return "file"
        else:
            return "not found"

    def dropEvent(self, event):
        if self.list_widget.count() >= 1:
            if self.list_widget.item(0).text().startswith("옮기려는"):
                self.list_widget.takeItem(0)
        drop_items = [u.toLocalFile() for u in event.mimeData().urls()]
        dir_temp = []
        for item in drop_items:
            item_type = self.is_directory_or_file(item)
            if item_type == "directory":
                if not item in self.dir_list:
                    self.dir_list.append(item)
                    dir_temp.append(item)
            elif item_type == "file":
                if not item in self.file_list:
                    self.file_list.append(item)
            else:
                self.unuse_list.append(item)
        for dir in dir_temp:
            for path, folder, files in os.walk(dir):
                for file in files:
                    if not file in self.file_list:
                        self.file_list.append(path + '/' + file)

        event.accept()
        self.clear_list_widget()
        self.list_widget.addItems(self.file_list)
        self.list_widget_colored()
        self.update_title_widget()
        
    def list_widget_colored(self):
        entered_dict = dict()
        for i in range(self.list_widget.count()):
            path = self.list_widget.item(i).text()
            file_name = os.path.basename(path)
            if not file_name in entered_dict:
                entered_dict[file_name] = ''
            else:
                item = self.list_widget.item(i)
                item.setForeground(QtGui.QColor("red"))
                self.dupli_list.append(file_name)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            selected_items = self.list_widget.selectedItems()
            for item in selected_items:
                self.list_widget.takeItem(self.list_widget.row(item))
            self.update_title_widget()
            if self.list_widget.count() == 0:
                self.initialized_self_list()
        elif event.key() == QtCore.Qt.Key_Escape:
            self.list_widget.clearSelection()
        else:
            super().keyPressEvent(event)

    def save_html_file(html_code, file_path):
        my_path = Path.home()
        helper = 'Guide.html'
        file_path = os.path.join(my_path, helper)
        app = 'explorer.exe'
        if os.path.isfile(file_path):
            subprocess.call([app, file_path])
        else:
            html = """
                <h2>사용법 📙</h2>

                <ol>
                <li>애플리케이션에 폴더를 <strong>드래그 앤 드롭</strong></li>
                <li>
                    합쳐질 <strong>경로를 설정</strong>
                    <ul>
                    <li>리스트에 빨갛게 표시된다면 <span style='background-color: #fff5b1; color: red'>중복된 파일</span></li>
                    <li>리스트에 있는 하나의 아이템을 더블클릭하면 탐색기 해당 파일이 있는 탐색기 창이 열림</li>
                    </ul>
                </li>
                <li><strong>Combine</strong> 버튼을 누르면 설정된 경로에 파일이 합쳐짐</li>
                <li><strong>Divide</strong> 버튼을 누르면 원래 있던 경로로 파일이 다시 이동됨</li>
                </ol>

                <h2>버튼 설명</h2>

                <ul>
                <li>Combine : 각각 폴더안의 파일을 설정한 <strong>경로로 이동</strong></li>
                <li>Divide : 설정한 경로로 이동했던 파일을 <strong>원래의 폴더로 이동</strong></li>
                <li>Clear : 드래그 앤 드롭 했던 파일들을 <strong>초기화</strong></li>
                <li>Set path : 이동할 <strong>경로를 설정</strong> (합쳐질 경로를 의미)</li>
                <li>Save : 현재 목록을 json 파일 형태로 저장</li>
                <li>Load : 이전에 저장해 두었던 목록을 불러옴</li>
                <li>Exit : 앱을 종료</li>
                </ul>
            """
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html)
            
            subprocess.call([app, file_path])

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = FileMergeNDivide()
    MainWindow.show()
    sys.exit(app.exec_())
