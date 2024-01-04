import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QComboBox, QMessageBox, QDialog
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QPixmap
import mysql.connector

class Contact:
    def __init__(self, Mata_Kuliah, Tanggal_Perkuliahan, Nama, NIM, Jurusan, Kelas):
        self.Mata_Kuliah = Mata_Kuliah
        self.Tanggal_Perkuliahan = Tanggal_Perkuliahan
        self.Nama = Nama
        self.NIM = NIM
        self.Jurusan = Jurusan
        self.Kelas = Kelas

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

class AttendanceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.__init_ui()

    def __init_ui(self):
        # Check if login is successful
        login_dialog = LoginDialog()
        if login_dialog.exec_() != QDialog.Accepted:
            sys.exit()

        # Continue with the rest of the initialization
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Absensi Perkuliahan')

        # Connect to MySQL database
        try:
            self.db_connection = mysql.connector.connect(
                user="root",
                password="",
                database="absensimhs"
            )
            self.cursor = self.db_connection.cursor()

            # Create the table if it doesn't exist
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS attendance (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nama VARCHAR(255),
                    nim VARCHAR(255),
                    jurusan VARCHAR(255),
                    kelas VARCHAR(255),
                    matkul VARCHAR(255),
                    tanggal DATE
                )
            ''')
            print("Connected to MySQL database.")

        except Exception as e:
            QMessageBox.critical(self, 'Error', f"Failed to connect to the database: {str(e)}")
            print(f"Failed to connect to the database: {str(e)}")

        self.setup_widgets()

    # ... (rest of the code for AttendanceApp class)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    coba = AttendanceApp()
    coba.show()
    sys.exit(app.exec_())
