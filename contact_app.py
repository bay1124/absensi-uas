import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QComboBox, QMessageBox, QDialog
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QPixmap
import mysql.connector

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

class Contact:
    def __init__(self, Mata_Kuliah, Tanggal_Perkuliahan, Nama, NIM, Jurusan, Kelas):
        self.Mata_Kuliah = Mata_Kuliah
        self.Tanggal_Perkuliahan = Tanggal_Perkuliahan
        self.Nama = Nama
        self.NIM = NIM
        self.Jurusan = Jurusan
        self.Kelas = Kelas

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

        self.kelas_label = QLabel('Kelas:', self)
        layout.addWidget(self.kelas_label)

        self.kelas_entry = QLineEdit(self)
        self.kelas_entry.setStyleSheet("background-color: lightcyan;")
        layout.addWidget(self.kelas_entry)

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

        self.create_new_button = QPushButton('Create New', self)
        self.create_new_button.clicked.connect(self.create_new_data)
        self.create_new_button.setStyleSheet("background-color: lightblue;")
        layout.addWidget(self.create_new_button)

        self.sort_button = QPushButton('Sort by Class', self)
        self.sort_button.clicked.connect(self.sort_data)
        self.sort_button.setStyleSheet("background-color: lightyellow;")
        layout.addWidget(self.sort_button)

        self.exit_button = QPushButton('Exit', self)
        self.exit_button.clicked.connect(self.close)
        self.exit_button.setStyleSheet("background-color: lightcoral;")
        layout.addWidget(self.exit_button)

        self.informasi_label = QLabel(
            'Klik Insert untuk semua mahasiswa, kemudian klik Save jika semua telah diabsen.', self)
        layout.addWidget(self.informasi_label)

        self.result_text = QLabel(self)
        layout.addWidget(self.result_text)

        self.setLayout(layout)

    def insert_data(self):
        try:
            # Get data from UI
            Mata_Kuliah = self.matkul_combobox.currentText()
            Tanggal_Perkuliahan = QDate.currentDate().toString("yyyy-MM-dd")
            Nama = self.nama_entry.text()
            NIM = self.nim_entry.text()
            Kelas = self.kelas_entry.text()
            Jurusan = self.jurusan_entry.text()

            # Create a Contact instance
            contact = Contact(Mata_Kuliah, Tanggal_Perkuliahan, Nama, NIM, Jurusan, Kelas)

            # Save data to MySQL database
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
                INSERT INTO attendance (nama, nim, jurusan, kelas, matkul, tanggal)
                VALUES (%s, %s, %s, %s, %s, %s)
            '''
            data = (contact.Nama, contact.NIM, contact.Jurusan, contact.Kelas, contact.Mata_Kuliah, contact.Tanggal_Perkuliahan)

            self.cursor.execute(query, data)
            self.db_connection.commit()

        except Exception as e:
            QMessageBox.critical(self, 'Error', f"Failed to save contact to database: {str(e)}")
            print(f"Failed to save contact to database: {str(e)}")

    def save_data(self):
        # Your implementation for saving data
        # Provide user feedback
        QMessageBox.information(self, 'Success', "Data absen telah di save!")
        print("Data saved successfully.")

    def create_new_data(self):
        # Your implementation for creating new data
        QMessageBox.information(self, 'Information', "Create New Data")
        print("Create New Data")

    def clear_entries(self):
        # Clear all entry fields
        self.tanggal_entry.clear()
        self.nama_entry.clear()
        self.nim_entry.clear()
        self.kelas_entry.clear()
        self.jurusan_entry.clear()

    def populate_courses(self):
        # Add courses to the combo box (you may fetch them from the database)
        courses = ["PBO", "BASIS DATA", "STRUKTUR DATA", "RISET OPERASI", "BAHASA INDONESIA"]
        self.matkul_combobox.addItems(courses)

    def sort_data(self):
        try:
            # Perform sorting by class in the database
            sorted_results = self.sort_data_by_class()

            # Display the sorted results
            result_text = ""
            for result in sorted_results:
                result_text += f"{result.Nama}, {result.Jurusan}, {result.Kelas}, {result.Mata_Kuliah}, {result.Tanggal_Perkuliahan}\n"

            self.result_text.setText(result_text)

        except Exception as e:
            QMessageBox.critical(self, 'Error', f"Failed to sort data: {str(e)}")
            print(f"Failed to sort data: {str(e)}")

    def sort_data_by_class(self):
        try:
            # Perform sorting by class in the database
            query = '''
                SELECT nama, nim, jurusan, kelas, matkul, tanggal
                FROM attendance
                ORDER BY kelas
            '''

            self.cursor.execute(query)
            results = self.cursor.fetchall()

            sorted_results = []
            for result in results:
                nama, nim, jurusan, kelas, matkul, tanggal = result
                sorted_results.append(Contact(matkul, tanggal, nama, nim, jurusan, kelas))

            return sorted_results

        except Exception as e:
            QMessageBox.critical(self, 'Error', f"Failed to sort data by class: {str(e)}")
            print(f"Failed to sort data by class: {str(e)}")
            return []

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
