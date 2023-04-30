from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
db.init_app(app)

class todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

@app.route("/")
def index():
    todo_list = todo.query.all()
    return render_template("base.html", todo_list=todo_list)


if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
        new_todo = todo(title = "Wash the car", complete = False)
        db.session.add(new_todo)
        db.session.commit()

    app.run(debug=True)
    
