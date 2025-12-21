import os
import json
from menu import Menu
from coffee_machine import CoffeeMachine
from money_calculation import MoneyCalculation
import time

Admin_pass = "admin123"
data_file = "Sales Data.json"
def load_data():
    if os.path.exists(data_file):
        try:
            with open(data_file, 'r') as f:
                data = json.load(f)
                coffee_maker.resources = data.get("resources",coffee_maker.resources)
                coffee_maker.sales_count = data.get("sales",coffee_maker.sales_count)
                money_calculation.profit = data.get("profit",money_calculation.profit)
                print("\n")
        except:
            print("Data file not found. Starting again...\n")
def save_data():
    data = {
        "resources": coffee_maker.resources,
        "sales_count": coffee_maker.sales_count,
        "profit": money_calculation.profit
    }
    with open(data_file, "w") as f:
        json.dump(data, f, indent=4)

menu = Menu()
coffee_maker = CoffeeMachine()
money_calculation = MoneyCalculation()

load_data()

print("=" * 30)
print("   COFFEE VENDING MACHINE")
print("=" * 30 + "\n")
while True:
    entry = input("Type 'start' to proceed...  ").lower()
    if entry == "report":
        admin_entry = input("Enter password : ")
        if admin_entry == Admin_pass:
            print("\nAdmin\n")
            while True:
                print("Admin Options:")
                print("1. View Resources Report")
                print("2. Refill All Resources")
                print("3. View sales and profit/ earnings")
                print("4. Exit Admin Mode")
                admin_choice = input("\nChoose one: ").strip()
                if admin_choice == "1":
                    coffee_maker.report()
                elif admin_choice == "2":
                    coffee_maker.resources = {"water": 1000, "milk": 1000, "coffee": 200}
                    print("\nAll resources fully refilled!\n")
                elif admin_choice == "3":
                    money_calculation.report()
                elif admin_choice == "4":
                    print("\nExiting admin mode...\n")
                    break
                else:
                    print("Invalid choice!")
        else:
            print("Wrong password!\n")
        continue
    elif entry == "off":
        pwd = input("Enter password to turn off: ")
        if pwd == Admin_pass:
            print("\nMachine turning off. Goodbye!")
            exit()
        else:
            print("Opps... Looks like you entered Wrong Password. Access denied.\n")
        continue
    elif entry != "start":
        print("\nPlease type 'Start' to proceed...")
        continue
    print("\nWelcome! Let's make your coffee\n")
    drink_orders = menu.choose_multiple_drinks()
    order_list = []
    total_cost = 0
    for order in drink_orders:
        drink = order["drink"]
        quantity = order["quantity"]
        print(f"\nYou chose {quantity} x {drink.name.capitalize()}\n")
        sizes = ["Small", "Regular", "Large"]
        size_inputs = []
        for i in range(quantity):
            size, size_price = menu.choose_size_with_price(sizes, f"Size for #{i + 1} {drink.name.capitalize()}",drink.cost)
            size_inputs.append((size, size_price))
        for i in range(quantity):
            sugar = menu.choose_option(["No Sugar", "Normal Sugar", "Extra Sweet"], f"Sugar for #{i + 1}")
            extra_shot = menu.choose_option(["No", "Yes (+Tk 20)"], f"Extra shot for #{i + 1}?")
            size, size_price = size_inputs[i]
            extra_cost = 20 if extra_shot == "Yes (+Tk 20)" else 0
            item_cost = size_price + extra_cost
            total_cost += item_cost
            multiplier = {"Small": 0.7, "Regular": 1.0, "Large": 1.4}[size]
            ingredients = {k: int(v * multiplier) for k, v in drink.ingredients.items()}
            if extra_shot == "Yes (+Tk 20)":
                ingredients["coffee"] = ingredients.get("coffee", 0) + 10
            name = f"{size} {drink.name.capitalize()} ({sugar})"
            if extra_shot == "Yes (+Tk 20)":
                name += " + Extra Shot"
            order_list.append({
                "name": name,
                "item_cost": item_cost,
                "ingredients": ingredients
            })
    all_ingredients = {}
    for item in order_list:
        for ing, amt in item["ingredients"].items():
            all_ingredients[ing] = all_ingredients.get(ing, 0) + amt
    if not coffee_maker.is_resource_sufficient(all_ingredients):
        print("\nSorry, insufficient resources. Order could not proceed.\n")
        continue
    print("\n" + "=" * 60)
    print("               YOUR ORDER SUMMARY")
    print("=" * 60)
    for i, item in enumerate(order_list, 1):
        print(f"{i}. {item['name']:<40}  Tk {item['item_cost']}")
    print("-" * 60)
    print(f"{'    TOTAL':<40}          Tk {total_cost}")
    print("=" * 60)
    confirm = input("\nPress Y to confirm/ Press any key to cancel: ").lower()
    if confirm != "y":
        print("\nOrder cancelled.\n")
        continue
    if not money_calculation.make_payment(total_cost):
        print("\nPayment failed.\n")
        continue
    print("\nBrewing your coffee...")
    print("Please wait a moment...\n\n")
    time.sleep(5)
    for item in order_list:
        coffee_maker.make_coffee(item["name"], item["ingredients"])
    save_data()
    print("Thank you! Enjoy your coffees and come again\n")

