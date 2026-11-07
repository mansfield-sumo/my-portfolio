keep_going = True

while keep_going == True:
    num1 = float(input("Enter first number"))
    num2 = float(input("Enter a second number"))
    operation = input("Enter operation ( +, -, *, /)")

    if operation == "+":
       result= num1 + num2
       print(result)

    elif operation == "-":
       result = num1 - num2
       print(result)

    elif operation == "*":
       result = num1 * num2
       print(result)

    elif operation == "/":
       result = num1 / num2
       print(result)


    answer = input("Do you want to do another calculation? (yes/no): ")

    if answer.lower() == "no":
       keep_going = False