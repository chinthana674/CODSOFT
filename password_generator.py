"""
🔐 Password Generator PRO

Developed as part of a Python Internship project.

This application is a secure and user-friendly password generator
built using PyQt. It includes advanced features such as:

• Master login system with authentication
• Forgot password functionality using security question
• Strong password generation with customizable options
• Password strength indicator
• Encrypted password storage using cryptography
• Copy to clipboard and export functionality
• Password history management

This project demonstrates skills in:
- Python programming
- GUI development using PyQt
- Secure data handling (hashing & encryption)
- Designing real-world applications

Author: Chinthana
"""

import sys
import os
import hashlib
import random
import string

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QLineEdit, QMessageBox, QSlider, QCheckBox,
    QListWidget, QProgressBar, QHBoxLayout,
    QRadioButton, QButtonGroup, QInputDialog
)
from PyQt5.QtCore import Qt
from cryptography.fernet import Fernet


# ------------------- FILES -------------------
MASTER_FILE = "master.key"
SECURITY_FILE = "security.key"
KEY_FILE = "key.key"
DATA_FILE = "passwords.dat"


# ------------------- HASH -------------------
def hash_data(data):
    return hashlib.sha256(data.encode()).hexdigest()


# ------------------- MASTER + SECURITY -------------------
def save_master_data(password, question, answer):
    with open(MASTER_FILE, "w") as f:
        f.write(hash_data(password))

    with open(SECURITY_FILE, "w") as f:
        f.write(question + "\n")
        f.write(hash_data(answer))


def verify_password(password):
    if not os.path.exists(MASTER_FILE):
        return False
    with open(MASTER_FILE, "r") as f:
        return f.read() == hash_data(password)


def get_security_question():
    if not os.path.exists(SECURITY_FILE):
        return None
    with open(SECURITY_FILE, "r") as f:
        return f.read().splitlines()[0]


def verify_answer(answer):
    with open(SECURITY_FILE, "r") as f:
        stored = f.read().splitlines()[1]
    return stored == hash_data(answer)


# ------------------- ENCRYPTION -------------------
def generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)


def load_key():
    with open(KEY_FILE, "rb") as f:
        return f.read()


def save_password_encrypted(password):
    f = Fernet(load_key())
    encrypted = f.encrypt(password.encode())

    with open(DATA_FILE, "ab") as file:
        file.write(encrypted + b"\n")


# ------------------- LOGIN WINDOW -------------------
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Secure Login")
        self.setGeometry(300, 200, 320, 250)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("🔐 Enter Master Password"))

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.handle_login)
        layout.addWidget(login_btn)

        forgot_btn = QPushButton("Forgot Password?")
        forgot_btn.clicked.connect(self.forgot_password)
        layout.addWidget(forgot_btn)

        self.setLayout(layout)
        self.setStyleSheet("background-color:#E6E6FA;")

    def handle_login(self):
        pwd = self.password.text()

        if not os.path.exists(MASTER_FILE):
            self.setup_master()
            return

        if verify_password(pwd):
            self.open_main()
        else:
            QMessageBox.warning(self, "Error", "Wrong password!")

    def setup_master(self):
        pwd, ok1 = QInputDialog.getText(self, "Set Password", "Create Master Password:", QLineEdit.Password)
        if not ok1 or not pwd:
            return

        question, ok2 = QInputDialog.getText(self, "Security Question", "Enter a security question:")
        if not ok2 or not question:
            return

        answer, ok3 = QInputDialog.getText(self, "Answer", "Enter answer:", QLineEdit.Password)
        if not ok3 or not answer:
            return

        save_master_data(pwd, question, answer)
        QMessageBox.information(self, "Success", "Setup complete!")
        self.open_main()

    def forgot_password(self):
        question = get_security_question()

        if not question:
            QMessageBox.warning(self, "Error", "No security question set!")
            return

        answer, ok = QInputDialog.getText(self, "Verify", question, QLineEdit.Password)
        if not ok:
            return

        if verify_answer(answer):
            new_pwd, ok2 = QInputDialog.getText(self, "Reset", "Enter new password:", QLineEdit.Password)
            if ok2 and new_pwd:
                save_master_data(new_pwd, question, answer)
                QMessageBox.information(self, "Success", "Password reset!")
        else:
            QMessageBox.warning(self, "Error", "Wrong answer!")

    def open_main(self):
        self.main = PasswordGenerator()
        self.main.show()
        self.close()


# ------------------- MAIN APP -------------------
class PasswordGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Generator PRO")
        self.setGeometry(100, 100, 400, 650)
        self.history = []

        generate_key()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("🔐 Password Generator"))

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(4, 30)
        self.slider.setValue(10)

        self.length_label = QLabel("Length: 10")
        self.slider.valueChanged.connect(
            lambda: self.length_label.setText(f"Length: {self.slider.value()}")
        )

        layout.addWidget(self.length_label)
        layout.addWidget(self.slider)

        # Strength
        self.group = QButtonGroup(self)
        self.weak = QRadioButton("Weak")
        self.medium = QRadioButton("Medium")
        self.strong = QRadioButton("Strong")
        self.strong.setChecked(True)

        self.group.addButton(self.weak)
        self.group.addButton(self.medium)
        self.group.addButton(self.strong)

        layout.addWidget(self.weak)
        layout.addWidget(self.medium)
        layout.addWidget(self.strong)

        # Options
        self.no_repeat = QCheckBox("No Repeat")
        layout.addWidget(self.no_repeat)

        # Generate
        gen_btn = QPushButton("Generate Password")
        gen_btn.clicked.connect(self.generate_password)
        layout.addWidget(gen_btn)

        # Output
        self.output = QLineEdit()
        self.output.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.output)

        self.show_checkbox = QCheckBox("Show Password 👁️")
        self.show_checkbox.stateChanged.connect(self.toggle_password)
        layout.addWidget(self.show_checkbox)

        # Buttons
        btn_layout = QHBoxLayout()

        copy_btn = QPushButton("Copy")
        copy_btn.clicked.connect(self.copy_password)

        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_password)

        clear_hist_btn = QPushButton("Clear History")
        clear_hist_btn.clicked.connect(self.clear_history)

        export_btn = QPushButton("Export")
        export_btn.clicked.connect(self.export_passwords)

        btn_layout.addWidget(copy_btn)
        btn_layout.addWidget(clear_btn)
        btn_layout.addWidget(clear_hist_btn)
        btn_layout.addWidget(export_btn)

        layout.addLayout(btn_layout)

        # Progress
        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        # History
        self.history_list = QListWidget()
        layout.addWidget(self.history_list)

        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget { background-color: #E6E6FA; font-family: Arial; }
            QPushButton { background:#9370DB; color:white; padding:6px; border-radius:6px; }
            QPushButton:hover { background:#7B68EE; }
            QLineEdit, QListWidget { background:white; padding:5px; border-radius:5px; }
        """)

    def get_chars(self):
        if self.weak.isChecked():
            return string.ascii_lowercase, 30
        elif self.medium.isChecked():
            return string.ascii_letters + string.digits, 60
        else:
            return string.ascii_letters + string.digits + string.punctuation, 100

    def generate_password(self):
        length = self.slider.value()
        chars, strength = self.get_chars()

        if self.no_repeat.isChecked() and length > len(set(chars)):
            QMessageBox.warning(self, "Error", "Too long for unique chars!")
            return

        password = (
            "".join(random.sample(chars, length))
            if self.no_repeat.isChecked()
            else "".join(random.choice(chars) for _ in range(length))
        )

        self.output.setText(password)
        self.progress.setValue(strength)

        self.history.append(password)
        self.history_list.clear()
        self.history_list.addItems(self.history[-10:])

        save_password_encrypted(password)

    def toggle_password(self):
        self.output.setEchoMode(
            QLineEdit.Normal if self.show_checkbox.isChecked() else QLineEdit.Password
        )

    def copy_password(self):
        QApplication.clipboard().setText(self.output.text())
        QMessageBox.information(self, "Copied", "Password copied!")

    def clear_password(self):
        self.output.clear()

    def clear_history(self):
        self.history.clear()
        self.history_list.clear()
        QMessageBox.information(self, "Cleared", "History cleared!")

    def export_passwords(self):
        with open("export.txt", "w") as f:
            for pwd in self.history:
                f.write(pwd + "\n")
        QMessageBox.information(self, "Exported", "Saved to export.txt")


# ------------------- RUN -------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())