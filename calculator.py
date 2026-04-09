import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QGridLayout
)
from PyQt6.QtCore import Qt



class Calculator(QWidget):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("Quick Maths :) ")
        self.setMinimumHeight(300)
        self.setMinimumWidth(400)

        self.layout = QVBoxLayout()

        # Display
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
        self.hasUserInput = False
        self.display.setText('Hello!')

        self.display.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setFocus()
        self.display.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setFocus()
    

        # Buttons
        self.buttons = [
            ('CLR', '', '⌫',  '÷'),
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

                if value in ['+', '-', 'x', '÷', '='] or value == 'CLR':
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
                    grid.addWidget(button, row, col, 1, 2)
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

    # -------------------------
    # Button Click Logic
    # -------------------------
    def on_button_click(self):
        button = self.sender()
        text = button.text()
        self.handle_input(text)

    # -------------------------
    # Keyboard Input (Qt Native)
    # -------------------------
    def keyPressEvent(self, event):
        key = event.key()
        text = event.text()

        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Equal):
            self.calculate_result()

        elif key in (Qt.Key.Key_Backspace, Qt.Key.Key_Delete):
            self.display.setText(self.display.text()[:-1])

        elif key == Qt.Key.Key_Escape:
            self.display.clear()

        elif key == Qt.Key.Key_Period:
            self.handle_input('.')

        elif text:
            self.handle_input(text)

    # -------------------------
    # Shared Input Handler
    # -------------------------
    def handle_input(self, text):
        current = self.display.text()
        if not self.hasUserInput:
            current = ""
            self.hasUserInput = True


        if text == '⌫':
            self.display.setText(current[:-1])
            return
        
        # Clear
        if text == "CLR":
            self.display.clear()
            return

        # Calculate
        if text == "=":
            self.calculate_result()
            return

        # Prevent double operators
        if current and self.is_operator(current[-1]) and self.is_operator(text):
            return

        self.display.setText(current + text)

    # -------------------------
    # Calculation Logic
    # -------------------------
    def calculate_result(self):
        try:
            expression = self.display.text().replace('x', '*')
            expression = expression.replace('÷', '/')

            result = str(eval(expression))
            rounded_val = round(float(result), 5)
            self.display.setText(str(rounded_val))
        except Exception:
            self.display.setText("Error")

    # -------------------------
    def is_operator(self, char):
        return char in "+-*/"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec())