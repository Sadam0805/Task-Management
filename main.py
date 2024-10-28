from flask import Flask, render_template, request, redirect
import mysql.connector
from mysql.connector import Error

# Flask app
app = Flask(__name__)


# MySQL database Connection
try:
    # Establish connection to MySQL
    connection = mysql.connector.connect(
        host='localhost',  # Replace with your MySQL server host
        database='project_use',  # Replace with your database name
        user='root',  # Replace with your MySQL username (e.g., 'root')
        password=''  # Replace with your MySQL password
    )

    if connection.is_connected():
        print("Connected to MySQL Server version")

except Error as e:
    print("Error while connecting to MySQL", e)


# Index page to show the tasks
@app.route("/")
def index():
    cursor = connection.cursor()
    cursor.execute("Select * from tasks")
    all_task_data = cursor.fetchall()

    return render_template("index.html", tasks=all_task_data)


@app.route("/add_task")
def get_task_data():
    return render_template("add_task.html")


# Add new task to the database
@app.route("/add", methods=["POST"])
def add():
    task_title = request.form["title"]
    task_description = request.form["description"]
    task_due_date = request.form["due_date"]


    cursor = connection.cursor()
    cursor.execute("insert into tasks (title, description, due_date) values(%s, %s, %s)", [task_title, task_description, task_due_date])
    connection.commit()
    print("data inserted successfully and commited")
    return redirect("/")


@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit(task_id):
    cursor = connection.cursor()
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        due_date = request.form["due_date"]
        status = request.form["status"]

        cursor.execute("update tasks set title=%s, description=%s, due_date=%s, status=%s where id=%s", (title, description, due_date, status, task_id))
        connection.commit()
        return redirect("/")

    cursor.execute("select * from tasks where id=%s", (task_id,))
    task = cursor.fetchone()
    return render_template("update_task.html", task=task)


# delete the task from the database
@app.route("/delete/<int:task_id>")
def delete(task_id):
    cursor = connection.cursor()
    cursor.execute("delete from tasks where id=%s", (task_id,))
    connection.commit()
    return redirect("/")


# run the Project
if __name__ == "__main__":
    app.run(debug=True)
