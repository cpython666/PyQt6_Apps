import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QProgressBar
from PyQt6.QtCore import Qt, QTimer

class LotteryApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('抽奖程序')

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText('请输入名字')

        self.lottery_button = QPushButton('开始抽奖', self)
        self.lottery_button.clicked.connect(self.start_lottery)

        self.result_label = QLabel('抽奖结果将在这里显示', self)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)

        layout = QVBoxLayout(self)
        layout.addWidget(self.name_input)
        layout.addWidget(self.lottery_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.progress_bar)

    def start_lottery(self):
        name = self.name_input.text()
        if not name:
            self.result_label.setText('请输入名字再抽奖！')
            return
        # 虚假的抽奖操作
        result = self.simulate_lottery(name)
        # 更新抽奖结果
        self.result_label.setText(result)
        # 重置界面状态
        self.name_input.setDisabled(False)
        self.lottery_button.setDisabled(False)
        self.progress_bar.setValue(0)
        self.timer=QTimer()

    def simulate_lottery(self, name):
        # 模拟中奖，充满进度条需要 0.5 秒
        for i in range(101):
            self.timer.start(5)  # 定时器每隔5毫秒触发一次
            self.timer.singleShot(5 * i, self.progress_bar.setValue, i)
        if name == '派森斗罗':
            result = '恭喜，您中了两亿！'
        else:
            result = '很遗憾，您只中了一毛钱。'
        return result

    def update_progress(self):
        pass  # 用于占位，不需要实际操作

if __name__ == '__main__':
    app = QApplication(sys.argv)
    lottery_app = LotteryApp()
    lottery_app.show()
    sys.exit(app.exec())
