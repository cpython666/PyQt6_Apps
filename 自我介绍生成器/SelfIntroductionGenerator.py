import sys
from PyQt6.QtCore import Qt, QTimer,QSize
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout,QGridLayout, QHBoxLayout, QLineEdit, QComboBox, QCheckBox, QPushButton, QProgressBar
from PyQt6.QtMultimedia import QMediaPlayer,QAudioOutput
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QIcon

class SelfIntroductionGenerator(QWidget):
    def __init__(self):
        super(SelfIntroductionGenerator, self).__init__()

        self.setWindowTitle("自我介绍生成器")
        self.setWindowIcon(QIcon('logo.png'))
        self.setGeometry(100, 100, 500, 300)

        self.name_label = QLabel("姓名:")
        self.name_input = QLineEdit()

        self.gender_label = QLabel("性别:")
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["男", "女"])

        self.hobbies_label = QLabel("兴趣爱好:")
        self.hobbies_checkboxes = [QCheckBox("旅行"), QCheckBox("阅读"), QCheckBox("音乐"),
                                   QCheckBox("电影"), QCheckBox("运动"), QCheckBox("美食")]

        self.checkbox_label=QLabel('选择加速服务：')
        self.ai_beautify_checkbox = QCheckBox("人工智能美化")
        self.gpu_checkbox = QCheckBox("GPU加速")
        self.threadpool_checkbox = QCheckBox("多线程线程池加速")
        self.cloud_checkbox = QCheckBox("云服务计算加速")
        self.bigdata_checkbox = QCheckBox("大数据分析")

        self.generate_button = QPushButton("生成自我介绍")
        self.generate_button.clicked.connect(self.button_clicked)

        self.progress_bar = QProgressBar()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress_bar)

        self.intro_label = QLabel("自我介绍将在此显示")
        self.intro_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.vip_button = QPushButton("充值VIP")
        self.vip_button.setIcon(QIcon('vip.jpg'))  # 设置VIP按钮图标
        self.vip_button.setIconSize(QSize(32,32)) # 设置图标大小
        # self.vip_button.setIconSize(self.vip_button.size())  # 设置图标大小
        self.vip_button.setStyleSheet("QPushButton { color: white; background-color: #FFD700; border-radius: 5px; }"
                                      "QPushButton:hover { background-color: #FFA500; }")  # 设置按钮样式


        layout = QVBoxLayout(self)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.gender_label)
        layout.addWidget(self.gender_combo)
        layout.addWidget(self.hobbies_label)

        # 使用QGridLayout进行兴趣爱好的布局
        grid_layout = QGridLayout()
        row, col = 0, 0
        for checkbox in self.hobbies_checkboxes:
            grid_layout.addWidget(checkbox, row, col, alignment=Qt.AlignmentFlag.AlignLeft)
            col += 1
            if col == 3:
                col = 0
                row += 1
        layout.addLayout(grid_layout)
        layout.addWidget(self.checkbox_label)
        layout.addWidget(self.ai_beautify_checkbox)
        layout.addWidget(self.threadpool_checkbox)
        layout.addWidget(self.cloud_checkbox)
        layout.addWidget(self.bigdata_checkbox)
        layout.addWidget(self.gpu_checkbox)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.intro_label)
        layout.addWidget(self.vip_button)

        self.counter=0

        self.time_vip=QTimer()
        self.time_vip.timeout.connect(self.vipTimer)
        self.time_vip.start(100)


    def vipTimer(self):
        if self.counter&1:
            self.vip_button.setStyleSheet("QPushButton{ background-color: #FFA500; }") 
        else:
            self.vip_button.setStyleSheet("QPushButton{ background-color: #FFD700; }") 
        self.counter+=1

    def button_clicked(self):
        self.play_mp3()
        self.generate_introduction()
        
    def play_mp3(self):
        print(1)
        self.media_player = QMediaPlayer()
        qurl=QUrl.fromLocalFile("fun.mp3")
        # qurl=QUrl.fromLocalFile("fan.mp3")
        self.audio_output = QAudioOutput()  # 声音文件路径
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setSource(qurl)
        self.audio_output.setVolume(10000)
        self.media_player.setPosition(0)  # 将声音定位到起始位置
        self.media_player.play()

    def generate_introduction(self):
        self.progress_bar.setValue(0)
        self.timer.start(50)  # 设置定时器的间隔，单位为毫秒

    def update_progress_bar(self):
        current_value = self.progress_bar.value()
        if current_value < 100:
            self.progress_bar.setValue(current_value + 1)
        else:
            self.timer.stop()
            self.generate_introduction_callback()

    def generate_introduction_callback(self):
        name = self.name_input.text()
        gender = self.gender_combo.currentText()
        hobbies = [checkbox.text() for checkbox in self.hobbies_checkboxes if checkbox.isChecked()]
        introduction = self.generate_introduction_text(name, gender, hobbies)
        self.show_introduction(introduction)

    def generate_introduction_text(self, name, gender, hobbies):
        hobbies_str = ', '.join(hobbies)
        return f"大家好，我叫{name}，{gender}，兴趣爱好是{hobbies_str}。"

    def show_introduction(self, introduction):
        self.intro_label.setText(introduction)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SelfIntroductionGenerator()
    window.show()
    sys.exit(app.exec())
