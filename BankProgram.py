#import is used only for Captcha and Acccount Number Generation
import random
import string

balance = 0 #global balance variable

# ANSI escape codes for colors
RED = '\033[31m'
GREEN = '\033[32m'  
AQUA = '\033[36m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
UNDERLINE = '\033[4m'
RESET = '\033[0m'

#Login for existing Account
def login():
    print(f"{AQUA}Hey! Customer, welcome to HDFC Bank.{RESET}\n")
    global customer_name
    global account_number
    global pin_number
    customer_name = input(f"{BLUE}Enter your good name, please: {RESET}")
    print(f"Hey {customer_name}, Welcome to Bank Program {AQUA}{UNDERLINE}Made By Sagar{RESET}\n")

    while True:
        account_number = input(f"{BLUE}Enter the account number: {RESET}")
        if len(account_number) == 10 and account_number.isdigit():
            break
        else:
            print(f"{RED}Please enter a 10-digit account number.{RESET}\n")
            continue

    while True:
        pin_number = input(f"{BLUE}Enter the account PIN (Numeric): {RESET}")
        print("\n")
        if len(pin_number) == 4 and pin_number.isdigit():
            break
        else:
            print(f"{RED}Please enter a 4-digit PIN.{RESET}\n")
            continue

    print(f"{GREEN}Login Successfully.....{RESET}")

#Create New Account
def create_account():
    while True:
        try:
            print(f"{GREEN}Creating a new account.{RESET}\n")
            name = input(f"{BLUE}Enter your name: {RESET}")
            
            # Phone number validation
            phone = input(f"{BLUE}Enter your phone number: {RESET}")
            if len(phone) == 10 and phone.isdigit():
                pass
            else:
                print(f"{RED}Phone number is not valid. It must be a 10-digit numeric value.{RESET}")
                continue

            # Aadhaar number validation
            aadhar_no = input(f"{BLUE}Enter your Aadhaar number: {RESET}")
            if len(aadhar_no) == 12 and aadhar_no.isdigit():
                pass
            else:
                print(f"{RED}Aadhaar number is not valid. It must be a 12-digit numeric value.{RESET}")
                continue
            
            # Captcha Validation
            captcha_text = generate_captcha()
            print(f"Generated CAPTCHA is :{AQUA}{captcha_text}{RESET}")
            validate_captcha = input(f"{BLUE}Enter the generated CAPTCHA: {RESET}")
            if captcha_text == validate_captcha:
                print(f"{GREEN}CAPTCHA validated successfully.{RESET}\n") 
            else:
                print(f"{RED}Invalid CAPTCHA. Please try again.{RESET}\n")
                continue

            # Account Number Validation
            generate_account_number(length=10)
            
            # Pin setup
            pin_number = input(f"{BLUE}Set The Account Pin: {RESET}")
            if len(str(pin_number)) == 4 and str(pin_number).isdigit():
                print(f"{GREEN}Pin set successfully.{RESET}\n")
                print(f"{GREEN}Account created successfully with a balance of 0.{RESET}")
            else:
                print(f"{RED}Error:Pin Not Set{RESET}")
                continue
            break
        except Exception as e:
            print(f"{RED}An error occurred while creating the account: {e}{RESET}")

#Account Number Generation
def generate_account_number(length=10):
    characters = string.digits
    account_number = ''.join(random.choice(characters) for _ in range(length))
    
    print(f"{BLUE}Generated Account Number:{RESET}{YELLOW}{account_number}{RESET}")

#CAPTCHA generator
def generate_captcha(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

#Store Data in file(Name, Account Number, Pin)
def datastore():
    global filename
    filename = "bankdata.txt"
    try:
        with open(filename, "a") as file:
            file.write("\n")
            file.write(f"*  Account holder's Name: {customer_name}\n")
            file.write(f"   Account No: {account_number}\n")
            file.write(f"   PIN number: {pin_number}\n")
            file.write("\n")
        print(f"{GREEN}Account details stored successfully.{RESET}")
    except Exception as e:
        print(f"{RED}Error: Could not write to file.{e}{RESET}")

#Transactions Store in file
def log_transaction(transaction_type, amount):
    global balance
    try:
        with open("bankdata.txt", "a") as file:
            file.write(f"{transaction_type} of {amount} | Balance: {balance}\n")
        print(f"{GREEN}{transaction_type} logged successfully.{RESET}\n")
    except Exception as e:
        print(f"{RED}Error logging transaction: {e}{RESET}")

#Withdraw Money Function
def withdraw():
    global balance
    try:
        withdraw_amount = int(input("\nEnter amount to withdraw: "))
        if withdraw_amount <= 0:
            print(f"{RED}Invalid amount. Please enter a positive number.{RESET}")
        elif withdraw_amount > balance:
            print(f"{RED}Insufficient funds.{RESET}")
        else:
            balance -= withdraw_amount
            print(f"{GREEN}{withdraw_amount} has been withdrawn.{RESET}")
            log_transaction("Withdrawal", withdraw_amount)
        display_balance()
    except ValueError:
        print(f"{RED}Error: Please enter a valid amount.{RESET}")

#Deposite Money Function
def deposit():
    global balance
    try:
        deposit_amount = int(input("\nEnter amount to deposit: "))
        if deposit_amount <= 0:
            print(f"{RED}Invalid amount. Please enter a positive number.{RESET}")
        else:
            balance += deposit_amount
            print(f"{GREEN}{deposit_amount} has been deposited.{RESET}")
            log_transaction("Deposit", deposit_amount)
        display_balance()
    except ValueError:
        print(f"{RED}Error: Please enter a valid amount.{RESET}")

#For Displaying balance Function
def display_balance():
    print(f"Total balance is {balance}")

#Main function
def main():
    while True:
        print(f"\n{YELLOW}^^^^^^^^^^^^^^^^^^^^^^")
        print(f"1. Create Account.")
        print(f"2. Log in Existing Account.")
        print(f"3. Exit")
        print(f"**********************{RESET}")
        global choice
        try:
            choice = int(input("Enter your choice (1-3): "))

            if choice == 1:
                create_account()
            elif choice == 2:
                login()
                datastore()
                while True:
                    print(f"\n{YELLOW}^^^^^^^^^^^^^^^^^^^^^^")
                    print("1. Withdraw Money")
                    print("2. Deposit Money")
                    print("3. Show Balance")
                    print("4. Exit")
                    print(f"**********************{RESET}")

                    fill_choice = int(input("Enter your choice (1-4):"))
                    if fill_choice == 1:
                        withdraw()
                    elif fill_choice == 2:
                        deposit()
                    elif fill_choice == 3:
                        display_balance()
                    elif fill_choice == 4:
                        print(f"{GREEN}Exiting the Bank. Thank you! for Transactions...{RESET}")
                        return 0
                    else:
                        print(f"{RED}Invalid choice. Please choose a valid option.{RESET}")
            elif choice == 3:
                print(f"{GREEN}Exiting the Bank. Thank you! for Transactions...{RESET}")
                break
            else:
                print(f"{RED}Invalid choice. Please choose between 1 and 3.{RESET}")
        except ValueError:
            print(f"{RED}Please enter a valid choice.{RESET}")

if __name__ == "__main__":
    main() #Calling Main Function
