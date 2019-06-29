import os
import json

from flask import Flask, session, render_template, request, session,abort, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import requests

KEY="CnbXvN0Q0gCHVkGFavV0g"
app = Flask(__name__)
#app.secret_key = 'fkdjsafjdkfdlkjfadskjfadskljdsfklj'

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("welcome.html")

@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if db.execute("SELECT * FROM users WHERE username = :username AND password = :password",
            {"username": username, "password": password}).rowcount == 0:
            return render_template("reg.html")
        else:
            #session['username'] == username
            return render_template("success_login.html", username=username)

    return render_template("welcome.html")

@app.route("/reg", methods = ["POST", "GET"])
def reg():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        db.execute("INSERT INTO users (username, password) VALUES (:name, :password)",
                    {"name": username, "password": password})
        db.commit()
        return render_template("welcome.html", username=username)

    return render_template("reg.html")

@app.route("/search", methods = ["POST"])
def search():
    isbn = request.form.get("isbn")
    title = request.form.get("title")
    author = request.form.get("author")
    data = []
    flag = True
    res = db.execute("SELECT * FROM books WHERE isbn iLIKE '%"+isbn+"%' AND title iLIKE '%"+title+"%' AND author iLIKE '%"+author+"%'").fetchall()

    for x in res:
        data.append(x)
    if len(res) == 0:
        message =("Sorry! No results found!")
    else:
        message =("Results as follows!")
    return render_template("results.html",results=data,message=message)

@app.route("/<string:isbn>")
def book_page(isbn):
    rating = range(1,6,1)
    res = db.execute("SELECT * FROM books WHERE isbn LIKE '%"+isbn+"%'").fetchall()
    reviews = db.execute("SELECT * FROM reviews WHERE isbn LIKE '%"+isbn+"%'").fetchall()
    api_res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": KEY, "isbns": isbn})
    Api_res = api_res.json()
    if not Api_res:
        m1 = "Sorry! No Goodreads reviews have been provided!"
        avg_r = ""
        avg_wrc = ""
    else:
        m1 = "Goodreads reviews are as follows:"
        avg_r=Api_res['books'][0]['average_rating']
        avg_wrc=Api_res['books'][0]['work_ratings_count']

    data1 = []
    data2 = []
    for x in res:
        data1.append(x)

    for y in reviews:
        data2.append(y)

    if len(data2)==0:
        m2 = "Sorry! No review for this book is provided!"
    else:
        m2 = "The review is as follows:"
    #return render_template("welcome.html")
    return render_template("book_detail.html",book=data1,reviews=data2,rating=rating, m1=m1, m2=m2, avg_r=avg_r, avg_wrc=avg_wrc)

@app.route("/review_submission/<isbn>", methods = ["POST"])
def review_submission(isbn):
    comment = request.form.get("comment")
    rating = request.form.get("rating")
    username = request.form.get("username")
    db.execute("INSERT INTO reviews (isbn, review, rating, username) VALUES (:isbn, :review, :rating, :username)",
        {"isbn":isbn, "review":comment, "rating":rating, "username":username})
    db.commit()
    return render_template("review_submit.html",isbn=isbn)

@app.route("/api/<isbn>", methods = ["GET"])
def api(isbn):
    data=db.execute("SELECT * FROM books WHERE isbn = :isbn",{"isbn":isbn}).fetchone()
    if not data:
        abort(404)

    api = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": KEY, "isbns": isbn})
    Api = api.json()
    x = {
        "title": data[1],
        "author": data[2],
        "year": data[3],
        "isbn": isbn,
        "review_count": Api['books'][0]['work_text_reviews_count'],
        "average_score": Api['books'][0]['average_rating']
        }
    api=json.dumps(x)
    return render_template("api.json",api=api)
'''
@app.route("/logout", methods = ["GET", "POST"])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
'''
