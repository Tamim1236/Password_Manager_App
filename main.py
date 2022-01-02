from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
               'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_label_input.insert(END, password)

    #the following line allows for the generated password to be copied to the user's clipboard
    pyperclip.copy(password)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)


def update_json(data_info):
    with open("password_manager_data.json", "w") as data_file:
        # Saving the updated data
        json.dump(data_info, data_file, indent=4)

        website_label_input.delete(0, END)
        email_label_input.delete(0, END)
        password_label_input.delete(0, END)


def add_information():
    website = website_label_input.get()
    email = email_label_input.get()
    password = password_label_input.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }

    }

    if not website or not email or not password:
        messagebox.showwarning(title="Warning", message="You have left an entry field empty!")
    else:
        try:
            data_file = open("password_manager_data.json", "r")

        except FileNotFoundError:
            update_json(new_data)

        else:
            with open("password_manager_data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
                # Updating old data with new data
                data.update(new_data)
                update_json(data)


def search_information():
    search_term = website_label_input.get()
    try:
        data_file = open("password_manager_data.json", "r")
    except FileNotFoundError:
        messagebox.showwarning(title="Warning", message="You have not added any data to search!")
    else:
        data = json.load(data_file)
        if search_term in data:
            messagebox.showinfo(title=search_term, message=f"Username/email: {data[search_term]['email']}\n"
                                             f" Password: {data[search_term]['password']}")
        else:
            messagebox.showwarning(title="Warning", message="There is no data for this website.")


canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1, padx=10)
website_label_input = Entry(width=35)
website_label_input.grid(column=1, row=1, columnspan=1, sticky="EW")
website_label_input.focus()

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2, padx=10)
email_label_input = Entry(width=35)
email_label_input.grid(column=1, row=2, columnspan=2, sticky="EW")
email_label_input.insert(0, "example@email.com")

password_label = Label(text="Password:")
password_label.grid(column=0, row=3, padx=10)
password_label_input = Entry()
password_label_input.grid(column=1, row=3, sticky="EW")

generate_pass_button = Button(text="Generate Password", command=generate_password)
generate_pass_button.grid(column=2, row=3, sticky="EW")

add_button = Button(text="Add", command=add_information, width=35)
add_button.grid(column=1, row=4, columnspan=2, sticky="EW")

search_button = Button(text="Search", command=search_information, width=10)
search_button.grid(column=2, row=1, columnspan=1, sticky="EW")

window.mainloop()