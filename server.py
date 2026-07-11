from flask import Flask,jsonify,request
from db.session import session
from db.User import User
from sqlalchemy import or_
app = Flask(__name__)


# Define the route for the homepage
@app.route("/")
def hello_world():
    return jsonify({"message": "hello in our server"})

# List All users
@app.route("/users")
def list_users():
    data = []
    try:
        users = session.query(User).all()
        for u in users:
            data.append({
            "id": u.id,
            "name":u.name,
            "age": u.age,
            "email":u.email
        })
        return jsonify(data)
    except Exception as e:
        session.rollback()
        return {
            "error": str(e)
        }, 400

# Add user
@app.route("/user",methods=['POST'])
def add_user():
    user_request=request.get_json()
    try:
        user =User(name=user_request['name'],age=user_request['age'],email=user_request['email'])
        res=session.add(user)
        session.commit()
        return {"message": "User added successfully","id":user.id,"name":user.name,"email":user.email}
    except Exception as e:
        session.rollback()
        return {
            "error": str(e)
        }, 400
    
# update user by id or email
@app.route("/updateUser",methods=['PUT'])
def update_user():
    try:
        user_request = request.get_json()
        print(user_request)
        user = session.query(User).filter(or_(
        User.id == user_request.get("id"),
        User.email == user_request.get("email")
    )
).first()
        user.name=user_request['name']
#       make the email not change          
#       user.email=user_request['email']
        user.age=user_request['age']
        session.commit()
        return {"message":"update user"}
    except Exception as e:
        session.rollback()
        return {
            "error": str(e)
        }, 400
@app.route('/deleteUser', methods=["DELETE"])
def delete_user():
    try:
        user_request = request.get_json()

        user = session.query(User).filter_by(id=user_request["id"]).first()

        if user is None:
            return {"error": "User not found"}, 404

        session.delete(user)
        session.commit()

        return {"message": "User deleted successfully"}, 200

    except Exception as e:
        session.rollback()
        return {"error": str(e)}, 400

# Run the application
if __name__ == "__main__":
    app.run(debug=True)
