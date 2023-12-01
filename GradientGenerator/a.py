import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
import random

class Minesweeper(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Minesweeper")
        self.setGeometry(100, 100, 400, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.buttons = []
        self.grid_size = 8
        self.mine_count = 10
        self.create_grid()

    def create_grid(self):
        for row in range(self.grid_size):
            button_row = []
            for col in range(self.grid_size):
                button = QPushButton("", self)
                button.setFixedSize(40, 40)
                button.clicked.connect(lambda _, r=row, c=col: self.on_button_click(r, c))
                button_row.append(button)
                self.layout.addWidget(button)
            self.buttons.append(button_row)

        self.place_mines()

    def place_mines(self):
        mines = random.sample(range(self.grid_size * self.grid_size), self.mine_count)
        for mine in mines:
            row = mine // self.grid_size
            col = mine % self.grid_size
            self.buttons[row][col].setProperty("mine", True)

    def on_button_click(self, row, col):
        button = self.buttons[row][col]
        is_mine = button.property("mine")

        if is_mine:
            button.setText("💣")
            self.show_game_over()
        else:
            mine_count = self.count_adjacent_mines(row, col)
            button.setText(str(mine_count))
            button.setEnabled(False)

    def count_adjacent_mines(self, row, col):
        mine_count = 0
        for r in range(max(0, row - 1), min(self.grid_size, row + 2)):
            for c in range(max(0, col - 1), min(self.grid_size, col + 2)):
                if self.buttons[r][c].property("mine"):
                    mine_count += 1
        return mine_count

    def show_game_over(self):
        for row in self.buttons:
            for button in row:
                button.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    minesweeper = Minesweeper()
    minesweeper.show()
    sys.exit(app.exec())
