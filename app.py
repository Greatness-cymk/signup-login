from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "my_secret_key"


def connect_to_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="pupils"
    )


@app.route("/")
def home():
    return redirect("/login")


@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        connection = connect_to_mysql()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO users (email, password) VALUES (%s, %s)",
            (email, password)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/login")

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        connection = connect_to_mysql()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email = %s AND password = %s",
            (email, password)
        )

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:
            session["email"] = email
            return redirect("/welcome")

        return "Invalid email or password"

    return render_template("login.html")


@app.route("/welcome")
def welcome():

    if "email" not in session:
        return redirect("/login")

    return render_template(
        "welcome.html",
        email=session["email"]
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)