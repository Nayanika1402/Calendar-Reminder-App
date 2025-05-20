import calendar
from tkinter import *
from tkinter import messagebox
import datetime
import json
import os

REMINDER_FILE = "reminders.json"

# Load reminders from file
def load_reminders():
    if os.path.exists(REMINDER_FILE):
        with open(REMINDER_FILE, "r") as file:
            return json.load(file)
    return {}

# Save reminders to file
def save_reminders():
    with open(REMINDER_FILE, "w") as file:
        json.dump(reminders, file)

# Display calendar
def show_calendar(year, month):
    cal_text = calendar.month(year, month)
    cal_output.delete(1.0, END)
    cal_output.insert(INSERT, cal_text)

# Set a new reminder
def set_reminder():
    date = date_entry.get()
    reminder_text = reminder_entry.get("1.0", END).strip()
    if date and reminder_text:
        reminders[date] = reminder_text
        save_reminders()
        update_upcoming_reminders()
        messagebox.showinfo("✅ Success", f"Reminder set for {date}")
        date_entry.delete(0, END)
        reminder_entry.delete("1.0", END)
    else:
        messagebox.showwarning("⚠️ Input Error", "Please enter a valid date and reminder.")

# View a reminder
def view_reminder():
    date = date_entry.get()
    if date in reminders:
        reminder_entry.delete("1.0", END)
        reminder_entry.insert(INSERT, reminders[date])
    else:
        messagebox.showinfo("🛈 No Reminder", f"No reminder found for {date}.")

# Clear the reminder box
def clear_reminder():
    reminder_entry.delete("1.0", END)

# Show upcoming reminders
def update_upcoming_reminders():
    upcoming.delete(0, END)
    for date, text in sorted(reminders.items()):
        upcoming.insert(END, f"{date}: {text[:30]}...")

# Exit app
def exit_app():
    root.quit()

# ---------- UI SETUP ----------

root = Tk()
root.title("📅 Modern Calendar Reminder App")
root.geometry("800x600")
root.config(bg="#F4F4F9")

reminders = load_reminders()
now = datetime.datetime.now()

# Header
header = Label(root, text="📆 Calendar Reminder App", font=("Helvetica", 20, "bold"), bg="#3E64FF", fg="white", pady=15)
header.pack(fill=X)

# Main layout frame
main_frame = Frame(root, bg="#F4F4F9", pady=10)
main_frame.pack(fill=BOTH, expand=True)

# Left Column (Calendar + Date input)
left_frame = Frame(main_frame, bg="#FFF", bd=2, relief=GROOVE, padx=20, pady=20)
left_frame.pack(side=LEFT, fill=Y, padx=30, pady=20)

Label(left_frame, text="📅 Monthly Calendar", font=("Arial", 14, "bold"), bg="#FFF", fg="#333").pack()
cal_output = Text(left_frame, width=25, height=8, font=("Courier", 12), bg="#FAFAFA", bd=1, relief="solid")
cal_output.pack(pady=10)
show_calendar(now.year, now.month)

Label(left_frame, text="Today: " + now.strftime("%Y-%m-%d"), font=("Arial", 10), bg="#FFF", fg="#777").pack()

Label(left_frame, text="\nEnter Date (YYYY-MM-DD):", font=("Arial", 11), bg="#FFF", anchor="w").pack(fill=X)
date_entry = Entry(left_frame, width=20, font=("Arial", 11), bd=2, relief="groove")
date_entry.pack(pady=5)

# Right Column (Reminder + Buttons)
right_frame = Frame(main_frame, bg="#FFF", bd=2, relief=GROOVE, padx=20, pady=20)
right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=20)

Label(right_frame, text="📝 Reminder", font=("Arial", 14, "bold"), bg="#FFF", fg="#333").pack()
reminder_entry = Text(right_frame, height=5, font=("Arial", 11), bg="#F9FAFB", bd=1, relief="solid")
reminder_entry.pack(fill=X, pady=10)

# Buttons Frame
btn_frame = Frame(right_frame, bg="#FFF")
btn_frame.pack(pady=5)

Button(btn_frame, text="➕ Set Reminder", command=set_reminder, bg="#4CAF50", fg="white", font=("Arial", 11), width=15).grid(row=0, column=0, padx=5)
Button(btn_frame, text="🔍 View Reminder", command=view_reminder, bg="#2196F3", fg="white", font=("Arial", 11), width=15).grid(row=0, column=1, padx=5)
Button(btn_frame, text="❌ Clear", command=clear_reminder, bg="#FF9800", fg="white", font=("Arial", 11), width=10).grid(row=1, column=0, padx=5, pady=5)
Button(btn_frame, text="🚪 Exit", command=exit_app, bg="#f44336", fg="white", font=("Arial", 11), width=10).grid(row=1, column=1, padx=5, pady=5)

# Upcoming Reminders Section
Label(right_frame, text="📅 Upcoming Reminders", font=("Arial", 12, "bold"), bg="#FFF", anchor="w").pack(fill=X, pady=(20, 5))
upcoming = Listbox(right_frame, font=("Arial", 10), height=8, bd=1, relief="sunken", bg="#FFFDF6")
upcoming.pack(fill=BOTH, expand=True)

update_upcoming_reminders()

# Footer
Label(root, text="✨ Made with Python & Tkinter", font=("Arial", 9), bg="#F4F4F9", fg="#888").pack(pady=10)

root.mainloop()
