import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCharts import QChart, QChartView, QLineSeries
from PyQt6.QtGui import QPainter

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Qt Charts Example")
        self.setGeometry(100, 100, 800, 600)

        # 创建一个 QLineSeries 对象并添加数据点
        series = QLineSeries()
        series.append(0, 6)
        series.append(2, 4)
        series.append(3, 8)
        series.append(7, 4)
        series.append(10, 5)

        # 创建一个 QChart 对象并添加系列
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Simple Line Chart Example")
        chart.createDefaultAxes()

        # 创建一个 QChartView 对象并将其设置为中央窗口部件
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(chart_view)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
