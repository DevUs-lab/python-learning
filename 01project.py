expensiveList = []

while True:
    print("======Main Menu======")
    print("1. Add Expense")
    print("2. See all Expense list")
    print("3. Total spend")
    print("4. Exit")

    choice = int(input("Please enter your choice: "))

    if choice == 1:
        expensive = {
            "date": input("Enter your date: "),
            "item": input("Enter item name: "),
            "description": input("Enter Description: "),
            "Price": input("Enter Price: "),
        }
        expensiveList.append(expensive)
        print("expense added successfully")

    elif choice == 2:
        if len(expensiveList) == 0:
            print("You did not spend money, or did not add any!")
        else:
            print("======Here are your expenses======")
            count = 1
            for item in expensiveList:
                print(f"kharcha no {count} ==> date: {item['date']}, item: {item['item']}, "
                      f"description: {item['description']}, price: {item['Price']}")
                count += 1

    elif choice == 3:
        if len(expensiveList) == 0:
            print("You did not spend money, or did not add any!")
        else:
            total = 0
            for expense in expensiveList:
                total = total + float(expense["Price"])
            print(f"\ntotal: {total}/-")

    elif choice == 4:
        print("thanks for choosing us")
        break

    else:
        print('Enter valid number.')