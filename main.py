from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "ijhgfcgfhjbyugubi"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my-library.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
Bootstrap(app)
db = SQLAlchemy(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False, unique=True)
    author = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"<Book {self.title}>"


db.create_all()


class AddBook(FlaskForm):
    book_name = StringField('Book Name', validators=[DataRequired()])
    book_author = StringField('Book Author', validators=[DataRequired()])
    rating = StringField('Rating', validators=[DataRequired()])
    add_book = SubmitField('Add Book')


class EditRating(FlaskForm):
    rating = StringField('Rating', validators=[DataRequired()])
    change_rating = SubmitField('Change Rating')


@app.route('/')
def home():
    books = Books.query.all()
    return render_template("index.html", books=books)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddBook()
    if form.validate_on_submit():

        new_book = Books(
            title=form.book_name.data,
            author=form.book_author.data,
            rating=form.rating.data
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html", form=form)


@app.route("/edit/<int:ID>", methods=["GET", "POST"])
def edit(ID):
    form = EditRating()
    book = Books.query.get(ID)
    if form.validate_on_submit():
        book.rating = form.rating.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", form=form, id=ID, book=book)


@app.route("/delete/<int:ID>")
def delete(ID):
    book = Books.query.get(ID)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

