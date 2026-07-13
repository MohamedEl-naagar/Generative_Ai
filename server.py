from flask import Flask,jsonify,request
from db.session import session
from db.User import User
from sqlalchemy import or_
from celery import Celery, Task
app = Flask(__name__)


# task

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost:6379/0",
        result_backend="redis://localhost:6379/0",
        task_ignore_result=False,
    ),
)
celery_app = celery_init_app(app)

# Define the route for the homepage
@app.route("/")
def hello_world():
    return jsonify({"message": "hello in our server"})


@celery_app.task(name="server.list_users_task")
def list_users_task():
    try:
        users = session.query(User).all()
        return [
            {
                "id": user.id,
                "name": user.name,
                "age": user.age,
                "email": user.email,
            }
            for user in users
        ]
    except Exception as e:
        session.rollback()
        raise e


@app.route("/users", methods=["GET"])
def list_users():
    task = list_users_task.delay()
    return jsonify({"task_id": task.id, "status": "processing"}), 202


@app.route("/users/<task_id>", methods=["GET"])
def get_users_result(task_id):
    task = celery_app.AsyncResult(task_id)

    if task.state == "SUCCESS":
        return jsonify(task.result), 200

    if task.state in {"PENDING", "STARTED", "RETRY"}:
        return jsonify({"status": task.state}), 202

    return jsonify({"status": task.state, "error": str(task.result)}), 500

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
