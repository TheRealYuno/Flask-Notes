from flask import Flask, redirect, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///UserNotes.db"
db = SQLAlchemy(app)

class UserNotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    content = db.Column(db.String(5000), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/", methods=["GET"])
def index():
    return redirect("/notes")

@app.route("/notes", methods=["GET", "POST"])
def notes():
    my_notes = UserNotes.query.order_by(UserNotes.date_time.desc()).all()
    if request.method == "POST":
        note_title = request.form["title"]
        note_content = request.form["content"]

        db.session.add(UserNotes(title=note_title, content=note_content))
        db.session.commit()
        return redirect("/notes")
    else:
        return render_template("notes.html", notes=my_notes)

@app.route("/notes/update/<int:id>", methods=["GET", "POST"])
def update(id):
    note = UserNotes.query.get_or_404(id)

    if request.method == "POST":
        note.title = request.form["title"]
        note.content = request.form["content"]

        db.session.add(UserNotes(title=note.title, content=note.content))
        db.session.commit()
        return redirect("/notes")
    else:
        return render_template("update.html", note=note)

@app.route("/notes/delete/<int:id>", methods=["GET"])
def delete(id):
    note = UserNotes.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return redirect("/notes")




if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")