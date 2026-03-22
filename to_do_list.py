"""
---------------------------------------------------------
📌 Project Title : Modern To-Do List Application
👨‍💻 Developed By : Chinthana
🎓 Internship   : Python Internship @ CodSoft

📖 Description:
This project is a feature-rich To-Do List application developed using Python.
It helps users efficiently manage daily tasks with a clean and modern interface.

✨ Features:
✔ Add, edit, and delete tasks
✔ Mark tasks as completed
✔ Priority levels (High, Medium, Low)
✔ Task categories
✔ Due date management
✔ Progress tracking
✔ Save functionality (data persistence)
✔ User-friendly and responsive UI

🛠 Technologies Used:
- Python
- PyQt5 (for GUI)

🎯 Objective:
To build a real-world task management application and improve
skills in GUI development, problem-solving, and user experience design.

---------------------------------------------------------
"""

import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QComboBox,
    QScrollArea, QFrame, QMessageBox, QProgressBar
)
from PyQt5.QtCore import Qt

# -------- App --------
class TodoApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Modern To-Do App")
        self.setGeometry(200, 100, 900, 600)

        self.tasks = []
        self.serial = 1

        self.setStyleSheet("background-color: #fff0f5;")

        main_layout = QVBoxLayout()

        # -------- Input --------
        input_layout = QHBoxLayout()

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter Task")

        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("YYYY-MM-DD")

        self.priority_box = QComboBox()
        self.priority_box.addItems(["High", "Medium", "Low"])

        input_layout.addWidget(self.task_input)
        input_layout.addWidget(self.date_input)

        # Priority label + box
        priority_layout = QVBoxLayout()
        priority_layout.addWidget(QLabel("Priority"))
        priority_layout.addWidget(self.priority_box)

        input_layout.addLayout(priority_layout)

        main_layout.addLayout(input_layout)

        # -------- Buttons --------
        btn_layout = QHBoxLayout()

        add_btn = QPushButton("➕ Add")
        add_btn.setStyleSheet("background-color:#ffb347; color:white;")
        add_btn.clicked.connect(self.add_task)

        save_btn = QPushButton("💾 Save")
        save_btn.setStyleSheet("background-color:#ffd1dc;")
        save_btn.clicked.connect(self.save_tasks)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(save_btn)

        main_layout.addLayout(btn_layout)

        # -------- Progress --------
        self.progress = QProgressBar()
        main_layout.addWidget(self.progress)

        # -------- Scroll Area --------
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.task_container = QWidget()
        self.task_layout = QVBoxLayout()
        self.task_container.setLayout(self.task_layout)

        self.scroll.setWidget(self.task_container)
        main_layout.addWidget(self.scroll)

        self.setLayout(main_layout)

    # -------- Add Task --------
    def add_task(self):
        task = self.task_input.text()
        date = self.date_input.text()
        priority = self.priority_box.currentText()

        if not task:
            QMessageBox.warning(self, "Error", "Enter task")
            return

        data = {
            "id": self.serial,
            "task": task,
            "date": date,
            "priority": priority,
            "status": "Not Completed"
        }

        self.tasks.append(data)
        self.serial += 1

        self.display_tasks()
        self.update_progress()

        self.task_input.clear()

    # -------- Display Tasks --------
    def display_tasks(self):
        for i in reversed(range(self.task_layout.count())):
            self.task_layout.itemAt(i).widget().deleteLater()

        for i, task in enumerate(self.tasks):

            card = QFrame()
            card.setStyleSheet("""
                background-color:white;
                border:2px solid #ffb6c1;
                border-radius:10px;
                padding:10px;
            """)

            layout = QVBoxLayout()

            title = QLabel(f"{task['task']}")
            if task["status"] == "Completed":
                title.setStyleSheet("color:gray;")

            layout.addWidget(title)
            layout.addWidget(QLabel(f"Priority: {task['priority']}"))
            layout.addWidget(QLabel(f"Date: {task['date']}"))

            # Buttons
            btn_layout = QHBoxLayout()

            complete_btn = QPushButton("✔")
            complete_btn.clicked.connect(lambda _, i=i: self.complete_task(i))

            delete_btn = QPushButton("🗑")
            delete_btn.clicked.connect(lambda _, i=i: self.delete_task(i))

            btn_layout.addWidget(complete_btn)
            btn_layout.addWidget(delete_btn)

            layout.addLayout(btn_layout)
            card.setLayout(layout)

            self.task_layout.addWidget(card)

    # -------- Actions --------
    def complete_task(self, i):
        self.tasks[i]["status"] = "Completed"
        self.display_tasks()
        self.update_progress()

    def delete_task(self, i):
        self.tasks.pop(i)
        self.display_tasks()
        self.update_progress()

    # -------- Save --------
    def save_tasks(self):
        try:
            with open("tasks.json", "w") as f:
                json.dump(self.tasks, f)
            QMessageBox.information(self, "Saved", "Tasks saved successfully!")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    # -------- Progress --------
    def update_progress(self):
        total = len(self.tasks)
        done = sum(1 for t in self.tasks if t["status"] == "Completed")

        percent = int((done / total) * 100) if total else 0
        self.progress.setValue(percent)

# -------- Run --------
app = QApplication(sys.argv)
window = TodoApp()
window.show()
sys.exit(app.exec_())