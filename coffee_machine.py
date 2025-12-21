class CoffeeMachine:
  def __init__(self):
    self.resources = {
      "water": 1000,
      "milk": 1000,
      "coffee": 1000,
    }
    self.sales_count = {"total_orders": 0}

  def report(self):
    print("\nResources :")
    print(f"Water: {self.resources['water']} ml")
    print(f"Milk: {self.resources['milk']} ml")
    print(f"Coffee: {self.resources['coffee']} g")
    print(f"\nSales: {self.sales_count['total_orders']} orders")
    for drink, count in self.sales_count.items():
      if drink != "total_orders":
        print(f"  {drink.capitalize()}: {count}")

  def is_resource_sufficient(self, ingredients):
    for item, amount in ingredients.items():
      if self.resources.get(item, 0) < amount:
        print(f"Sorry, not enough {item}.")
        return False
      if self.resources.get(item, 0) < amount + 100:
        print(f"Warning: {item.capitalize()} is running low!")
    return True

  def make_coffee(self, drink_name, ingredients):
    for item, amount in ingredients.items():
      if item in self.resources:
        self.resources[item] -= amount
    self.sales_count['total_orders'] = self.sales_count.get('total_orders', 0) + 1
    self.sales_count[drink_name] = self.sales_count.get(drink_name, 0) + 1
    print(f"Here is your {drink_name}!")
