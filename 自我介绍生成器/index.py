import sys
import time
from PyQt6.QtCore import Qt, QThreadPool, QRunnable, pyqtSignal
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QComboBox, QCheckBox, QPushButton, QProgressBar

class Worker(QRunnable):
    def __init__(self, callback, *args, **kwargs):
        super(Worker, self).__init__()
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def run(self):
        result = self.callback(*self.args, **self.kwargs)
        self.callback.result.emit(result)

class SelfIntroductionGenerator(QWidget):
    def __init__(self):
        super(SelfIntroductionGenerator, self).__init__()

        self.name_label = QLabel("姓名:")
        self.name_input = QLineEdit()

        self.gender_label = QLabel("性别:")
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["男", "女"])

        self.hobbies_label = QLabel("兴趣爱好:")
        self.hobbies_input = QLineEdit()

        self.gpu_checkbox = QCheckBox("GPU加速")
        self.threadpool_checkbox = QCheckBox("多线程线程池加速")
        self.cloud_checkbox = QCheckBox("云服务计算加速")
        self.bigdata_checkbox = QCheckBox("大数据分析")
        self.ai_beautify_checkbox = QCheckBox("人工智能美化")

        self.generate_button = QPushButton("生成自我介绍")
        self.generate_button.clicked.connect(self.generate_introduction)

        self.progress_bar = QProgressBar()

        layout = QVBoxLayout(self)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.gender_label)
        layout.addWidget(self.gender_combo)
        layout.addWidget(self.hobbies_label)
        layout.addWidget(self.hobbies_input)
        layout.addWidget(self.gpu_checkbox)
        layout.addWidget(self.threadpool_checkbox)
        layout.addWidget(self.cloud_checkbox)
        layout.addWidget(self.bigdata_checkbox)
        layout.addWidget(self.ai_beautify_checkbox)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.progress_bar)

        # self.threadpool = QThreadPool()
        # self.worker = Worker(self.generate_introduction_callback)
        # self.worker.callback.result.connect(self.show_introduction)

    def generate_introduction(self):
        self.progress_bar.setValue(0)
        self.worker.args = (self.name_input.text(), self.gender_combo.currentText(), self.hobbies_input.text())
        self.threadpool.start(self.worker)

    def generate_introduction_callback(self, name, gender, hobbies):
        # 模拟生成自我介绍的过程，实际中需要调用相应的库和服务
        time.sleep(3)
        return f"大家好，我叫{name}，{gender}，兴趣爱好是{hobbies}。"

    def show_introduction(self, introduction):
        print(introduction)
        # 在这里可以将生成的自我介绍显示在界面上，或者进行其他处理
        self.progress_bar.setValue(100)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SelfIntroductionGenerator()
    window.show()
    sys.exit(app.exec())