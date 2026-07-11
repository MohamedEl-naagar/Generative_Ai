from flask import Flask,jsonify
from db.session import session
from db.User import User

app = Flask(__name__)
data = []

users = session.query(User).all()

for u in users:
    data.append({
        "id": f"{u.id}",
        "name": f"{u.name}",
        "age": f"{u.age}"
    })

# Define the route for the homepage
@app.route("/")
def hello_world():
    return jsonify({"message": "hello in our server"})

# List All users
@app.route("/users")
def list_users():
    return jsonify(data)


# Run the application
if __name__ == "__main__":
    app.run(debug=True)
