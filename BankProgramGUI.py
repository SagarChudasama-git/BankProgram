from customtkinter import *
from tkinter import *
from tkinter import ttk
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from tkinter import messagebox

set_appearance_mode("System")
set_default_color_theme("blue")

balance = 0
account_no = "1234567890"

def bank_window():
    global balance

    root = CTk()
    root.geometry("800x500")
    root.minsize(800, 500)
    root.maxsize(800, 500)
    root.title("Bank Program")

    def log_transaction(transaction_type, amount):
        date = datetime.now().strftime("%d-%m-%Y %H:%M")
        tree.insert("", "end", values=(account_no, date, transaction_type, f"₹ {amount}"))

    def deposite_win():
        global balance
        rootd = Toplevel(root)
        rootd.title("Deposit Money")
        rootd.geometry("300x200")

        Label(rootd, text="Enter Amount to Deposit", font=("Helvetica", 12)).pack(pady=10)
        amount_entry = Entry(rootd, font=("Helvetica", 12))
        amount_entry.pack(pady=5)
        message_label = Label(rootd, text="", fg="red", font=("Helvetica", 10))
        message_label.pack(pady=5)

        def submit_deposit():
            nonlocal message_label
            global balance
            try:
                deposit_amount = int(amount_entry.get())
                if deposit_amount <= 0:
                    message_label.config(text="Enter a positive amount.")
                else:
                    balance += deposit_amount
                    message_label.config(text=f"₹ {deposit_amount} deposited.", fg="green")
                    log_transaction("Deposit", deposit_amount)
                    rootd.after(1000, rootd.destroy)
            except ValueError:
                message_label.config(text="Enter a valid number.")

        Button(rootd, text="Deposit", command=submit_deposit, bg="#0087f2", fg="white", font=("Helvetica", 12)).pack(pady=20)

    def withdraw_win():
        global balance
        rootw = Toplevel(root)
        rootw.title("Withdraw Money")
        rootw.geometry("300x200")

        Label(rootw, text="Enter Amount to Withdraw", font=("Helvetica", 12)).pack(pady=10)
        amount_entry = Entry(rootw, font=("Helvetica", 12))
        amount_entry.pack(pady=5)
        message_label = Label(rootw, text="", fg="red", font=("Helvetica", 10))
        message_label.pack(pady=5)

        def submit_withdraw():
            nonlocal message_label
            global balance
            try:
                withdraw_amount = int(amount_entry.get())
                if withdraw_amount <= 0:
                    message_label.config(text="Enter a positive amount.")
                elif withdraw_amount > balance:
                    message_label.config(text="Insufficient balance.")
                else:
                    balance -= withdraw_amount
                    message_label.config(text=f"₹ {withdraw_amount} withdrawn.", fg="green")
                    log_transaction("Withdraw", withdraw_amount)
                    rootw.after(1000, rootw.destroy)
            except ValueError:
                message_label.config(text="Enter a valid number.")

        Button(rootw, text="Withdraw", command=submit_withdraw, bg="red", fg="white", font=("Helvetica", 12)).pack(pady=20)

    def showbal():
        rootsb = Toplevel(root)
        rootsb.title("Show Balance")
        rootsb.geometry("300x200")

        Label(rootsb, text="Your Current Balance is:", font=("Helvetica", 12)).pack(pady=20)
        bal_label = Label(rootsb, text=f"₹ {balance}", font=("Helvetica", 16, "bold"), fg="green")
        bal_label.pack(pady=10)


    def generate_passbook():
        if balance == 0:
            messagebox.showerror("Error", "Please Do Entries in the Bank") 
        else:
            c = canvas.Canvas("Passbook.pdf", pagesize=A4)
            width, height = A4
            y = height - 50  # Start 50px from top

            c.setFont("Helvetica-Bold", 16)
            c.drawString(200, y, "Bank Passbook")
            y -= 40

            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "Account No")
            c.drawString(150, y, "Date & Time")
            c.drawString(300, y, "Transaction")
            c.drawString(400, y, "Amount")
            y -= 20
            c.line(50, y, 500, y)
            y -= 20

            c.setFont("Helvetica", 12)

            for child in tree.get_children():
                if y < 50:  # New page if space runs out
                    c.showPage()
                    y = height - 50

                values = tree.item(child)["values"]
                c.drawString(50, y, str(values[0]))
                c.drawString(150, y, str(values[1]))
                c.drawString(300, y, str(values[2]))
                c.drawString(400, y, str(values[3]))
                y -= 20

            c.save()
            messagebox.showinfo("Success", "Passbook generated as 'Passbook.pdf'")


    HeaderLabel = CTkLabel(root, text="Bank Program", fg_color="#0087f2", font=('Helvetica', 20), text_color="white", height=45, width=800)
    HeaderLabel.pack()

    box = CTkFrame(root, width=300, height=180, fg_color="lightblue")
    box.place(x=7, y=50)

    box2 = CTkFrame(root, width=480, height=180, fg_color="lightblue")
    box2.place(x=314, y=50)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background="lightblue",
                    foreground="black",
                    fieldbackground="lightblue",
                    rowheight=30)
    style.map('Treeview', background=[('selected', '#1f538d')])

    global tree
    tree = ttk.Treeview(root, columns=("Account No", "Date", "Transaction", "Money"), show="headings", height=5)
    tree.heading("Account No", text="Account No")
    tree.heading("Date", text="Date")
    tree.heading("Transaction", text="Transaction")
    tree.heading("Money", text="Money")

    tree.column("Account No", width=150)
    tree.column("Date", width=150)
    tree.column("Transaction", width=150)
    tree.column("Money", width=150)

    tree.place(x=7, y=240, width=785, height=250)

    func_lab = Label(box2, text="Functions", padx=200, pady=30, font=("Helvetica", 12), background="lightblue")
    func_lab.pack(pady=10)

    button_frame = Frame(box2, background="lightblue")
    button_frame.pack(pady=10)

    gen_pass = CTkButton(box, text="Generate Passbook", text_color="white", height=180, width=300, command=generate_passbook)
    gen_pass.pack()

    d_but = CTkButton(button_frame, text="Deposit", text_color="white", height=58, command=deposite_win)
    d_but.pack(side=LEFT, padx=5)

    w_but = CTkButton(button_frame, text="Withdraw", text_color="white", height=58, command=withdraw_win)
    w_but.pack(side=LEFT, padx=5)

    sb_but = CTkButton(button_frame, text="Show Balance", text_color="white", height=58, command=showbal)
    sb_but.pack(side=LEFT, padx=5)

    root.mainloop()

bank_window()

# def login_window():
#     def login_event():
#         if entry_1.get() == "BankCustomer" and entry_2.get() == "2007":
#             root_login.destroy()
#             bank_window()
#         else:
#             entry_1.configure(text_color="red")
#             entry_2.configure(text_color="red")
#             print("Wrong password/username!")

#     root_login = CTk()
#     root_login.geometry(f"{500}x{500}")
#     root_login.title("Login Bank")

#     Username = "BankCustomer"
#     Password = 2007

#     frame = CTkFrame(master=root_login, width=450, height=450, corner_radius=10)
#     frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

#     label_1 = CTkLabel(master=frame, width=400, height=60, corner_radius=10,
#                                      fg_color=("gray70", "gray35"),
#                                      text=f"Please Login! \nHint: Username={Username}, Pass={Password}")
#     label_1.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

#     entry_1 = CTkEntry(master=frame, corner_radius=20, width=400, placeholder_text="Username")
#     entry_1.place(relx=0.5, rely=0.52, anchor=tkinter.CENTER)

#     entry_2 = CTkEntry(master=frame, corner_radius=20, width=400, show="*", placeholder_text="Password")
#     entry_2.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

#     button_login = CTkButton(master=frame, text="LOGIN", corner_radius=6, command=login_event, width=400)
#     button_login.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

#     root_login.mainloop()

# login_window()
