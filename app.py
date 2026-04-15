from flask import Flask, render_template_string, request
from main import Manager

app = Flask(__name__)
manager = Manager()

@app.route("/")
def home():
    transactions = manager.get_transactions()

    html = """
    <h2>Expense Tracker</h2>

    <h3>Add Transaction</h3>
    <form action="/add" method="post">
        Category: <input name="category"><br><br>
        Amount: <input name="amount"><br><br>
        Type:
        <select name="type">
            <option value="income">Income</option>
            <option value="expense">Expense</option>
        </select><br><br>

        <button type="submit">Add</button>
    </form>

    <hr>
    <h3>Transactions</h3>
    """

    if not transactions:
        html += "No transactions yet"
        return html

    html += "<ul>"
    for t in transactions:
        html += f"<li>{t.category} - ₹{t.amount} - {t.type}</li>"
    html += "</ul>"

    return html
@app.route("/add", methods=["POST"])

def add():
    category = request.form["category"]
    amount = float(request.form["amount"])
    ttype = request.form["type"]

    manager.add_transaction(category, amount, ttype)

    return "<h3>Added successfully! <a href='/'>Go back</a></h3>"
if __name__ == "__main__":
    app.run(debug=True)
