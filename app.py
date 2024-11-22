#gitでバージョン管理
#Pythonのバージョンは，3.9.13

from flask import Flask, request, redirect
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tp_hu.db" # 今回作成するDB名
db = SQLAlchemy(app)

# Classを使ってDBへPOSTするデーターを定義
# nullable=Falseは、nullでPOSTはできないように定義

class tp_hu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temp= db.Column(db.String(10), nullable=False)
    hum = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                    default=datetime.now(pytz.timezone('Asia/Tokyo')))

@app.route("/", methods=['GET', 'POST']) 
def index():
    if request.method == 'GET':
        tp_hus = tp_hu.query.all()
        return render_template('index.html', tp_hus=tp_hus)

@app.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        temp = request.form.get('temp')
        hum = request.form.get('hum')
        post = tp_hu(temp=temp, hum=hum)
        db.session.add(post)
        db.session.commit()
        tp_hus = tp_hu.query.all()
        return render_template('index.html', tp_hus=tp_hus)
    else:
        return render_template('create.html')

@app.route("/update", methods=['GET', 'POST']) 
def update():    
    if request.method == 'GET':
        return render_template('update.html')
    else:
        id = request.form.get('u_id')
        post = tp_hu.query.get(id)
        post.temp = request.form.get('temp') # 書き換え
        post.hum = request.form.get('hum') # 書き換え
        db.session.commit()

        return redirect('/')

@app.route("/delete", methods=['GET', 'POST']) 
def delete():    
    if request.method == 'GET':
        return render_template('delete.html')
    else:
        id = request.form.get('u_id')
        post = tp_hu.query.get(id)
        db.session.delete(post)
        db.session.commit()
        return redirect('/')
