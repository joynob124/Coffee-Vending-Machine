class MenuItem:
    def __init__(self, name, ingredients, cost):
        self.name = name
        self.cost = cost
        self.ingredients = ingredients

class Menu:
    def __init__(self):
        self.menu = [
            MenuItem("espresso", {"water": 50, "milk": 0, "coffee": 20}, 105),
            MenuItem("latte", {"water": 150, "milk": 200, "coffee": 25}, 125),
            MenuItem("cappuccino", {"water": 250, "milk": 100, "coffee": 25}, 135),
            MenuItem("americano", {"water": 200, "milk": 0, "coffee": 20}, 110),
            MenuItem("hot chocolate", {"water": 200, "milk": 150, "coffee": 0}, 120),
            MenuItem("black tea", {"water": 200, "milk": 50, "coffee": 0}, 80),
        ]

    def show_menu(self):
        print("\nAVAILABLE DRINKS")
        print("=" * 40)
        for i, item in enumerate(self.menu, 1):
            print(f"{i}. {item.name.capitalize():<15} - Tk {item.cost}")
        print("=" * 40)

    def choose_multiple_drinks(self):
        orders = []
        self.show_menu()
        print("\nChoose your drink(s). Type 0 when done.\n")
        while True:
            try:
                choice = int(input("\nSelect your drink(s) (number): "))
                if choice == 0:
                    if len(orders) == 0:
                        print("Please choose at least one drink to proceed...")
                        continue
                    break
                if 1 <= choice <= len(self.menu):
                    drink = self.menu[choice - 1]
                    try:
                        qty = int(input(f"How many {drink.name.capitalize()} do you want? "))
                        if qty <= 0:
                            print("Quantity must be at least 1!")
                            continue
                        orders.append({"drink": drink, "quantity": qty})
                        print(f" Added: {qty} x {drink.name.capitalize()}")
                    except ValueError:
                        print("Please enter a valid number!")
                else:
                    print("Invalid drink number!")
            except ValueError:
                print("Please enter a number!")
        return orders


    def choose_option(self, options, question):
        print(f"\n{question}")
        print("-" * 30)
        for i, opt in enumerate(options, 1):
            print(f"{i}. {opt}")
        print("-" * 30)
        while True:
            try:
                choice = int(input("Choose a number: "))
                if 1 <= choice <= len(options):
                    return options[choice - 1]
                else:
                    print("Invalid number!")
            except ValueError:
                print("Please enter a number!")

    def choose_size_with_price(self, sizes, question, base_cost):
        print(f"\n{question}")
        print("-" * 40)
        multipliers = {
            "Small": 0.7,
            "Regular": 1.0,
            "Large": 1.4
        }
        for i, size in enumerate(sizes, 1):
            price = int(base_cost * multipliers[size])
            print(f"{i}. {size:<8} - Tk {price}")
        print("-" * 40)
        while True:
            try:
                choice = int(input("Choose size: "))
                if 1 <= choice <= len(sizes):
                    selected_size = sizes[choice - 1]
                    final_price = int(base_cost * multipliers[selected_size])
                    return selected_size, final_price
                else:
                    print("Invalid number!")
            except ValueError:
                print("Please enter a number!")