from flask import Blueprint,render_template,request,redirect, url_for, session
import requests
import os
from dotenv import load_dotenv
from . import db
import uuid

class user(db.Model):
    id = db.Column("id",db.Integer,primary_key = True)
    user_id = db.Column("user_id",db.String(33),nullable=False)
    role = db.Column("role",db.String(20),nullable=False)
    message = db.Column("message",db.Text,nullable=False)
load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")

views = Blueprint('views',__name__)

url = "https://api.groq.com/openai/v1/chat/completions"
header = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}


@views.route('/', methods=["GET","POST"])
def home():
    if "user_id" not in session:
        session["user_id"] = uuid.uuid4().hex
    user_id = session["user_id"]
    if request.method == "POST":
        message = []
        prompt = request.form["prompt"]
        usr = user(user_id = user_id, role = "user" ,message = prompt)
        db.session.add(usr)
        db.session.commit()
        mes = user.query.filter_by(user_id = user_id).order_by(user.id).all()
        for i in mes:
            message.append({
                "role": i.role,
                "content": i.message
            })
        data = {
            "model": "openai/gpt-oss-120b",
            "messages": message
        }
        response = requests.post(url,headers=header,json=data)
        res_jn = response.json()
        print(response.status_code)
        print(response.text)
        if response.status_code == 200:
            usr1 = user(user_id = user_id, role = "assistant" ,message = res_jn["choices"][0]["message"]["content"])
            db.session.add(usr1)
            db.session.commit()
        else:
            usr2 = user(user_id = user_id, role = "assistant" ,message = "error")
            db.session.add(usr2)
            db.session.commit()
        return redirect(url_for("views.home"))
    mess = user.query.filter_by(user_id = user_id).order_by(user.id).all()
    return render_template("home.html",message = mess)