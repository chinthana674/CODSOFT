"""
📞 Contact Book Application (GUI Version)

This project is developed as part of a Python Programming Internship.

Description:
A user-friendly Contact Book application built using Python and Tkinter
that allows users to store and manage contact details efficiently.

Features:
- Add new contacts (Name, Phone, Email, Address)
- Phone number used as a unique identifier
- 10-digit phone number validation
- View all contacts in a scrollable list
- Search contacts by name or phone number
- Update existing contact details
- Delete contacts
- Auto-fill contact details on selection
- Persistent data storage using JSON file

Technologies Used:
- Python
- Tkinter (GUI)
- JSON (File Handling)

Author: Chinthana
"""

import tkinter as tk
from tkinter import messagebox
import json
import os

FILE = "contacts.json"

# ---------------- Load Contacts ----------------
def load_contacts():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return {}

# ---------------- Save Contacts ----------------
def save_contacts():
    with open(FILE, "w") as f:
        json.dump(contacts, f, indent=4)

# ---------------- Clear Input Fields ----------------
def clear_fields():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

# ---------------- Phone Validation ----------------
def valid_phone(phone):
    return phone.isdigit() and len(phone) == 10

# ---------------- Add Contact ----------------
def add_contact():
    phone = phone_entry.get().strip()

    if not valid_phone(phone):
        messagebox.showerror("Invalid Phone", "Phone number must contain exactly 10 digits.")
        return

    if phone in contacts:
        messagebox.showwarning("Duplicate", "Phone number already exists.")
        return

    name = name_entry.get().strip()
    email = email_entry.get().strip()
    address = address_entry.get().strip()

    contacts[phone] = {
        "name": name,
        "email": email,
        "address": address
    }

    save_contacts()
    messagebox.showinfo("Success", "Contact added successfully.")

    clear_fields()
    view_contacts()

# ---------------- View Contacts ----------------
def view_contacts():
    listbox.delete(0, tk.END)

    if not contacts:
        listbox.insert(tk.END, "No contacts available.")
        return

    for phone, details in contacts.items():

        name = details.get("name", "")
        email = details.get("email", "")
        address = details.get("address", "")

        text = f"{name} | {phone}"

        if email:
            text += f" | {email}"

        if address:
            text += f" | {address}"

        listbox.insert(tk.END, text)

# ---------------- Search Contact ----------------
def search_contact():
    search = search_entry.get().strip().lower()

    listbox.delete(0, tk.END)

    for phone, details in contacts.items():
        name = details.get("name", "").lower()

        if search == phone or search == name:

            email = details.get("email", "")
            address = details.get("address", "")

            text = f"{details['name']} | {phone}"

            if email:
                text += f" | {email}"

            if address:
                text += f" | {address}"

            listbox.insert(tk.END, text)

# ---------------- Update Contact ----------------
def update_contact():
    phone = phone_entry.get().strip()

    if not valid_phone(phone):
        messagebox.showerror("Invalid Phone", "Phone number must contain exactly 10 digits.")
        return

    if phone not in contacts:
        messagebox.showerror("Error", "Contact not found.")
        return

    contacts[phone]["name"] = name_entry.get().strip()
    contacts[phone]["email"] = email_entry.get().strip()
    contacts[phone]["address"] = address_entry.get().strip()

    save_contacts()
    messagebox.showinfo("Updated", "Contact updated successfully.")

    view_contacts()

# ---------------- Delete Contact ----------------
def delete_contact():
    phone = phone_entry.get().strip()

    if phone in contacts:
        del contacts[phone]

        save_contacts()

        messagebox.showinfo("Deleted", "Contact deleted successfully.")

        clear_fields()
        view_contacts()

    else:
        messagebox.showerror("Error", "Contact not found.")

# ---------------- Select Contact From List ----------------
def select_contact(event):

    if not listbox.curselection():
        return

    selected = listbox.get(listbox.curselection())

    parts = selected.split("|")

    name = parts[0].strip()
    phone = parts[1].strip()

    details = contacts.get(phone)

    clear_fields()

    name_entry.insert(0, name)
    phone_entry.insert(0, phone)

    if details.get("email"):
        email_entry.insert(0, details["email"])

    if details.get("address"):
        address_entry.insert(0, details["address"])

# ---------------- GUI ----------------

contacts = load_contacts()

root = tk.Tk()
root.title("Contact Book")
root.geometry("500x550")

tk.Label(root, text="📞 Contact Book", font=("Arial",18,"bold")).pack(pady=10)

# -------- Input Fields --------

tk.Label(root, text="Name").pack()
name_entry = tk.Entry(root, width=40)
name_entry.pack()

tk.Label(root, text="Phone (10 digits)").pack()
phone_entry = tk.Entry(root, width=40)
phone_entry.pack()

tk.Label(root, text="Email").pack()
email_entry = tk.Entry(root, width=40)
email_entry.pack()

tk.Label(root, text="Address").pack()
address_entry = tk.Entry(root, width=40)
address_entry.pack()

# -------- Buttons --------

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Contact", width=15, command=add_contact).grid(row=0,column=0,padx=5,pady=5)
tk.Button(button_frame, text="Update Contact", width=15, command=update_contact).grid(row=0,column=1,padx=5,pady=5)
tk.Button(button_frame, text="Delete Contact", width=15, command=delete_contact).grid(row=1,column=0,padx=5,pady=5)
tk.Button(button_frame, text="View Contacts", width=15, command=view_contacts).grid(row=1,column=1,padx=5,pady=5)

# -------- Search --------

tk.Label(root, text="Search (Name or Phone)").pack(pady=5)
search_entry = tk.Entry(root, width=40)
search_entry.pack()

tk.Button(root, text="Search Contact", width=20, command=search_contact).pack(pady=5)

# -------- Contact List with Scrollbar --------

list_frame = tk.Frame(root)
list_frame.pack(pady=10)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(list_frame, width=65, yscrollcommand=scrollbar.set)
listbox.pack(side=tk.LEFT)

scrollbar.config(command=listbox.yview)

listbox.bind("<<ListboxSelect>>", select_contact)

root.mainloop()


---

# 2️⃣ Contact Book Project

```markdown
# Contact Book Project

## Description
A contact management application in Python. You can add, view, search, and delete contacts. Optional fields like email and address are also supported.

## Features
- Add, View, Search, and Delete contacts
- Stores contacts in JSON / text file
- Validates phone numbers (exactly 10 digits)
- Displays email & address if available

## How to Run
1. Install Python (preferably 3.x)
2. Run the file:
```bash
python contact_book.py

Author : Chinthana
