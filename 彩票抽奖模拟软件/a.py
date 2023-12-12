# -*- coding: utf-8 -*-
# @Time    : 2023/12/8 18:44
# @QQ  : 2942581284
# @File    : a.py
import sys
from PyQt6.QtWidgets import QApplication,QLabel,QLineEdit, QWidget, QVBoxLayout, QPushButton, QProgressBar
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon
class ProgressBarApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('彩票抽奖')
        self.setGeometry(300, 200, 400, 200)
        self.setWindowIcon(QIcon('logo.png'))

        # 创建垂直布局
        layout = QVBoxLayout()
        self.name_input=QLineEdit()
        layout.addWidget(self.name_input)

        # 创建按钮
        self.start_button = QPushButton('点击抽奖', self)
        self.start_button.clicked.connect(self.startProgressBar)
        self.answer_label=QLabel('这里显示结果')
        layout.addWidget(self.start_button)
        # 创建进度条
        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.answer_label)

        # 设置布局
        self.setLayout(layout)

    def startProgressBar(self):
        self.answer_label.setText('抽奖中~')
        self.progress_bar.setValue(0)
        # 点击按钮后启动定时器，每20毫秒更新一次进度条
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateProgressBar)
        self.timer.start(20)

    def updateProgressBar(self):
        # 每次定时器触发，增加进度条的值
        current_value = self.progress_bar.value()
        new_value = current_value + 10
        # 如果进度条充满，停止定时器
        if new_value >= 100:
            new_value=100
            self.timer.stop()

        self.progress_bar.setValue(new_value)
        if new_value==100:
            self.choujiang()

    def choujiang(self):
        name=self.name_input.text()
        if name == '派森斗罗':
            result = '恭喜派森斗罗中了两亿！'
        else:
            result = '很遗憾，您只中了一毛钱。'
        self.answer_label.setText(result)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProgressBarApp()
    window.show()
    sys.exit(app.exec())
