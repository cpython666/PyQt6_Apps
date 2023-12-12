import sys
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QWidget,QHBoxLayout, QVBoxLayout, QCheckBox, QProgressBar, QLabel
from PyQt6.QtGui import QIcon

class HandsomeVerificationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(300,200,500,350)
        self.setWindowTitle('帅哥验证器')
        self.setWindowIcon(QIcon('logo.png'))

        # 创建复选框
        check_layout=QHBoxLayout()

        check_layout.addStretch(1)
        self.checkbox = QCheckBox('我是帅哥', self)
        self.checkbox.stateChanged.connect(self.start_verification)
        check_layout.addWidget(self.checkbox)
        check_layout.addStretch(1)
        # 创建进度条
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        # 创建验证结果标签
        self.result_label = QLabel('', self)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setVisible(False)

        # 设置布局
        layout = QVBoxLayout(self)
        layout.addStretch(2)
        layout.addLayout(check_layout)
        layout.addStretch(1)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.result_label)
        layout.addStretch(2)

        self.setLayout(layout)

    def start_verification(self):
        self.progress_bar.setVisible(True)
        # 模拟验证过程，加载2秒
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.verify_complete)
        self.timer.start(20)

    def verify_complete(self):
        current_value = self.progress_bar.value()
        if current_value < 100:
            self.progress_bar.setValue(current_value + 1)
        else:
            self.timer.stop()
            self.progress_bar.setVisible(False)
            self.result_label.setText('验证通过：你是帅哥')
            self.result_label.setVisible(True)

def main():
    app = QApplication(sys.argv)
    window = HandsomeVerificationApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
