from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import os

load_dotenv()

app            = Flask(__name__, template_folder="web_pages")
app.secret_key = os.getenv("SECRET_KEY", "dev")

client         = MongoClient(os.getenv("MONGO_URI"))
db             = client[os.getenv("MONGO_DB", "ddl_manager")]
deadlines      = db["deadlines"]

@app.get("/")
def list_deadlines():
    q = request.args.get("q", "").strip()

    query = {}
    if q:
        query["title"] = {"$regex": q, "$options": "i"}

    items = list(deadlines.find(query).sort([
        ("deadline", 1),
        ("created_at", 1)
    ]))

    return render_template("deadlines_list_screen.html", items=items, q=q)

@app.get("/deadlines/new")
def new_deadline_screen():
    return render_template("deadlines_add_screen.html")

@app.route("/deadlines/add", methods=["POST"])
def add_deadline():
    title = request.form.get("title", "").strip()
    deadline_str = request.form.get("deadline", "").strip()

    if not title or not deadline_str:
        return redirect(url_for("list_deadlines"))

    try:
        deadline_dt = datetime.datetime.strptime(deadline_str, "%Y-%m-%d")
    except ValueError:
        return redirect(url_for("list_deadlines"))

    doc = {
        "title": title,
        "deadline": deadline_dt,
        "created_at": datetime.datetime.utcnow()
    }

    deadlines.insert_one(doc)
    return redirect(url_for("list_deadlines"))

if __name__ == "__main__":
    app.run(debug=True)