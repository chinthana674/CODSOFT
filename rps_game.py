'''# ------------------------------------------------------------
# Project: AI Rock-Paper-Scissors Game
#
# Description:
# This is a GUI-based Rock-Paper-Scissors game developed using
# Python and PyQt5. The game features an intelligent AI opponent
# that learns from user choices and predicts future moves.
#
# Features:
# - Interactive GUI using PyQt5
# - Smart AI based on user move patterns
# - Real-time score tracking
# - Reset game functionality
# - User-friendly design
#
# Author: Chinthana 
# Internship: CodSoft Python Internship
# ------------------------------------------------------------
'''
import sys
import random
from collections import Counter

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class SmartRPS(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Rock-Paper-Scissors")
        self.setGeometry(300, 200, 500, 500)

        # Scores
        self.user_score = 0
        self.computer_score = 0

        # AI memory
        self.user_history = []

        self.init_ui()

    # ---------------- BUTTON SETUP ---------------- #
    def setup_button(self, button, text):
        button.setText(text)
        button.setFixedSize(130, 130)
        button.setFont(QFont("Arial", 11, QFont.Bold))

    # ---------------- UI ---------------- #
    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("🤖 AI Rock - Paper - Scissors")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(title)

        # Instruction
        self.info_label = QLabel("Choose your move")
        self.info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.info_label)

        # Buttons
        btn_layout = QHBoxLayout()

        self.rock_btn = QPushButton()
        self.paper_btn = QPushButton()
        self.scissors_btn = QPushButton()

        self.setup_button(self.rock_btn, "🪨 Rock")
        self.setup_button(self.paper_btn, "📄 Paper")
        self.setup_button(self.scissors_btn, "✂️ Scissors")

        self.rock_btn.clicked.connect(lambda: self.play("Rock"))
        self.paper_btn.clicked.connect(lambda: self.play("Paper"))
        self.scissors_btn.clicked.connect(lambda: self.play("Scissors"))

        btn_layout.addWidget(self.rock_btn)
        btn_layout.addWidget(self.paper_btn)
        btn_layout.addWidget(self.scissors_btn)

        layout.addLayout(btn_layout)

        # Result
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.result_label)

        # Score
        self.score_label = QLabel("You: 0 | Computer: 0")
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(self.score_label)

        # Reset
        self.reset_btn = QPushButton("🔄 Reset Game")
        self.reset_btn.clicked.connect(self.reset_game)
        layout.addWidget(self.reset_btn)

        self.setLayout(layout)

        # Styling
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: white;
            }

            QPushButton {
                border-radius: 15px;
                background-color: #2e2e3e;
                padding: 10px;
            }

            QPushButton:hover {
                background-color: #4e8cff;
            }

            QPushButton:pressed {
                background-color: #3461c1;
            }

            QLabel {
                margin: 10px;
            }
        """)

    # ---------------- AI LOGIC ---------------- #
    def smart_computer_choice(self):
        choices = ["Rock", "Paper", "Scissors"]

        if len(self.user_history) < 3:
            return random.choice(choices)

        most_common = Counter(self.user_history).most_common(1)[0][0]

        if most_common == "Rock":
            return "Paper"
        elif most_common == "Paper":
            return "Scissors"
        else:
            return "Rock"

    # ---------------- GAME LOGIC ---------------- #
    def play(self, user_choice):
        self.user_history.append(user_choice)

        computer_choice = self.smart_computer_choice()

        result = self.get_result(user_choice, computer_choice)

        if result == "You Win!":
            self.user_score += 1
        elif result == "Computer Wins!":
            self.computer_score += 1

        self.result_label.setText(
            f"You: {user_choice} | AI: {computer_choice}\n\n{result}"
        )

        self.score_label.setText(
            f"You: {self.user_score} | Computer: {self.computer_score}"
        )

    def get_result(self, user, computer):
        if user == computer:
            return "It's a Tie!"

        elif (user == "Rock" and computer == "Scissors") or \
             (user == "Paper" and computer == "Rock") or \
             (user == "Scissors" and computer == "Paper"):
            return "You Win!"
        else:
            return "Computer Wins!"

    # ---------------- RESET ---------------- #
    def reset_game(self):
        self.user_score = 0
        self.computer_score = 0
        self.user_history.clear()

        self.score_label.setText("You: 0 | Computer: 0")
        self.result_label.setText("Game Reset! Play again.")
        self.info_label.setText("Choose your move")


# ---------------- MAIN ---------------- #
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SmartRPS()
    window.show()
    sys.exit(app.exec_())


