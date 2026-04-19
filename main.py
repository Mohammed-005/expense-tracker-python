import json

class Transaction:
    def __init__(self, category: str, amount: float, transaction_type: str):
        self.category = category
        self.amount = amount
        self.type = transaction_type

    def show(self):
        print(f"{self.category:<15}{self.amount:>15.2f}{self.type:^20}")

    def to_dict(self):
        return {
            "category": self.category.lower(),
            "amount": self.amount,
            "type": self.type
        }

    @staticmethod
    def from_dict(data):
        return Transaction(
            data["category"].lower(),
            data["amount"],
            data["type"]
        )

class Manager:
    def __init__(self):
        self.transactions = []
        self.load_data()

    def add_transaction(self, category, amount, transaction_type):
        self.transactions.append(Transaction(category, amount, transaction_type))
        self.save_data()

    def get_transactions(self):
        return self.transactions.copy()

    def search_transactions(self,category):
        keyword = category.lower().strip()
        search_results = []

        for transaction in self.transactions:
            if keyword in transaction.category.lower():
                search_results.append(transaction)

        return search_results

    def sort_transactions(self, order):
        copied_list = self.transactions.copy()

        if order.lower() in ["asc", "ascending"]:
            copied_list.sort(key=lambda t: t.amount)
        elif order.lower() in ["desc", "descending"]:
            copied_list.sort(key=lambda t: t.amount, reverse=True)
        else:
            return copied_list

        return copied_list

    def net_balance(self):
        total_income: float = 0
        total_expense: float= 0

        for transaction in self.transactions:
            if transaction.type == "income":
                total_income += transaction.amount
            elif transaction.type == "expense":
                total_expense += transaction.amount

        net_balance = total_income - total_expense

        return total_income, total_expense, net_balance

    def delete_transaction(self, index):
        if 0 <= index < len(self.transactions):
            del self.transactions[index]
            self.save_data()
            return True
        return False

    def get_category_summary(self):
        summary = {}

        for transaction in self.transactions:
            category = transaction.category.lower()

            if category not in summary:
                summary[category] = {
                    "income" : 0,
                    "expense" : 0,
                }
            if transaction.type == "income":
                summary[category]["income"] += transaction.amount
            elif transaction.type == "expense":
                summary[category]["expense"] += transaction.amount

        return summary


    def load_data(self):
        try:
            with open("transactions.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                self.transactions = [Transaction.from_dict(d) for d in data]
        except FileNotFoundError:
            self.transactions = []
        except json.JSONDecodeError:
            self.transactions = []

    def save_data(self):
        data = [t.to_dict() for t in self.transactions]
        with open("transactions.json", "w", encoding="utf-8", ) as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def clear_data(self):
            self.transactions = []
            self.save_data()

def get_valid_amount():
    while True:
        try:
            amount = float(input("Enter an amount: "))
            if amount <= 0:
                print("Amount must be greater than 0")
                continue
            return amount
        except ValueError:
            print("Amount must be an integer")

def get_valid_type():
    while True:
        transaction_type = input("Enter transaction type (1.Income, 2.Expense): ").lower()

        if transaction_type in ["1", "income"]:
            return "income"
        elif transaction_type in ["2", "expense"]:
            return "expense"
        else:
            print("Invalid transaction type")
            continue

def get_valid_choice(prompt, min_value = None, max_value = None):
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                print(f"Please enter a value between {min_value} and {max_value}")
                continue
            if max_value is not None and value > max_value:
                print(f"Please enter a value between {min_value} and {max_value}")
                continue
            return value
        except ValueError:
            print(f"Please enter a value between {min_value} and {max_value}")

def display_transaction(transactions):

    if not transactions:
        print("No transactions found!")
        return

    print("-" * 60)
    print(f"{'No':<5}{'Category'.title():<15}{'Amount(in Rs)':>15}{'Type':^20}")
    print("-" * 60)

    for i, transaction in enumerate(transactions, start=1):
        print(f"{i:<5}", end="")
        transaction.show()

    print("-" * 60)

def handle_add():
    category = input("Enter category: ")
    amount = get_valid_amount()
    transaction_type = get_valid_type()
    manager.add_transaction(category, amount, transaction_type)
    print("Transaction added!")

def handle_view():
    display_transaction(manger.get_transactions())

def handle_search():
    category = input("Enter category to search: ")
    display_transaction(manger.get_transactions(category))

def handle_sort():
    order = input("Enter sort order (asc or desc): ")
    display_transaction(manger.sort_transactions(order))

def handle_delete():
    transactions = manager.get_transactions()
    display_transaction(transactions)

    if not transactions:
        return

    index = get_valid_choice("Enter index number to delete: ", 1, len(transactions))
    if manger.delete_transaction(index -1):
        print("Transaction deleted!")
    else:
        print("Invalid index!")

def handle_summary():
    summary = manager.get_category_summary()

    if not summary:
        print("No transactions found!")
        return

    print("-" * 60)
    print(f"{'category':<20}{'Income':>15}{'Expense':>15}")
    print("-" * 60)

    for category, data in summary.items():
        print(f"{category:<20}{data['income']:>15.2f}{data['expense']:>15.2f}")
    print("-" * 60)


manager = Manager()

def main():
    while True:
        print("\n========FINANCE MANAGER========")
        print("\n1. Add transaction")
        print("2. View transactions")
        print("3. Search transactions")
        print("4. Balance")
        print("5. Delete transaction")
        print("6. Sort transactions")
        print("7. Summary of transactions")
        print("8. Clear transaction history")
        print("9. Exit")

        choice = get_valid_choice("\nEnter your choice: ",1,9)

        if choice == 1:
            handle_add()

        elif choice == 2:
            handle_view()

        elif choice == 3:
            handle_search()

        elif choice == 4:
            income, expense, net_balance = manager.net_balance()
            print(f"Income: ₹{income:.2f}")
            print(f"Expense: ₹{expense:.2f}")
            print(f"Net Balance: ₹{net_balance:.2f}")

        elif choice == 5:
            handle_delete()

        elif choice == 6:
            handle_sort()

        elif choice == 7:
            handle_summary()

        elif choice == 8:
            manager.clear_data()
            print("Transactions cleared!")

        elif choice == 9:
            print("Thank you for using this program!")
            break

if __name__ == "__main__":
    main()

