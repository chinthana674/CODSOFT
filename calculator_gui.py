"""
Python GUI Calculator
Internship Project - CodSoft

Author: Chinthana 

Description:
This project is a Graphical User Interface (GUI) based calculator
developed using Python and Tkinter.

It is an improved version of a CLI calculator, enhanced by adding a GUI
to provide a more interactive and user-friendly experience.

Features:
- Basic arithmetic operations (+, -, *, /)
- Real calculator-style interface
- Display for results and error messages
- Backspace (undo) functionality
- Previous result reuse (ANS)
- Input validation and error handling
- Hover effects on buttons

Technologies Used:
- Python
- Tkinter (GUI Library)
"""

import tkinter as tk

# ---------------- Calculation Logic ----------------

def calculate(num1, operator, num2):
    if operator == "+":
        return num1 + num2
    elif operator == "-":
        return num1 - num2
    elif operator == "*":
        return num1 * num2
    elif operator == "/":
        if num2 == 0:
            return "Error: Cannot divide by zero"
        return num1 / num2
    else:
        return "Invalid operator"


# ---------------- Global Variables ----------------

expression = ""
previous_result = None


# ---------------- Button Functions ----------------

def press(value):
    global expression
    expression += str(value)
    display_var.set(expression)


def clear():
    global expression
    expression = ""
    display_var.set("")


def backspace():
    global expression
    expression = expression[:-1]
    display_var.set(expression)


def evaluate():
    global expression, previous_result

    try:
        for op in ["+", "-", "*", "/"]:
            if op in expression:
                num1, num2 = expression.split(op)

                num1 = float(num1)
                num2 = float(num2)

                result = calculate(num1, op, num2)

                if isinstance(result, (int, float)):
                    previous_result = result
                    result = round(result, 2)
                    display_var.set(result)
                    expression = str(result)
                else:
                    display_var.set(result)
                    expression = ""
                return

    except:
        display_var.set("Error")
        expression = ""


def use_previous():
    global expression, previous_result
    if previous_result is not None:
        expression = str(previous_result)
        display_var.set(expression)


# ---------------- Hover Effects ----------------

def on_enter(e):
    e.widget['background'] = "#555555"

def on_leave(e):
    e.widget['background'] = e.widget.default_bg


# ---------------- Window ----------------

window = tk.Tk()
window.title("Python Calculator")
window.geometry("320x460")
window.configure(bg="black")

# Keep window on top (good for screen recording)
window.attributes("-topmost", True)


# ---------------- Display ----------------

display_var = tk.StringVar()

display = tk.Entry(
    window,
    textvariable=display_var,
    font=("Arial", 24),
    bd=10,
    relief="sunken",
    justify="right"
)

display.pack(fill="both", padx=10, pady=10)


# ---------------- Button Frame ----------------

frame = tk.Frame(window, bg="black")
frame.pack()


# ---------------- Button Creator ----------------

def create_button(text, row, col, command, color):

    btn = tk.Button(
        frame,
        text=text,
        command=command,
        bg=color,
        fg="white",
        font=("Arial", 14),
        width=4,
        height=2
    )

    btn.default_bg = color

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

    btn.grid(row=row, column=col, padx=6, pady=6)


# ---------------- Number Buttons ----------------

numbers = [
    ('7',1,0), ('8',1,1), ('9',1,2),
    ('4',2,0), ('5',2,1), ('6',2,2),
    ('1',3,0), ('2',3,1), ('3',3,2),
    ('0',4,1)
]

for (num,row,col) in numbers:
    create_button(num,row,col,lambda n=num: press(n),"gray")


# ---------------- Operator Buttons ----------------

operators = [
    ('+',1,3),
    ('-',2,3),
    ('*',3,3),
    ('/',4,3)
]

for (op,row,col) in operators:
    create_button(op,row,col,lambda o=op: press(o),"orange")


# ---------------- Special Buttons ----------------

create_button("=",4,2,evaluate,"green")
create_button("C",4,0,clear,"red")
create_button("⌫",5,0,backspace,"purple")
create_button("ANS",5,1,use_previous,"blue")


# ---------------- Run Program ----------------

window.mainloop()