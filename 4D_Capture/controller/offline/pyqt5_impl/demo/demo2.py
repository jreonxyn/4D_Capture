#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Created on 2019年1月16日

@author: yiluo

@site: https://github.com/bingshilei

@email: 786129166@qq.com

@file: QThreadDemo2

@description: 使用多线程动态添加控件

"""

import time

from PyQt5.QtCore import QThread, pyqtSignal, QDateTime

from PyQt5.QtWidgets import QWidget, QLineEdit, QListWidget, QPushButton, QVBoxLayout, QLabel

'''

声明线程类

'''

class addItemThread(QThread):

    add_item = pyqtSignal(str)

    show_time = pyqtSignal(str)

    '''

            添加控件

    '''

    def __init__(self,*args, **kwargs):

        super(addItemThread, self).__init__(*args, **kwargs)

        self.num = 0

    def run(self, *args, **kwargs):

        while True:

            file_str = 'File index{0}'.format(self.num,*args, **kwargs)

            self.num +=1

            #发送添加信号

            self.add_item.emit(file_str)

            date = QDateTime.currentDateTime()

            currtime = date.toString('yyyy-MM-dd hh:mm:ss')

            print(currtime)

            self.show_time.emit(str(currtime))

            time.sleep(1)

class Window(QWidget):

    def __init__(self, *args, **kwargs):

        super(Window, self).__init__(*args, **kwargs)

        self.setWindowTitle('多线程动态添加控件')

        # x,y,w,h

        self.setGeometry(800, 100, 500, 750)

        #创建QListWidget控件

        self.listWidget = QListWidget()

        #创建按钮控件

        self.btn = QPushButton('开始',self)

        self.lb = QLabel('显示时间',self)

        #创建布局控件

        self.vlayout = QVBoxLayout()

        #将按钮和列表控件添加到布局

        self.vlayout.addWidget(self.btn)

        self.vlayout.addWidget(self.lb)

        self.vlayout.addWidget(self.listWidget)

        #设置窗体的布局

        self.setLayout(self.vlayout)

        #绑定按钮槽函数

        self.btn.clicked.connect(self.startThread)

        #声明线程实例

        self.additemthread = addItemThread()

        #绑定增加控件函数

        self.additemthread.add_item.connect(self.addItem)

        #绑定显示时间函数

        self.additemthread.show_time.connect(self.showTime)

    '''

    @description:按钮开始，启动线程

    '''

    def startThread(self):

        #按钮不可用

        self.btn.setEnabled(False)

        #启动线程

        self.additemthread.start()

    '''

    @description:为listwidget增加项

    @param:项的值 

    '''

    def addItem(self,file_str):

        self.listWidget.addItem(file_str)

    '''

    @description:显示时间

    @param:项的值 

    '''

    def showTime(self,time):

        self.lb.setText(time)

if __name__ == '__main__':

    import sys

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    w = Window()

    w.show()

    sys.exit(app.exec_())