# A FUNCTIONAL ATM MACHINE

keep_going = True
balance = 1000.0

while keep_going:
    print("\nHello, valued customer! What would you like to do today?")
    print("===== ATM Menu =====")
    print("1. Check Balance")
    print("2. Withdraw Cash")
    print("3. Deposit Cash")
    
    choice = input("\nEnter your selection: ")

    if choice == "1":
        print(f"Your current balance is: ${balance:.2f}")

    elif choice == "2":
        amount_text = input("Enter withdrawal amount: $")
        if not amount_text.isdigit():
            print("Invalid key. Please enter only numbers.")
        else:
            amount = int(amount_text)
            if amount > 0 and amount <= balance:
                balance -= amount
                print(f"Withdrew ${amount}. New balance: ${balance:.2f}")
            else:
                print("Transaction failed. Insufficient funds.")

    elif choice == "3":
        amount_text = input("Enter deposit amount: $")
        if not amount_text.isdigit():
            print("Invalid key. Please enter only numbers.")
        else:
            amount = int(amount_text)
            if amount > 0:
                balance += amount
                print(f"Deposited ${amount}. New balance: ${balance:.2f}")
            else:
                print("Invalid deposit amount.")

    else:
        print("Invalid selection, please try again.")

    again = input("\nPress 1 for another transaction, press 0 to exit: ")
    if again == "0":
        keep_going = False

print("\nATM session ended. Thank you!")
