from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QPushButton
from PyQt6.QtWebEngineWidgets import QWebEngineView
import sys

class CloseableTabWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
    def initUI(self):
        layout = QVBoxLayout()
        # 创建 QTabWidget
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setTabsClosable(True)  # 允许选项卡关闭
        # 连接标签关闭事件到槽函数
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        urls = [
            # '全网同名：派森斗罗'
            'https://space.bilibili.com/1909782963',  # B站
            'https://github.com/w-x-x-w',  # Github
            'https://w-x-x-w.github.io/',  # 个人主页
            'https://blog.csdn.net/weixin_62650212',  # CSDN
        ]
        # 添加标签页并关联每个标签页的 QWebEngineView
        for i in range(len(urls)):  # 三个标签页示例
            web_view = QWebEngineView()
            web_view.setUrl(QUrl(urls[i]))
            # 创建包含关闭按钮的小部件
            tab_widget = QWidget()
            tab_layout = QVBoxLayout(tab_widget)
            tab_layout.addWidget(web_view)
            # 添加关闭按钮
            close_button = QPushButton("关闭")
            close_button.clicked.connect(lambda _, index=i: self.close_tab(index))
            tab_layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignRight)
            self.tab_widget.addTab(tab_widget, f"Page {i + 1}")
        # 将 QTabWidget 添加到布局中
        layout.addWidget(self.tab_widget)
        # 设置布局
        self.setLayout(layout)
    def close_tab(self, index):
        # 关闭标签页的槽函数
        if index >= 0:
            self.tab_widget.removeTab(index)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    closeable_tab_widget = CloseableTabWidget()
    closeable_tab_widget.show()
    sys.exit(app.exec())
