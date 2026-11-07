

secret_code = "1234"


for i in range(3):
    guess = input("Enter the 4-digit code: ")
    if guess == secret_code:       
       print("vault open")
       break

else:
    print("wrong code, try again")

    if guess != secret_code:
       print("wrong code, vault locked")
       
        