from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Login')
        self.setGeometry(300, 300, 400, 200)
        self.setStyleSheet("background-color: lightblue;")

        # Add QLabel for logo
        self.logo_label = QLabel(self)
        self.logo_label.setGeometry(25, 25, 250, 250)
        pixmap = QPixmap('Logo-UNP-Kediri-terbaru-2023.png')
        self.logo_label.setPixmap(pixmap.scaled(self.logo_label.size(), Qt.KeepAspectRatio))
        self.logo_label.setScaledContents(True)

        self.username_label = QLabel('Username:', self)
        self.username_entry = QLineEdit(self)
        self.password_label = QLabel('Password:', self)
        self.password_entry = QLineEdit(self)
        self.password_entry.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.check_login)

        layout = QVBoxLayout(self)
        layout.addWidget(self.logo_label)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_entry)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_entry)
        layout.addWidget(self.login_button)

    def check_login(self):
        username = self.username_entry.text()
        password = self.password_entry.text()

        if username != "" and password != "":
            QMessageBox.information(self, 'Login Successful', 'Welcome!')
            self.accept()
        else:
            QMessageBox.warning(self, 'Login Failed', 'Invalid username or password')
