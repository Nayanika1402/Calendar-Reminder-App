import calendar
from tkinter import *
from tkinter import messagebox, ttk
import datetime
import json
import os
from tkcalendar import Calendar

REMINDER_FILE = "reminders.json"

def load_reminders():
    if os.path.exists(REMINDER_FILE):
        with open(REMINDER_FILE, "r") as file:
            return json.load(file)
    return {}

def save_reminders():
    with open(REMINDER_FILE, "w") as file:
        json.dump(reminders, file, indent=4)

def is_valid_date(date_str):
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def is_valid_time(time_str):
    if not time_str:
        return True  # allow empty
    try:
        datetime.datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

def on_date_select(event):
    date = cal.selection_get()
    date_str = date.strftime("%Y-%m-%d")
    date_entry.delete(0, END)
    date_entry.insert(0, date_str)
    show_reminder_for_date(date_str)
    if date_str in date_dropdown['values']:
        date_dropdown.set(date_str)

def on_dropdown_select(event):
    selected_date = date_dropdown.get()
    date_entry.delete(0, END)
    date_entry.insert(0, selected_date)
    cal.selection_set(datetime.datetime.strptime(selected_date, "%Y-%m-%d"))
    show_reminder_for_date(selected_date)

def show_reminder_for_date(date):
    if date in reminders:
        info = reminders[date]
        reminder_entry.delete("1.0", END)
        time_entry.delete(0, END)
        if isinstance(info, dict):
            reminder_entry.insert(INSERT, info.get("text", ""))
            time_entry.insert(0, info.get("time", ""))
            recurrence_var.set(info.get("recurrence", "None"))
        else:
            reminder_entry.insert(INSERT, str(info))
            recurrence_var.set("None")
    else:
        reminder_entry.delete("1.0", END)
        time_entry.delete(0, END)
        recurrence_var.set("None")

def set_reminder():
    date = date_entry.get()
    time = time_entry.get()
    reminder_text = reminder_entry.get("1.0", END).strip()
    recurrence = recurrence_var.get()

    if not date or not reminder_text:
        messagebox.showwarning("⚠ Input Error", "Please enter a valid date and reminder.")
        return

    if not is_valid_date(date):
        messagebox.showwarning("⚠ Input Error", "Invalid date format! Use YYYY-MM-DD.")
        return

    if not is_valid_time(time):
        messagebox.showwarning("⚠ Input Error", "Invalid time format! Use HH:MM.")
        return

    reminders[date] = {
        "text": reminder_text,
        "time": time,
        "recurrence": recurrence
    }
    save_reminders()
    update_upcoming_reminders()
    update_dropdown_values()
    messagebox.showinfo("✅ Success", f"Reminder set for {date}")

def view_reminder():
    date = date_entry.get()
    if not date:
        messagebox.showwarning("⚠ Input Error", "Please select or enter a date first.")
        return
    if not is_valid_date(date):
        messagebox.showwarning("⚠ Input Error", "Invalid date format! Use YYYY-MM-DD.")
        return
    show_reminder_for_date(date)

def delete_reminder():
    date = date_entry.get()
    if not date:
        messagebox.showwarning("⚠ Input Error", "Please select or enter a date first.")
        return
    if date in reminders:
        del reminders[date]
        save_reminders()
        update_upcoming_reminders()
        update_dropdown_values()
        reminder_entry.delete("1.0", END)
        time_entry.delete(0, END)
        recurrence_var.set("None")
        messagebox.showinfo("🗑 Deleted", f"Reminder for {date} deleted.")
    else:
        messagebox.showwarning("⚠ Error", f"No reminder found for {date}.")

def clear_reminder():
    reminder_entry.delete("1.0", END)
    time_entry.delete(0, END)
    recurrence_var.set("None")
    date_entry.delete(0, END)

def update_upcoming_reminders():
    upcoming.delete(*upcoming.get_children())
    for date, info in sorted(reminders.items()):
        if isinstance(info, dict):
            time_val = info.get("time", "")
            recurrence_val = info.get("recurrence", "None")
            text_val = info.get("text", str(info))
        else:
            time_val = ""
            recurrence_val = "None"
            text_val = str(info)
        upcoming.insert("", "end", values=(date, time_val, recurrence_val, text_val[:40]+"..."))

def update_dropdown_values():
    values = sorted(reminders.keys())
    date_dropdown['values'] = values
    if not values:
        date_dropdown.set('')

def exit_app():
    root.quit()

# ----------- UI SETUP ------------

root = Tk()
root.title("📅 Calendar Reminder App")
root.geometry("900x700")
root.config(bg="#f3e5f5")  # light purple

reminders = load_reminders()
now = datetime.datetime.now()

# Header
header = Label(root, text="📆 Calendar Reminder App", font=("Segoe UI", 24, "bold"), bg="#9575cd", fg="white", pady=15)
header.pack(fill=X)

main_frame = Frame(root, bg="#f3e5f5")
main_frame.pack(padx=10, pady=10, fill=BOTH, expand=True)

# Left frame: Calendar
left_frame = Frame(main_frame, bg="#f3e5f5")
left_frame.pack(side=LEFT, padx=(0,10))

cal = Calendar(left_frame, selectmode='day', year=now.year, month=now.month, day=now.day,
               background='#9575cd', foreground='white', selectbackground='#7e57c2', font=("Segoe UI", 12))
cal.pack()
cal.bind("<<CalendarSelected>>", on_date_select)

# Right frame: Dropdown + reminder inputs & buttons
right_frame = Frame(main_frame, bg="#f3e5f5")
right_frame.pack(side=LEFT, fill=BOTH, expand=True)

Label(right_frame, text="Select Date (Reminders):", font=("Segoe UI", 11, "bold"), bg="#f3e5f5").pack(anchor=W, pady=(0,5))

date_dropdown = ttk.Combobox(right_frame, state="readonly", font=("Segoe UI", 11), width=20)
date_dropdown.pack(anchor=W, pady=(0,10))
date_dropdown.bind("<<ComboboxSelected>>", on_dropdown_select)

form_frame = Frame(right_frame, bg="#f3e5f5")
form_frame.pack(fill=X, pady=(10,0))

Label(form_frame, text="Date (YYYY-MM-DD):", font=("Segoe UI", 11, "bold"), bg="#f3e5f5").grid(row=0, column=0, sticky=W)
date_entry = Entry(form_frame, font=("Segoe UI", 11), width=18)
date_entry.grid(row=0, column=1, sticky=W, padx=5, pady=5)

Label(form_frame, text="Time (HH:MM):", font=("Segoe UI", 11, "bold"), bg="#f3e5f5").grid(row=0, column=2, sticky=W)
time_entry = Entry(form_frame, font=("Segoe UI", 11), width=10)
time_entry.grid(row=0, column=3, sticky=W, padx=5, pady=5)

Label(form_frame, text="Recurrence:", font=("Segoe UI", 11, "bold"), bg="#f3e5f5").grid(row=0, column=4, sticky=W)
recurrence_var = StringVar(value="None")
recurrence_menu = ttk.Combobox(form_frame, textvariable=recurrence_var, values=["None", "Daily", "Weekly", "Monthly"],
                               width=12, state="readonly", font=("Segoe UI", 11))
recurrence_menu.grid(row=0, column=5, sticky=W, padx=5, pady=5)

Label(right_frame, text="Reminder Text:", font=("Segoe UI", 11, "bold"), bg="#f3e5f5").pack(anchor=W, pady=(10,2))

reminder_entry = Text(right_frame, width=45, height=10, font=("Segoe UI", 11), borderwidth=2, relief="solid")
reminder_entry.pack(fill=X, pady=(0,10))

btn_frame = Frame(right_frame, bg="#f3e5f5")
btn_frame.pack(fill=X, pady=10)

btn_set = ttk.Button(btn_frame, text="Set Reminder", command=set_reminder)
btn_set.pack(side=LEFT, expand=True, fill=X, padx=5)

btn_view = ttk.Button(btn_frame, text="View Reminder", command=view_reminder)
btn_view.pack(side=LEFT, expand=True, fill=X, padx=5)

btn_delete = ttk.Button(btn_frame, text="Delete Reminder", command=delete_reminder)
btn_delete.pack(side=LEFT, expand=True, fill=X, padx=5)

btn_clear = ttk.Button(btn_frame, text="Clear", command=clear_reminder)
btn_clear.pack(side=LEFT, expand=True, fill=X, padx=5)

btn_exit = ttk.Button(btn_frame, text="Exit", command=exit_app)
btn_exit.pack(side=LEFT, expand=True, fill=X, padx=5)

bottom_frame = Frame(root, bg="#f3e5f5")
bottom_frame.pack(padx=10, pady=10, fill=BOTH, expand=True)

Label(bottom_frame, text="Upcoming Reminders", font=("Segoe UI", 14, "bold"), bg="#f3e5f5", fg="#6a1b9a").pack(anchor=W)

tree_frame = Frame(bottom_frame, bg="#f3e5f5")
tree_frame.pack(fill=BOTH, expand=True)

upcoming = ttk.Treeview(tree_frame, columns=("Date", "Time", "Recurrence", "Reminder"), show="headings")
for col in ("Date", "Time", "Recurrence", "Reminder"):
    upcoming.heading(col, text=col)
    upcoming.column(col, width=150 if col != "Reminder" else 400, anchor=W)
upcoming.pack(fill=BOTH, expand=True)

update_upcoming_reminders()
update_dropdown_values()

root.mainloop()
