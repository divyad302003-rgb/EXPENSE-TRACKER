from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database connection
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# Table create
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
id INTEGER PRIMARY KEY AUTOINCREMENT,
amount INTEGER,
category TEXT
)
""")
conn.commit()

# Home page
@app.route("/")
def home():

    return render_template("index.html",)

# Add expense
@app.route('/add', methods=['POST'])
def add():

    amount = request.form['amount']
    category = request.form['category']

    cursor.execute(
        "INSERT INTO expenses (amount, category) VALUES (?,?)",
        (amount, category)
    )

    conn.commit()

    return redirect("/")

# Expense list page
@app.route('/expenses')
def expenses():

    cursor.execute("SELECT * from expenses")
    data = cursor.fetchall()

    cursor.execute("select sum(amount) from expenses")
    total = cursor.fetchone()[0]

    return render_template("expenses.html", expenses=data,total=total)

@app.route('/delete/<int:id>')
def delete(id):
    cursor.execute("delete from expenses where id=?",(id, ))
    conn.commit()

    return redirect("/expenses")


app.run(debug=True)