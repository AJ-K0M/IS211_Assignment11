from flask import Flask, render_template, request, redirect, url_for
import pickle
import os
import re

app = Flask(__name__)
DATA_FILE = "todo_list.pkl"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "rb") as file:
        todo_list = pickle.load(file)
else:
    todo_list = []

def is_valid_email(email):
    pattern = r"[^@]+@[^@]+\.[^@]+"
    return re.match(pattern, email)

@app.route("/")
def index():
    return render_template("index.html", todo_list=todo_list)

@app.route("/submit", methods=["POST"])
def submit():
    task = request.form.get("task")
    email = request.form.get("email")
    priority = request.form.get("priority")

    if not task or not is_valid_email(email) or priority not in ["Low", "Medium", "High"]:
        return redirect(url_for("index"))

    todo_list.append({"task": task, "email": email, "priority": priority})
    return redirect(url_for("index"))

@app.route("/clear", methods=["POST"])
def clear():
    global todo_list
    todo_list = []
    return redirect(url_for("index"))

@app.route("/save", methods=["POST"])
def save():
    with open(DATA_FILE, "wb") as file:
        pickle.dump(todo_list, file)
    return redirect(url_for("index"))

@app.route("/delete/<int:item_id>", methods=["POST"])
def delete(item_id):
    if 0 <= item_id < len(todo_list):
        todo_list.pop(item_id)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
