#ATM SIMULATION

keep_going = True
balance = 1000.0  # starting balance

while keep_going:
    print("\n===== ATM Menu =====")
    print("1. Check Balance")
    print("2. Withdraw Cash")
    print("3. Deposit Cash")
    
    choice = input("\nPlease enter your choice (1/2/3): ")
    
    if choice == "1":
        print(f"Your current balance is: ${balance:.2f}")
    elif choice == "2":
        amount = float(input("Enter withdrawal amount: $"))
        if amount > 0 and amount <= balance:
            balance -= amount
            print(f"Withdrew ${amount:.2f}. New balance: ${balance:.2f}")
        else:
            print("Invalid amount. Not enough money or amount must be positive.")
    elif choice == "3":
        amount = float(input("Enter deposit amount: $"))
        if amount > 0:
            balance += amount
            print(f"Deposited ${amount:.2f}. New balance: ${balance:.2f}")
        else:
            print("Deposit amount must be positive.")
    else:
        print("Invalid menu option, try again.")

    # Ask if user wants another transaction
    again = input("\nDo you want to perform another transaction? (yes/no): ")
    if again.lower() == "no":
        keep_going = False

print("\nATM session ended. Thank you!")
