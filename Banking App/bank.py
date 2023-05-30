import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, filedialog
import random
import string
from PIL import ImageTk, Image


class BankingGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Banking Application')
        self.geometry('800x900')

        # Set custom background color
        self.configure(bg='#588A8A')

        self.account_number = None
        self.pin = None

        self.create_login_screen()

    def create_login_screen(self):
        valid_account = False
        valid_pin = False

        while not valid_account:
            self.account_number = simpledialog.askinteger("Account Number", "Enter your account number:")
            if self.account_number is not None:
                if len(str(self.account_number)) == 10 and isinstance(self.account_number, int):
                    valid_account = True
                else:
                    messagebox.showerror("Invalid Account Number", "Account number must be 10 digits and must not contain alphabets.")

        while not valid_pin:
            self.pin = simpledialog.askinteger("PIN", "Enter your PIN:")
            if self.pin is not None:
                if len(str(self.pin)) == 4 and isinstance(self.pin, int):
                    valid_pin = True
                else:
                    messagebox.showerror("Invalid PIN", "PIN must be 4 digits.")

        self.account = BankAccount(self.account_number, self.pin)
        self.create_main_screen()

    def create_main_screen(self):
        # Create a frame for buttons
        button_frame = tk.Frame(self, bg='white')
        button_frame.pack(pady=10)

        # Define button styles
        style = ttk.Style()
        style.configure('TButton',
                        background='yellow',
                        foreground='black',
                        padding=20)

        # Create deposit button
        deposit_button = ttk.Button(button_frame, text="Deposit", command=self.deposit)
        deposit_button.pack(side='left', padx=15, pady=15)

        # Create withdraw button
        withdraw_button = ttk.Button(button_frame, text="Withdraw", command=self.withdraw)
        withdraw_button.pack(side='left', padx=15, pady=15)

        # Create statement button
        statement_button = ttk.Button(button_frame, text="Get Statement", command=self.get_statement)
        statement_button.pack(side='left', padx=15, pady=15)

    def deposit(self):
        if self.authenticate():
            amount = simpledialog.askfloat("Deposit", "Enter the amount to deposit:")
            if amount is not None:
                try:
                    self.account.deposit(amount)
                    self.show_info_message("Deposit", "Deposit successful.")
                except ValueError as e:
                    self.show_error_message("Invalid Amount", str(e))

    def withdraw(self):
        if self.authenticate():
            amount = simpledialog.askfloat("Withdraw", "Enter the amount to withdraw:")
            if amount is not None:
                try:
                    self.account.withdraw(amount)
                    self.show_info_message("Withdrawal", "Withdrawal successful.")
                except ValueError as e:
                    self.show_error_message("Invalid Amount", str(e))

    def get_statement(self):
        if self.authenticate():
            statement = self.account.get_statement()
            self.show_info_message("Bank Statement", statement)

    def show_info_message(self, title, message):
        messagebox.showinfo(title, message)

    def show_error_message(self, title, message):
        messagebox.showerror(title, message)

    def authenticate(self):
        pin = simpledialog.askstring("Authentication", "Enter your PIN:")
        if pin == str(self.pin):
                        return True
        else:
            messagebox.showerror("Invalid PIN", "Invalid PIN")
            return False


class BankAccount:
    def __init__(self, account_number, pin):
        self.account_number = account_number
        self.pin = pin
        self.balance = 0
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"Deposit: +{amount}")

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self.balance -= amount
        self.transactions.append(f"Withdrawal: -{amount}")

    def get_statement(self):
        statement = f"Bank Statement for Account Number: {self.account_number}\n"
        statement += f"Current Balance: {self.balance}\n"
        statement += "Transactions:\n"
        for transaction in self.transactions:
            statement += f"- {transaction}\n"
        return statement


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def generate_new_password():
    entered_password = password_entry.get()
    if entered_password:
        password_label.config(text="Entered Password: " + entered_password)
    else:
        password = generate_random_password()
        password_label.config(text="Generated Password: " + password)


# Create the main window
window = tk.Tk()
window.title("Banking Application & Password Entry")
window.geometry('800x900')

# Set custom background color
window.configure(bg='#588A8A')


# Banking Application GUI
account_number = None
pin = None
account = None


def create_login_screen():
    valid_account = False
    valid_pin = False

    while not valid_account:
        account_number = simpledialog.askinteger("Account Number", "Enter your account number:")
        if account_number is not None:
            if len(str(account_number)) == 10 and isinstance(account_number, int):
                valid_account = True
            else:
                messagebox.showerror("Invalid Account Number",
                                     "Account number must be 10 digits and must not contain alphabets.")

    while not valid_pin:
        pin = simpledialog.askinteger("PIN", "Enter your PIN:")
        if pin is not None:
            if len(str(pin)) == 4 and isinstance(pin, int):
                valid_pin = True
            else:
                messagebox.showerror("Invalid PIN", "PIN must be 4 digits.")

    global account
    account = BankAccount(account_number, pin)
    create_main_screen()


def create_main_screen():
    # Create a frame for buttons
    button_frame = tk.Frame(window, bg='white')
    button_frame.pack(pady=10)

    # Define button styles
    style = ttk.Style()
    style.configure('TButton',
                    background='yellow',
                    foreground='black',
                    padding=20)

    # Create deposit button
    deposit_button = ttk.Button(button_frame, text="Deposit", command=deposit)
    deposit_button.pack(side='left', padx=15, pady=15)

    # Create withdraw button
    withdraw_button = ttk.Button(button_frame, text="Withdraw", command=withdraw)
    withdraw_button.pack(side='left', padx=15, pady=15)

    # Create statement button
    statement_button = ttk.Button(button_frame, text="Get Statement", command=get_statement)
    statement_button.pack(side='left', padx=15, pady=15)


def deposit():
    if authenticate():
        amount = simpledialog.askfloat("Deposit", "Enter the amount to deposit:")
        if amount is not None:
            try:
                account.deposit(amount)
                show_info_message("Deposit", "Deposit successful.")
            except ValueError as e:
                show_error_message("Invalid Amount", str(e))


def withdraw():
    if authenticate():
        amount = simpledialog.askfloat("Withdraw", "Enter the amount to withdraw:")
        if amount is not None:
            try:
                account.withdraw(amount)
                show_info_message("Withdrawal", "Withdrawal successful.")
            except ValueError as e:
                show_error_message("Invalid Amount", str(e))


def get_statement():
    if authenticate():
        statement = account.get_statement()
        show_info_message("Bank Statement", statement)


def show_info_message(title, message):
    messagebox.showinfo(title, message)


def show_error_message(title, message):
    messagebox.showerror(title, message)


def authenticate():
    pin = simpledialog.askstring("Authentication", "Enter your PIN:")
    if pin == str(account.pin):
        return True
    else:
        messagebox.showerror("Invalid PIN", "Invalid PIN")
        return False


# Password Generator GUI
def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def generate_new_password():
    entered_password = password_entry.get()
    if entered_password:
        password_label.config(text="Entered Password: " + entered_password)
    else:
        password = generate_random_password()
        password_label.config(text="Generated Password: " + password)


# Create the main window
window = tk.Tk()
window.title("Banking Application & Password Entry")
window.geometry('800x900')

# Set custom background color
window.configure(bg='#588A8A')


# Banking Application GUI
account_number = None
pin = None
account = None


def create_login_screen():
    valid_account = False
    valid_pin = False

    while not valid_account:
        account_number = simpledialog.askinteger("Account Number", "Enter your account number:")
        if account_number is not None:
            if len(str(account_number)) == 10 and isinstance(account_number, int):
                valid_account = True
            else:
                messagebox.showerror("Invalid Account Number",
                                     "Account number must be 10 digits and must not contain alphabets.")

    while not valid_pin:
        pin = simpledialog.askinteger("PIN", "Enter your PIN:")
        if pin is not None:
            if len(str(pin)) == 4 and isinstance(pin, int):
                valid_pin = True
            else:
                messagebox.showerror("Invalid PIN", "PIN must be 4 digits.")

    global account
    account = BankAccount(account_number, pin)
    create_main_screen()


def create_main_screen():
    # Create a frame for buttons
    button_frame = tk.Frame(window, bg='white')
    button_frame.pack(pady=10)

    # Define button styles
    style = ttk.Style()
    style.configure('TButton',
                    background='yellow',
                    foreground='black',
                    padding=20)

    # Create deposit button
    deposit_button = ttk.Button(button_frame, text="Deposit", command=deposit)
    deposit_button.pack(side='left', padx=15, pady=15)

    # Create withdraw button
    withdraw_button = ttk.Button(button_frame, text="Withdraw", command=withdraw)
    withdraw_button.pack(side='left', padx=15, pady=15)

       # Create statement button
    statement_button = ttk.Button(button_frame, text="Get Statement", command=get_statement)
    statement_button.pack(side='left', padx=15, pady=15)


def deposit():
    if authenticate():
        amount = simpledialog.askfloat("Deposit", "Enter the amount to deposit:")
        if amount is not None:
            try:
                account.deposit(amount)
                show_info_message("Deposit", "Deposit successful.")
            except ValueError as e:
                show_error_message("Invalid Amount", str(e))


def withdraw():
    if authenticate():
        amount = simpledialog.askfloat("Withdraw", "Enter the amount to withdraw:")
        if amount is not None:
            try:
                account.withdraw(amount)
                show_info_message("Withdrawal", "Withdrawal successful.")
            except ValueError as e:
                show_error_message("Invalid Amount", str(e))


def get_statement():
    if authenticate():
        statement = account.get_statement()
        show_info_message("Bank Statement", statement)


def show_info_message(title, message):
    messagebox.showinfo(title, message)


def show_error_message(title, message):
    messagebox.showerror(title, message)


def authenticate():
    pin = simpledialog.askstring("Authentication", "Enter your PIN:")
    if pin == str(account.pin):
        return True
    else:
        messagebox.showerror("Invalid PIN", "Invalid PIN")
        return False


# Password Generator GUI
def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def generate_new_password():
    entered_password = password_entry.get()
    if entered_password:
        password_label.config(text="Entered Password: " + entered_password)
    else:
        password = generate_random_password()
        password_label.config(text="Generated Password: " + password)


# Create the main window
window = tk.Tk()
window.title("Banking Application & Password Entry")
window.geometry('800x900')

# Set custom background color
window.configure(bg='#588A8A')


# Banking Application GUI
account_number = None
pin = None
account = None


def create_login_screen():
    valid_account = False
    valid_pin = False

    while not valid_account:
        account_number = simpledialog.askinteger("Account Number", "Enter your account number:")
        if account_number is not None:
            if len(str(account_number)) == 10 and isinstance(account_number, int):
                valid_account = True
            else:
                messagebox.showerror("Invalid Account Number",
                                     "Account number must be 10 digits and must not contain alphabets.")

    while not valid_pin:
        pin = simpledialog.askinteger("PIN", "Enter your PIN:")
        if pin is not None:
            if len(str(pin)) == 4 and isinstance(pin, int):
                valid_pin = True
            else:
                messagebox.showerror("Invalid PIN", "PIN must be 4 digits.")

    global account
    account = BankAccount(account_number, pin)
    create_main_screen()


def create_main_screen():
    # Create a frame for buttons
    button_frame = tk.Frame(window, bg='white')
    button_frame.pack(pady=10)

    # Define button styles
    style = ttk.Style()
    style.configure('TButton',
                    background='yellow',
                    foreground='black',
                    padding=20)

    # Create deposit button
    deposit_button = ttk.Button(button_frame, text="Deposit", command=deposit)
    deposit_button.pack(side='left', padx=15, pady=15)

    # Create withdraw button
    withdraw_button = ttk.Button(button_frame, text="Withdraw", command=withdraw)
    withdraw_button.pack(side='left', padx=15, pady=15)

    # Create statement button
    statement_button = ttk.Button(button_frame, text="Get Statement", command=get_statement)
    statement_button.pack(side='left', padx=15, pady=15)


def deposit():
    if authenticate():
        amount = simpledialog.askfloat("Deposit", "Enter the amount to deposit:")
        if amount is not None:
            try:
                account.deposit(amount)
                show_info_message("Deposit", "Deposit successful.")
            except ValueError as e:
                show_error_message("Invalid Amount", str(e))


def withdraw():
    if authenticate():
        amount = simpledialog.askfloat("Withdraw", "Enter the amount to withdraw:")
        if amount is not None:
            try:
                account.withdraw(amount)
                show_info_message("Withdrawal", "Withdrawal successful.")
            except ValueError as e:
                show_error_message("Invalid Amount", str(e))


def get_statement():
    if authenticate():
        statement = account.get_statement()
        show_info_message("Bank Statement", statement)


def show_info_message(title, message):
    messagebox.showinfo(title, message)


def show_error_message(title, message):
    messagebox.showerror(title, message)


def authenticate():
    pin = simpledialog.askstring("Authentication", "Enter your PIN:")
    if pin == str(account.pin):
        return True
    else:
        messagebox.showerror("Invalid PIN", "Invalid PIN")
        return False


# Create a frame for the password generator
password_frame = tk.Frame(window, bg='white')
password_frame.pack(pady=10)

# Create password label
password_label = tk.Label(password_frame, text="Generated Password: ", bg='white')
password_label.pack(pady=10)

# Create password entry
password_entry = ttk.Entry(password_frame, font=('Helvetica', 24))
password_entry.pack(pady=10)

# Create generate password button
generate_button = ttk.Button(password_frame, text="Generate Password", command=generate_new_password)
generate_button.pack(pady=10)


# Run the login screen
create_login_screen()

# Start the main loop
window.mainloop()
