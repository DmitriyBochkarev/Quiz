from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@pgdb:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()


class Article(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(100), nullable=False)
    question = db.Column(db.String(300), nullable=False)
    value = db.Column(db.Text, nullable=False)
    airdate = db.Column(db.DateTime, nullable=False)


    def __repr__(self):
        return '<Article %r>' % self.id
# Создание таблиц
with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.airdate.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        count = request.form['count']
        res = requests.get(f"https://jservice.io/api/random?count={count}")

        answer = list(res.json()[0].values())[1]
        question = list(res.json()[0].values())[2]
        value = list(res.json()[0].values())[3]
        airdate = list(res.json()[0].values())[4]

        article = Article(answer=answer, question=question, value=value, airdate=airdate)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')

        except:
            return "При создании вопроса произошла ошибка"
    else:
        return render_template("create-article.html")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
