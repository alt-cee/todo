from flask import Flask, render_template, request, redirect, url_for
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
    """
    Main page that displays TODOs
    """
    todo_list = todo.query.all()
    return render_template("base.html", todo_list=todo_list)

@app.route("/incomplete")
def incomplete():
    """
    Page that displays incomplete TODOs.
    """
    todo_list = todo.query.filter_by(complete=False).all()
    return render_template("base.html", todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
    """
    Add a new TODO
    """
    title = request.form.get("title")
    new_todo = todo(title = title, complete = False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    """
    Update a TODO between Complete <--> Not Complete
    """
    update_todo = todo.query.filter_by(id=todo_id).first()
    update_todo.complete = not update_todo.complete
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    """
    Delete a TODO
    """
    delete_todo = todo.query.filter_by(id=todo_id).first()
    db.session.delete(delete_todo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 

    app.run(debug=False)
    
