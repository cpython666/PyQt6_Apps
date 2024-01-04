from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
import sys

class WebTabWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 创建 QTabWidget
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setTabsClosable(True)  # 允许选项卡关闭

        urls=['https://www.google.cn/','https://github.com/']
        # 添加标签页并关联每个标签页的 QWebEngineView
        for i in range(2):  # 三个标签页示例
            web_view = QWebEngineView()
            web_view.setUrl(QUrl(urls[i]))
            self.tab_widget.addTab(web_view, f"Page {i + 1}")

        # 将 QTabWidget 添加到布局中
        layout.addWidget(self.tab_widget)

        # 设置布局
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    web_tab_widget = WebTabWidget()
    web_tab_widget.show()
    sys.exit(app.exec())
