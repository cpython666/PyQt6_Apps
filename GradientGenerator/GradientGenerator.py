from PyQt6.QtWidgets import (QApplication,QSpinBox, QMainWindow, QDoubleSpinBox,QLabel, QVBoxLayout,
                             QPushButton, QWidget, QHBoxLayout, QSlider, QColorDialog, QListWidget,
                             QListWidgetItem,QLineEdit,QMessageBox)
from PyQt6.QtGui import (QGuiApplication,QPixmap,
                         QPainter, QLinearGradient, QColor,QIcon,QDesktopServices)
from PyQt6.QtCore import Qt, QPointF,pyqtSignal,QObject,QUrl
from os import path,mkdir
import math

class FloatSlider(QSlider):
    valueChangedFloat = pyqtSignal(float,QObject)
    
    def __init__(self, parent=None):
        super().__init__(Qt.Orientation.Horizontal, parent)
        self._multiplier = 100  # 放大倍数，例如设置为100，就支持两位小数

        self.valueChanged.connect(self.emitFloatValueChanged)

    def setFloatValue(self, floatValue):
        intValue = int(floatValue * self._multiplier)
        self.setValue(intValue)

    def floatValue(self):
        return self.value() / self._multiplier

    def emitFloatValueChanged(self):
        self.valueChangedFloat.emit(self.floatValue(),self)

    def setMultiplier(self, multiplier):
        self._multiplier = multiplier

    def multiplier(self):
        return self._multiplier

class GradientWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.width = 200
        self.height = 200
        self.angle = 135
        self.window_width=1000
        self.window_height=500
        self.pre_width=500
        self.colors = [{'position':0, 'color':QColor(255, 0, 0)}, {'position':1,'color':QColor(255, 255, 0)}]

        self.initUI()
        self.initLayout()
        self.update_colors_list()

        
    def initUI(self):
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle('渐变图片生成器')
        self.setGeometry(0,0,self.window_width,self.window_height)
        self.center()
        
    def center(self):
        qr=self.frameGeometry()
        cp=QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initLayout(self):
        self.width_label = QLabel(f'图片宽度:{self.width}px', self)
        self.width_input_line = QSpinBox(self)
        self.width_input_line.setMinimum(1)
        self.width_input_line.setMaximum(10*10000*10000)
        self.width_input_line.setValue(self.width)
        self.width_unit_label = QLabel('像素', self)
        self.width_input_line.valueChanged.connect(self.update_width)
        width_input_layout = QHBoxLayout()
        width_input_layout.addWidget(self.width_label)
        width_input_layout.addWidget(self.width_input_line)
        width_input_layout.addWidget(self.width_unit_label)

        self.height_label = QLabel(f'图片高度:{self.height}px', self)
        self.height_input_line = QSpinBox(self)
        self.height_input_line.setMinimum(1)
        self.height_input_line.setMaximum(10*10000*10000)
        self.height_input_line.setValue(self.height)
        self.height_input_line.valueChanged.connect(self.update_height)
        self.height_unit_label = QLabel('像素', self)
        height_input_layout = QHBoxLayout()
        height_input_layout.addWidget(self.height_label)
        height_input_layout.addWidget(self.height_input_line)
        height_input_layout.addWidget(self.height_unit_label)

        self.angle_label=QLabel(f'角度:{self.angle}°', self)
        self.angle_slider = QSlider(Qt.Orientation.Horizontal)
        self.angle_slider.setMinimum(0)
        self.angle_slider.setMaximum(360)
        self.angle_slider.setValue(self.angle)
        self.angle_slider.valueChanged.connect(self.update_angle)
        angle_layout=QHBoxLayout()
        angle_layout.addWidget(self.angle_label)
        angle_layout.addWidget(self.angle_slider)

        self.percentage_label = QLabel('新增颜色百分比:')
        self.percentage_edit = QDoubleSpinBox()
        self.percentage_edit.setMinimum(0)
        self.percentage_edit.setMaximum(1)
        percentage_layout = QHBoxLayout()
        percentage_layout.addWidget(self.percentage_label)
        percentage_layout.addWidget(self.percentage_edit)

        self.add_color_button = QPushButton('增加颜色过渡')
        self.add_color_button.clicked.connect(self.add_color)

        self.colors_list = QListWidget()

        self.delete_color_button = QPushButton('删除选中的颜色')
        self.delete_color_button.clicked.connect(self.delete_color)

        self.create_button = QPushButton('创建图片', self)
        self.create_button.clicked.connect(self.createImage)

        learn_layout=QHBoxLayout()
        learn_button=QPushButton('寻找颜色灵感！')
        font=learn_button.font()
        font.setUnderline(True)
        learn_button.setFont(font)
        learn_button.setStyleSheet("border:0;")
        learn_button.clicked.connect(lambda:self.open_browser('https://uigradients.com/'))
        learn_layout.addWidget(learn_button)

        author_layout=self.get_link_layout()

        config_layout=QVBoxLayout()
        config_layout.addLayout(learn_layout)
        config_layout.addLayout(width_input_layout)
        config_layout.addLayout(height_input_layout)
        config_layout.addLayout(angle_layout)
        config_layout.addLayout(percentage_layout)
        config_layout.addWidget(self.add_color_button)
        config_layout.addWidget(self.colors_list)
        config_layout.addWidget(self.delete_color_button)
        config_layout.addWidget(self.create_button)
        config_layout.addLayout(author_layout)

        central_widget = QWidget(self)
        main_layout = QHBoxLayout()
        # 左侧窗口
        configs_widget = QWidget(self)
        configs_widget.setLayout(config_layout)
        # 右侧窗口
        self.preview_label = QLabel()
        self.update_preview()

        # 主布局
        main_layout.addWidget(configs_widget)
        main_layout.addWidget(self.preview_label)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def createImage(self):
        pixmap=self.create_custom_gradient_image()
        # 获取当前日期和时间
        if not path.exists('bgs'):
            mkdir('bgs')
        name_str=''
        for color_obj in self.colors:
            name_str+=color_obj['color'].name()
        pixmap.save(f'./bgs/{self.width}x{self.height}-{self.angle}-{name_str}.png')
        QMessageBox.information(self, '提示', '图片已保存在 bgs 目录下！', QMessageBox.StandardButton.Ok)
    
    def get_link_layout(self,text="Made By",des='派森斗罗',link='https://space.bilibili.com/1909782963'):
        layout = QHBoxLayout()
        label=QLabel(text)
        open_button = QPushButton(des, self)
        font=open_button.font()
        font.setUnderline(True)
        open_button.setFont(font)
        open_button.setStyleSheet("border:0;")
        open_button.clicked.connect(lambda:self.open_browser(link))
        layout.addStretch(1)
        layout.addWidget(label)
        layout.addWidget(open_button)
        layout.addStretch(1)
        return layout

    def open_browser(self,link):
        url = QUrl(link)
        # 使用QDesktopServices打开默认浏览器
        QDesktopServices.openUrl(url)

    def update_width(self, value):
        if value<5:
            value=5
        self.width = value
        self.width_label.setText(f'图片宽度:{self.width}px')
        self.update_preview()

    def update_height(self, value):
        if value<5:
            value=5
        self.height = value
        self.height_label.setText(f'图片高度:{self.height}px')
        self.update_preview()

    def update_angle(self, value):
        self.angle = value
        self.angle_label.setText(f'角度:{self.angle}°')
        self.update_preview()

    def update_preview(self):
        pixmap = self.create_custom_gradient_image()
        scaled_pixmap = pixmap.scaledToWidth(self.pre_width)
        self.preview_label.setPixmap(scaled_pixmap)

    def create_custom_gradient_image(self):
        pixmap = QPixmap(self.width, self.height)
        pixmap.fill(Qt.GlobalColor.white)  # 设置背景为白色
        painter = QPainter(pixmap)
        # 创建渐变对象，设置渐变的起始和结束点坐标
        start_point, end_point = self.calculate_gradient_points()
        gradient = QLinearGradient(start_point, end_point)
        # 添加颜色节点
        for color_obj in self.colors:
            gradient.setColorAt(color_obj['position'], color_obj['color'])
        # 用渐变填充矩形
        painter.fillRect(pixmap.rect(), gradient)
        painter.end()
        return pixmap

    def calculate_gradient_points(self):
        radian_angle = self.angle * math.pi / 180.0

        start_point = QPointF(self.width / 2 - (self.width / 2) * math.cos(radian_angle),
                              self.height / 2 - (self.height / 2) * math.sin(radian_angle))

        end_point = QPointF(self.width / 2 + (self.width / 2) * math.cos(radian_angle),
                            self.height / 2 + (self.height / 2) * math.sin(radian_angle))

        return start_point, end_point

    def add_color(self):
        color = QColorDialog.getColor()
        percentage = float(self.percentage_edit.text()) if self.percentage_edit.text() else 0.5
        if color.isValid():
            self.colors.append({'position':percentage, 'color':color})
            self.update_preview()
            self.update_colors_list()

    def delete_color(self):
        selected_items = self.colors_list.selectedItems()
        for item in selected_items:
            index = self.colors_list.row(item)
            del self.colors[index]

        self.update_preview()
        self.update_colors_list()

    def update_colors_list(self):
        self.colors_list.clear()
        for index,color_obj in enumerate(self.colors):
            listItem=QWidget()
            listItem.index=index
            listItem.label_position=QLabel(f"百分比:{color_obj['position']:.2%}",listItem)
            listItem.label_position.setFixedWidth(90)
            slider_position=FloatSlider()
            slider_position.setFixedWidth(100)
            slider_position.setRange(0,1*slider_position.multiplier())
            slider_position.setValue(int(color_obj['position']*slider_position.multiplier()))
            slider_position.valueChangedFloat.connect(self.update_list_item_label)
            listItem.label_color=QLabel("颜色:",listItem)

            listItem.color_line=QLineEdit()
            listItem.color_line.setText(color_obj['color'].name())
            listItem.color_line.textChanged.connect(self.update_list_item_color_line)

            listItem.button_color=QPushButton()
            listItem.button_color.setFixedSize(20,20)
            listItem.button_color.setStyleSheet(f"background-color:{color_obj['color'].name()}")
            listItem.button_color.clicked.connect(self.update_list_item_button)

            listItemLayout=QHBoxLayout()
            listItemLayout.addWidget(listItem.label_position)
            listItemLayout.addWidget(slider_position)
            listItemLayout.addWidget(listItem.label_color)
            listItemLayout.addWidget(listItem.color_line)
            listItemLayout.addWidget(listItem.button_color)
            listItem.setLayout(listItemLayout)

            item = QListWidgetItem()
            item.setSizeHint(listItem.sizeHint())
            self.colors_list.addItem(item)
            self.colors_list.setItemWidget(item,listItem)

    def update_list_item_label(self,value,obj):
        obj.parent().label_position.setText(f"百分比:{value:.2%}")
        self.colors[obj.parent().index]['position']=value
        self.update_preview()
    def update_list_item_color_line(self,value):
        line=self.sender()
        parent=line.parent()
        color_tmp=QColor(value)
        self.colors[parent.index]['color']=color_tmp
        parent.button_color.setStyleSheet(f"background-color:{color_tmp.name()}")
        self.update_preview()

    
    def update_list_item_button(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color
        button=self.sender()
        button.setStyleSheet(f"background-color:{color.name()}")
        parent=button.parent()
        self.colors[parent.index]['color']=color
        parent.color_line.setText(f"{color.name()}")
        self.update_preview()

if __name__ == '__main__':
    app = QApplication([])

    window = GradientWindow()
    window.show()

    app.exec()