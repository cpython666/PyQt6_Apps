import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QIcon


class MainWindow(QMainWindow):
	def __init__(self):
		
		super().__init__()
		
		
		self.setWindowTitle("PyQt6 Navigation Example")
		self.setGeometry(100, 100, 800, 600)
		
		# 创建左侧导航栏
		self.tree = QTreeWidget()
		self.tree.setHeaderHidden(True)
		
		# 创建根目录项
		root_item = QTreeWidgetItem(self.tree)
		root_item.setText(0, "Root")
		root_item.setIcon(0, QIcon("icons/setting.svg"))  # 设置图标
		
		# 创建子目录项
		child_item1 = QTreeWidgetItem(root_item)
		child_item1.setText(0, "Child 1")
		child_item1.setIcon(0, QIcon("icons/setting.svg"))  # 设置图标
		
		sub_child_item1 = QTreeWidgetItem(child_item1)
		sub_child_item1.setText(0, "Sub Child 1-1")
		sub_child_item1.setIcon(0, QIcon("icons/setting.svg"))  # 设置图标
		
		sub_child_item2 = QTreeWidgetItem(child_item1)
		sub_child_item2.setText(0, "Sub Child 1-2")
		sub_child_item2.setIcon(0, QIcon("icons/setting.svg"))  # 设置图标
		
		child_item2 = QTreeWidgetItem(root_item)
		child_item2.setText(0, "Child 2")
		child_item2.setIcon(0, QIcon("icons/setting.svg"))  # 设置图标
		
		sub_child_item3 = QTreeWidgetItem(child_item2)
		sub_child_item3.setText(0, "Sub Child 2-1")
		sub_child_item3.setIcon(0, QIcon("icons/setting.svg"))  # 设置图标
		
		sub_child_item4 = QTreeWidgetItem(child_item2)
		sub_child_item4.setText(0, "Sub Child 2-2")
		sub_child_item4.setIcon(0, QIcon("icons/setting.svg"))  # 设置图标
		
		self.tree.expandAll()  # 默认展开所有项
		
		# 添加导航栏到布局
		layout = QVBoxLayout()
		layout.addWidget(self.tree)
		
		# 创建主窗口内容部件
		content = QWidget()
		content.setLayout(layout)
		
		# 设置主窗口中央部件
		self.setCentralWidget(content)
		
		# 连接导航栏项点击信号到槽函数
		self.tree.itemClicked.connect(self.on_item_clicked)
		
		# 创建一个标签用于显示选中项的信息
		self.label = QLabel("Please select an item from the navigation")
		layout.addWidget(self.label)
		
		self.tree.setStyleSheet("""
		    QTreeWidget {
		        background-color: #f0f0f0;
		        font-size: 16px;
		    }
		    QTreeWidget::item {
		        padding: 5px;
		    }
		    QTreeWidget::item:selected {
		        background-color: #a0a0ff;
		        color: white;
		    }
		    QTreeWidget::item:hover {
		        background-color: #c0c0ff;
		    }
		""")
	
	def on_item_clicked(self, item, column):
		self.label.setText(f"Selected: {item.text(0)}")


if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec())
