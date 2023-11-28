import sys
from PyQt6.QtWidgets import (QApplication,QWidget,QHBoxLayout,QVBoxLayout,QLabel,
                             QMainWindow,QMessageBox,
                             QPushButton,
                             QSlider,QVBoxLayout,QColorDialog,QLineEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import (QGuiApplication,QPixmap, 
                         QColor,QIcon)

class ImageCreator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.initLayout()
        self.center()
    
    def initUI(self):
        self.setWindowTitle('纯色背景生成器')
        self.setGeometry(100,100,300,300)
        self.setWindowIcon(QIcon('logo.png'))
    
    def center(self):
        qr=self.frameGeometry()
        cp=QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initLayout(self):
        self.color_label = QLabel('当前颜色:(255,255,255,255)', self)
        self.color_button = QPushButton('选择颜色', self)
        self.color=QColor('white')
        self.color_button.clicked.connect(self.showColorDialog)
        color_layout=QHBoxLayout()
        color_layout.addStretch(1)
        color_layout.addWidget(self.color_label)
        color_layout.addWidget(self.color_button)
        color_layout.addStretch(1)

        self.bg_a=QLabel('图片不透明度：255')
        self.bg_a_slider=QSlider(Qt.Orientation.Horizontal)
        self.bg_a_slider.setRange(0, 255)
        self.bg_a_slider.setSingleStep(1)
        self.bg_a_slider.setValue(255)
        bg_a_layout=QHBoxLayout()
        bg_a_layout.addStretch(1)
        bg_a_layout.addWidget(self.bg_a)
        bg_a_layout.addWidget(self.bg_a_slider)
        bg_a_layout.addStretch(1)
        self.bg_a_slider.valueChanged.connect(self.update_bg_a_label)

        self.color_pre=QLabel('颜色预览：')
        self.color_rect=QLabel()
        self.color_rect.setFixedSize(50,50)
        self.color_rect.setStyleSheet(f'background-color: {self.color.name()}')
        color_pre_layout=QHBoxLayout()
        color_pre_layout.addStretch(1)
        color_pre_layout.addWidget(self.color_pre)
        color_pre_layout.addWidget(self.color_rect)
        color_pre_layout.addStretch(1)

        self.width_label = QLabel('图片长度:', self)
        self.width_input_line = QLineEdit(self)
        self.width_input_line.setPlaceholderText('在这里输入整数')
        self.width_unit_label = QLabel('像素', self)
        width_input_layout = QHBoxLayout()
        width_input_layout.addStretch(1)
        width_input_layout.addWidget(self.width_label)
        width_input_layout.addWidget(self.width_input_line)
        width_input_layout.addWidget(self.width_unit_label)
        width_input_layout.addStretch(1)

        self.height_label = QLabel('图片宽度:', self)
        self.height_input_line = QLineEdit(self)
        self.height_input_line.setPlaceholderText('在这里输入整数')
        self.height_unit_label = QLabel('像素', self)
        height_input_layout = QHBoxLayout()
        height_input_layout.addStretch(1)
        height_input_layout.addWidget(self.height_label)
        height_input_layout.addWidget(self.height_input_line)
        height_input_layout.addWidget(self.height_unit_label)
        height_input_layout.addStretch(1)

        self.create_button = QPushButton('创建图片', self)
        self.create_button.clicked.connect(self.createImage)

        self.auther=QLabel('made by 派森斗罗')
        self.auther.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        layout = QVBoxLayout()
        layout.addLayout(color_layout)
        layout.addLayout(bg_a_layout)
        layout.addLayout(color_pre_layout)

        layout.addLayout(width_input_layout)
        layout.addLayout(height_input_layout)

        layout.addWidget(self.create_button)
        layout.addWidget(self.auther)

        main_widget=QWidget()
        main_widget.setLayout(layout)

        self.setCentralWidget(main_widget)
    
    def update_bg_a_label(self):
        self.bg_a.setText(f'图片不透明度：{self.bg_a_slider.value()}')
        self.color.setAlpha(self.bg_a_slider.value())
        self.color_rect.setStyleSheet(f'background-color: {self.color.name()}')
        self.color_label.setText(f'当前颜色:{self.color.getRgb()}')

    def showColorDialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_label.setText(f'当前颜色:{self.color.getRgb()}')
            self.color_button.setStyleSheet(f'background-color: {color.name()}')
            self.color_rect.setStyleSheet(f'background-color: {color.name()}')
            self.color = color

    def createImage(self):
        width = int(self.width_input_line.text())
        height = int(self.height_input_line.text())
        if width <= 0 or height <= 0:
            return
        if not hasattr(self, 'color'):
            return
        image = QPixmap(width, height)
        image.fill(self.color)
        image.save(f'./bgs/{self.color.name()}-{width}x{height}.png')
        QMessageBox.information(self, '提示', '图片已保存在 bgs 目录下！', QMessageBox.StandardButton.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = ImageCreator()
    viewer.show()
    sys.exit(app.exec())