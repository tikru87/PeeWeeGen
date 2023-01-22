from tkinter import *
from tkinter import messagebox as mb
from characters import *
import random
import pyperclip
import json
import os

EMAIL_ADDRESS = ""
DATA_FILE = "data.json"
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_pw():  # generate password and copy it to clipboard
    pw_entry.delete(0, END)
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    pw_letters = [random.choice(letters) for _ in range(nr_letters)]
    pw_numbers = [random.choice(numbers) for _ in range(nr_numbers)]
    pw_symbols = [random.choice(symbols) for _ in range(nr_symbols)]

    pw_list = pw_letters + pw_numbers + pw_symbols

    random.shuffle(pw_list)

    peewee = "".join(pw_list)

    pw_entry.insert(0, peewee)
    pyperclip.copy(peewee)
# ---------------------------- SAVE PASSWORD ------------------------------- #


def create_json():  # create json file if it's not already there
    if os.path.exists(DATA_FILE):
        pass
    else:
        try:
            with open(DATA_FILE, "w") as created_file:
                json.dump("new file", created_file)
            open(DATA_FILE, "w").close()
        except OSError:
            print("Creating new file failed!")
        else:
            print("created")


def save():

    address = address_entry.get()
    email = email_entry.get()
    peewee = pw_entry.get()
    new_data = {
        address: {
            "email": email,
            "peewee": peewee,
        }
    }

    if len(address) == 0 or len(peewee) == 0:
        mb.showinfo(title="Empty fields!", message="Don't leave empty fields!")
    else:
        if os.path.getsize(DATA_FILE) == 0:  # if file is empty
            with open(DATA_FILE, "w") as file:
                json.dump(new_data, file, indent=4)
        else:  # if file already contains data
            with open(DATA_FILE, "r") as file:
                data = json.load(file)
                data.update(new_data)

            with open(DATA_FILE, "w") as file:
                json.dump(data, file, indent=4)

        address_entry.delete(0, END)
        pw_entry.delete(0, END)


def find_peewee():
    address = address_entry.get()
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            if address in data:
                email = data[address]["email"]
                peewee = data[address]["peewee"]
                mb.showinfo(title="Result", message=f"Login credentials for {address}:\n Email: {email}\n Peewee: {peewee}")
                pyperclip.copy(peewee)
            else:
                mb.showinfo(title="Result", message=f"No login credentials for {address} found!")
    except json.JSONDecodeError:
        mb.showinfo(title="Error!", message="No saved credentials!")

# ---------------------------- UI SETUP ------------------------------- #


create_json()
window = Tk()
window.title("PeeWee Manager")
window.config(padx=20, pady=20)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
address_label = Label(text="Website:")
address_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

pw_label = Label(text="Password:")
pw_label.grid(row=3, column=0)

# Entries
address_entry = Entry(width=30)
address_entry.grid(row=1, column=1, columnspan=2, sticky="w")
address_entry.focus()

email_entry = Entry(width=30)
email_entry.grid(row=2, column=1, columnspan=2, sticky="w")
email_entry.insert(0, EMAIL_ADDRESS)

pw_entry = Entry(width=30)
pw_entry.grid(row=3, column=1, sticky="w")

# Buttons
gen_btn = Button(text="Generate PeeWee", command=generate_pw, width=14)
gen_btn.grid(row=2, column=2, sticky="w")

add_btn = Button(width=14, text="Add", command=save)
add_btn.grid(row=3, column=2, sticky="w")

search_btn = Button(text="Search", width=14, command=find_peewee)
search_btn.grid(row=1, column=2, sticky="w")

window.mainloop()
