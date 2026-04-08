import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QGridLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontDatabase



class Calculator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Quick Maths :) ")
        self.setMinimumHeight(300)
        self.setMinimumWidth(400)

        self.layout = QVBoxLayout()

        #Display Settings
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet('''
            font-size: 50px; 
            font-family: VT323;
            padding: 15px; 
            border-radius: 10px; 
            background-color: #FFF3E0;
            color: #455054;
            ''')
        self.layout.addWidget(self.display)

        #Buttons Display Settings
        self.buttons = [
            ('CLR', '', '',  '/'),
            ('7', '8', '9', 'x'),
            ('4', '5', '6', '-'),
            ('1', '2', '3', '+'),
            ('0', '', '.', '=')
        ]

        grid = QGridLayout()
        grid.setVerticalSpacing(10)    
        grid.setHorizontalSpacing(5)
        for i in range(4):  
            grid.setColumnStretch(i, 1)

        for i in range(5):  
            grid.setRowStretch(i, 1)  


        for row, row_values in enumerate(self.buttons):
            col = 0
            while col < len(row_values):
                value = row_values[col]

                if value == "":
                    col += 1
                    continue

                button = QPushButton(value)
                button.setMinimumHeight(55)

                if value in ['+', '-', 'x', '/', '=']:
                    color = "#FD8F52"
                elif value == 'CLR':
                    color = "#FD8F52"
                else:
                    color = "#FFDCA2"

                button.setStyleSheet(f"""
                    QPushButton {{
                        font-size: 18px;
                        font-family: Montserrat;
                        border-radius: 15px;
                        background-color: {color};
                        color: #1F1F1F;
                    }}
                    QPushButton:hover {{
                        background-color: #C73866;
                        color: white;
                    }}
                """)

                button.clicked.connect(self.on_button_click)

                if value == "CLR":
                    grid.addWidget(button, row, col, 1, 3)  
                    col += 2
                elif value == "0" and row == 4:
                    grid.addWidget(button, row, col, 1, 2)  
                    col += 2
                else:
                    button.setMinimumWidth(60)
                    grid.addWidget(button, row, col)
                    col += 1

        self.layout.addLayout(grid)
        self.setLayout(self.layout)

    def on_button_click(self):
        button = self.sender()
        text = button.text()

        if text == "CLR":
            self.display.clear()
        elif text == "=":
            try:
                expression = self.display.text()
                expression = expression.replace('x', '*')
                result = str(eval(expression))
                self.display.setText(result)
            except:
                self.display.setText("Error")
        else:
            self.display.setText(self.display.text() + text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec())