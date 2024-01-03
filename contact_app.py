import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QComboBox, QMessageBox, QDialog,)
import sqlite3
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QPixmap


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Login')
        self.setGeometry(300, 300, 400, 200) 
        self.setStyleSheet("background-color: lightblue;")

        # Add QLabel for logo
        self.logo_label = QLabel(self)
        self.logo_label.setGeometry(5, 5, 250, 250) 
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

       
        if username and password:
            self.accept()
        else:
            QMessageBox.warning(self, 'Login Failed', 'Invalid username or password')



class Contact:
    def __init__(self, Mata_Kuliah, Tanggal_Perkuliahan, Nama, NIM, Jurusan):
        self.Mata_Kuliah = Mata_Kuliah
        self.Tanggal_Perkuliahan = Tanggal_Perkuliahan
        self.Nama = Nama
        self.NIM = NIM
        self.Jurusan = Jurusan

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

        # Connect to SQLite database
        try:
            self.db_connection = sqlite3.connect("absensi.db")
            self.cursor = self.db_connection.cursor()

            # Create the table if it doesn't exist
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama TEXT,
                    nim TEXT,
                    jurusan TEXT,
                    matkul TEXT,
                    tanggal TEXT
                )
            ''')
            print("Connected to SQLite database.")

        except Exception as e:
            QMessageBox.critical(self, 'Error', f"Failed to connect to the database: {str(e)}")
            print(f"Failed to connect to the database: {str(e)}")

        self.setup_widgets()

    def setup_widgets(self):
        layout = QVBoxLayout(self)

        self.title_label = QLabel('Absensi Perkuliahan', self)
        layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.matkul_label = QLabel('Mata Kuliah:', self)
        layout.addWidget(self.matkul_label)

        self.matkul_combobox = QComboBox(self)
        self.populate_courses()
        layout.addWidget(self.matkul_combobox)

        self.tanggal_label = QLabel('Tanggal Perkuliahan:', self)
        layout.addWidget(self.tanggal_label)

        self.tanggal_entry = QLineEdit(self)
        self.tanggal_entry.setText(QDate.currentDate().toString("yyyy-MM-dd"))
        layout.addWidget(self.tanggal_entry)

        self.nama_label = QLabel('Nama:', self)
        layout.addWidget(self.nama_label)

        self.nama_entry = QLineEdit(self)
        self.nama_entry.setStyleSheet("background-color: lightcyan;")
        layout.addWidget(self.nama_entry)

        self.nim_label = QLabel('NIM:', self)
        layout.addWidget(self.nim_label)

        self.nim_entry = QLineEdit(self)
        self.nim_entry.setStyleSheet("background-color: lightcyan;")
        layout.addWidget(self.nim_entry)

        self.jurusan_label = QLabel('Jurusan:', self)
        layout.addWidget(self.jurusan_label)

        self.jurusan_entry = QLineEdit(self)
        self.jurusan_entry.setStyleSheet("background-color: lightcyan;")
        layout.addWidget(self.jurusan_entry)

        self.insert_button = QPushButton('Insert', self)
        self.insert_button.clicked.connect(self.insert_data)
        self.insert_button.setStyleSheet("background-color: lightblue;")
        layout.addWidget(self.insert_button)

        self.save_button = QPushButton('Save', self)
        self.save_button.clicked.connect(self.save_data)
        self.save_button.setStyleSheet("background-color: lightblue;")
        layout.addWidget(self.save_button)

        create_new_button = QPushButton('Create New', self)
        create_new_button.clicked.connect(self.create_new_data)
        create_new_button.setStyleSheet("background-color: lightblue;")
        layout.addWidget(create_new_button)

        self.exit_button = QPushButton('Exit', self)
        self.exit_button.clicked.connect(self.close)
        self.exit_button.setStyleSheet("background-color: lightcoral;")
        layout.addWidget(self.exit_button)

        self.informasi_label = QLabel(
            'Klik Insert untuk semua mahasiswa, kemudian klik Save jika semua telah diabsen.', self)
        layout.addWidget(self.informasi_label)

        self.setLayout(layout)

    def insert_data(self):
        try:
            # Get data from UI
            Mata_Kuliah = self.matkul_combobox.currentText()
            Tanggal_Perkuliahan = QDate.currentDate().toString("yyyy-MM-dd")
            Nama = self.nama_entry.text()
            NIM = self.nim_entry.text()
            Jurusan = self.jurusan_entry.text()

            # Create a Contact instance
            contact = Contact(Mata_Kuliah, Tanggal_Perkuliahan, Nama, NIM, Jurusan)

            # Save data to SQLite database
            self.save_contact_to_database(contact)

            # Clear entry fields
            self.clear_entries()

            # Provide user feedback
            QMessageBox.information(self, 'Success', "Data inserted successfully.")
            print("Data inserted successfully.")

        except Exception as e:
            QMessageBox.critical(self, 'Error', f"Failed to insert data: {str(e)}")
            print(f"Failed to insert data: {str(e)}")

    def save_contact_to_database(self, contact):
        try:
            query = '''
                INSERT INTO attendance (nama, nim, jurusan, matkul, tanggal)
                VALUES (?, ?, ?, ?, ?)
            '''
            data = (contact.Nama, contact.NIM, contact.Jurusan, contact.Mata_Kuliah, contact.Tanggal_Perkuliahan)

            self.cursor.execute(query, data)
            self.db_connection.commit()

        except Exception as e:
            QMessageBox.critical(self, 'Error', f"Failed to save contact to database: {str(e)}")
            print(f"Failed to save contact to database: {str(e)}")

    def save_data(self):
        try:
            # Your implementation for saving data
            # Provide user feedback
            QMessageBox.information(self, 'Success', "Data absen telah di save!")
            print("Data saved successfully.")

        except Exception as e:
            QMessageBox.critical(self, 'Error', f"An error occurred: {str(e)}")
            print(f"An error occurred: {str(e)}")

    def create_new_data(self):
        # Your implementation for creating new data
        QMessageBox.information(self, 'Information', "Create New Data")
        print("Create New Data")

    def clear_entries(self):
        # Clear all entry fields
        self.tanggal_entry.clear()
        self.nama_entry.clear()
        self.nim_entry.clear()
        self.jurusan_entry.clear()

    def populate_courses(self):
        # Add courses to the combo box (you may fetch them from the database)
        courses = ["PBO", "BASIS DATA", "STRUKTUR DATA", "RISET OPERASI", "BAHASA INDONESIA"]
        self.matkul_combobox.addItems(courses)

    def closeEvent(self, event):
        if self.db_connection:
            self.db_connection.close()
            print("Database connection closed.")
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    coba = AttendanceApp()
    coba.show()
    sys.exit(app.exec_())
