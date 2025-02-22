from flask import Flask,request,jsonify,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

from flask import Flask,request,jsonify,redirect,url_for
from flask_sqlalchemy  import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite_api.db'
db = SQLAlchemy(app)
print("connection to database is successfull",db)

class sqliteapi_Table(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    number = db.Column(db.String(100), nullable=True)
print("table is created successfully in:",db)
with app.app_context():
    db.create_all()

@app.route("/add_user", methods=["post"])
def add_user():
    data = request.json
    if not data or 'email' not in data:
        return jsonify({'message':'email is required'}),404
    new_user = sqliteapi_Table(
        name = data.get('name'),
        email = data['email'],
        number = data.get('number')
    )
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message':'user is successfully added'}),201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),404
    
@app.route("/get_user", methods=["GET"])
def get_user():
    getusers = sqliteapi_Table.query.all()
    users = [{"id":u.id,"name":u.name, "email":u.email, "number":u.number} for u in getusers]
    return jsonify(users)

@app.route("/delete_user/<int:user_id>", methods=["Delete"])
def delete_user(user_id):
    user = sqliteapi_Table.query.get(user_id)
    if not user:
        return jsonify({"message":"user not found"}),404
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message":"user deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}),500

if  __name__ == "__main__":
    app.run(debug=True)
