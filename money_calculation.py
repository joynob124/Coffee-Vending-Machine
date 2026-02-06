class MoneyCalculation:
    def __init__(self):
        self.profit = 0

    def report(self):
        print(f"\nTotal earning : Tk {self.profit}")

    def make_payment(self, cost):
        print(f"Please insert Tk {cost}")
        try:
            paid = float(input("Taka : "))
        except:
            print("Invalid amount. Order cancelled.")
            return False

        if paid < cost:
            print(f"Sorry, {cost - paid} Tk short. Amount refunded.")
            return False
        elif paid > cost:
            change = round(paid - cost, 2)
            print(f"Here is your change: Tk {change}")
        self.profit += cost
        print("Payment successful!")
        return True
