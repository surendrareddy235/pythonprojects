from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuring SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.db'  # Creating a file called flask.db in the project
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the database model (table)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"

# Route to display the form
@app.route("/")
def getform():
    return render_template("index.html")

# Route to handle form submission
@app.route("/formpage", methods=["POST"])
def formpage():
    # Get data from the form
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    # Create a new user and add it to the database
    new_user = User(name=name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/success")

@app.route("/success")
def showsuccess():
    users = User.query.all()
    return render_template("success.html", users=users)

@app.route("/edit/<int:user_id>", methods=["GET", "POST"])
def edit(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == "POST":
        # Update the user with the new form data
        user.name = request.form['name']
        user.email = request.form['email']
        user.password = request.form['password']
        db.session.commit()
        return redirect("/success")

    # If the method is GET, display the form with the existing user data
    return render_template("edit_user.html", user=user)

@app.route("/delete/<int:user_id>")
def delete(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/success")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)   # only for local testing
else:
    # When IIS imports your app via wfastcgi, ensure DB tables are created
    with app.app_context():
        db.create_all()
