from flask import Blueprint,render_template,request,redirect, url_for, session
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")

views = Blueprint('views',__name__)

url = "https://api.groq.com/openai/v1/chat/completions"
header = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}
promp = []
answe = []
message = []
@views.route('/', methods=["GET","POST"])
def home():
    if request.method == "POST":
        prompt = request.form["prompt"]
        message.append({
                "role": "user",
                "content": f"{prompt}"
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
            promp.append(prompt)
            answe.append(res_jn["choices"][0]["message"]["content"])
            message.append({
        "role": "assistant",
        "content": res_jn["choices"][0]["message"]["content"]
      })
        else:
            promp.append(prompt)
            answe.append("error")
        return redirect(url_for("views.home"))
    return render_template("home.html",prompts=promp, answers=answe)