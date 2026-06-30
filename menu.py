import os
import json

class MenuItem:
    def __init__(self, name, ingredients, cost):
        self.name = name
        self.cost = cost
        self.ingredients = ingredients

class Menu:
    def __init__(self, recipe_file="Recipes.json"):
        self.recipe_file = recipe_file
        self.menu = []
        self.load_recipes()

    def load_recipes(self):
        default_menu = [
            MenuItem("espresso", {"water": 50, "milk": 0, "coffee": 20}, 105),
            MenuItem("latte", {"water": 150, "milk": 200, "coffee": 25}, 125),
            MenuItem("cappuccino", {"water": 250, "milk": 100, "coffee": 25}, 135),
            MenuItem("americano", {"water": 200, "milk": 0, "coffee": 20}, 110),
            MenuItem("hot chocolate", {"water": 200, "milk": 150, "coffee": 0}, 120),
            MenuItem("black tea", {"water": 200, "milk": 50, "coffee": 0}, 80),
        ]
        if os.path.exists(self.recipe_file):
            try:
                with open(self.recipe_file, "r") as f:
                    data = json.load(f)
                    self.menu = [
                        MenuItem(item["name"], item["ingredients"], item["cost"])
                        for item in data
                    ]
            except Exception as e:
                print(f"Error loading recipes: {e}. Using default values...")
                self.menu = default_menu
        else:
            self.menu = default_menu
            self.save_recipes()

    def save_recipes(self):
        data = [
            {"name": item.name, "ingredients": item.ingredients, "cost": item.cost}
            for item in self.menu
        ]
        try:
            with open(self.recipe_file, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving recipes: {e}")

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

    def add_or_modify_recipe_menu(self):
        while True:
            print("\nRecipe Management Menu:")
            print("1. Add a New Drink Recipe")
            print("2. Modify an Existing Drink Recipe")
            print("3. Exit Recipe Management")
            choice = input("\nChoose one: ").strip()
            if choice == "1":
                self.add_new_recipe()
            elif choice == "2":
                self.modify_recipe()
            elif choice == "3":
                break
            else:
                print("Invalid choice!")

    def add_new_recipe(self):
        print("\n--- Add a New Drink Recipe ---")
        name = input("Enter drink name: ").strip().lower()
        if not name:
            print("Name cannot be empty!")
            return
        
        for item in self.menu:
            if item.name == name:
                print(f"Drink '{name}' already exists. Use modify option to change it.")
                return

        ingredients = {}
        for ing in ["water", "milk", "coffee", "sugar"]:
            try:
                val_str = input(f"Enter quantity of {ing} (in ml/g, press Enter for 0): ").strip()
                val = int(val_str) if val_str else 0
                if val < 0:
                    print("Value cannot be negative! Setting to 0.")
                    val = 0
                if val > 0:
                    ingredients[ing] = val
            except ValueError:
                print("Invalid input! Setting to 0.")
                ingredients[ing] = 0

        try:
            cost_str = input("Enter base cost of the drink (Tk): ").strip()
            cost = int(cost_str) if cost_str else 0
            if cost <= 0:
                print("Cost must be greater than 0!")
                return
        except ValueError:
            print("Invalid cost input!")
            return

        new_item = MenuItem(name, ingredients, cost)
        self.menu.append(new_item)
        self.save_recipes()
        print(f"\nDrink '{name.capitalize()}' added successfully!")

    def modify_recipe(self):
        print("\n--- Modify an Existing Drink Recipe ---")
        for i, item in enumerate(self.menu, 1):
            print(f"{i}. {item.name.capitalize()}")
        try:
            choice = int(input("\nSelect drink to modify (number): "))
            if not (1 <= choice <= len(self.menu)):
                print("Invalid selection!")
                return
            drink = self.menu[choice - 1]
        except ValueError:
            print("Invalid selection!")
            return

        print(f"\nModifying {drink.name.capitalize()}:")
        cost_str = input(f"Current cost: Tk {drink.cost}. Enter new cost (or press Enter to keep): ").strip()
        if cost_str:
            try:
                cost = int(cost_str)
                if cost > 0:
                    drink.cost = cost
                else:
                    print("Cost must be greater than 0! Kept original cost.")
            except ValueError:
                print("Invalid input! Kept original cost.")

        print("Modifying ingredients (press Enter to keep current value):")
        for ing in ["water", "milk", "coffee", "sugar"]:
            curr = drink.ingredients.get(ing, 0)
            val_str = input(f"  {ing.capitalize()} (current: {curr}): ").strip()
            if val_str:
                try:
                    val = int(val_str)
                    if val < 0:
                        print("Value cannot be negative! Kept original.")
                    else:
                        if val > 0:
                            drink.ingredients[ing] = val
                        else:
                            if ing in drink.ingredients:
                                drink.ingredients[ing] = 0
                except ValueError:
                    print("Invalid input! Kept original.")

        self.save_recipes()
        print(f"\nDrink '{drink.name.capitalize()}' updated successfully!")