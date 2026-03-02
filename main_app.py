from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId
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
    # Default
    sort   = request.args.get("sort", "deadline")
    order  = request.args.get("order", "asc")
    diffi  = request.args.get("difficulty", "")
    course = request.args.get("course", "")

    # Sort in MongDB
    query  = {}
    if diffi:
        query["difficulty"] = diffi
    if course:
        query["course"] = course

    sort_map   = {"deadline": "deadline", "created_at": "created_at", "title": "title",}
    sort_field = sort_map.get(sort, "deadline")
    if order == "asc":
        sort_dir = 1
    else: 
        sort_dir = -1

    items = list(deadlines.find(query).sort([(sort_field, sort_dir), ("created_at", 1)]))
    return render_template("deadlines_list_screen.html", items=items)

@app.get("/deadlines/new")
def new_deadline_screen():
    return render_template("deadlines_add_screen.html")
@app.get("/search")
def search_deadlines():
    q = request.args.get("q", "").strip()

    query = {}
    if q:
        query["$or"] = [
            {"title": {"$regex": q, "$options": "i"}},
            {"course": {"$regex": q, "$options": "i"}},
            {"difficulty": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}},
        ]

    items = list(deadlines.find(query).sort([("deadline", 1), ("created_at", 1)]))
    return render_template("deadlines_search_screen.html", items=items, q=q)
@app.route("/deadlines/add", methods=["POST"])
def add_deadline():
    title        = request.form.get("title", "").strip()
    course       = request.form.get("course", "").strip()
    deadline_str = request.form.get("deadline", "").strip()
    difficulty   = request.form.get("difficulty", "").strip()
    description  = request.form.get("description", "").strip()

    if not title or not deadline_str:
        return redirect(url_for("list_deadlines"))

    try:
        deadline_dt = datetime.datetime.strptime(deadline_str, "%Y-%m-%d")
    except ValueError:
        return redirect(url_for("list_deadlines"))

    doc = {
        "title"      : title,
        "course"     : course,
        "deadline"   : deadline_dt,
        "created_at" : datetime.datetime.utcnow(),
        "difficulty" : difficulty,
        "description": description
    }

    deadlines.insert_one(doc)
    return redirect(url_for("list_deadlines"))

@app.get("/deadlines/filter")
def deadlines_filter_screen():
    return render_template("deadlines_filter_screen.html")

@app.get("/deadlines/info/<deadline_id>")
def info_deadline_screen(deadline_id):
    deadline = deadlines.find_one({"_id": ObjectId(deadline_id)})
    return render_template("deadlines_info_screen.html", deadline = deadline)

@app.get("/deadlines/edit/<deadline_id>")
def edit_deadline_screen(deadline_id):
    deadline = deadlines.find_one({"_id": ObjectId(deadline_id)})
    return render_template("deadlines_edit_screen.html", deadline = deadline)

@app.post("/deadlines/edit/<deadline_id>")
def edit_deadline(deadline_id):
    newTitle       = request.form.get("title", "").strip()
    newCourse      = request.form.get("course", "").strip()
    newDeadline    = request.form.get("deadline", "").strip()
    newDifficulty  = request.form.get("difficulty", "").strip()
    newDescription = request.form.get("description", "").strip()
    if not newTitle or not newCourse or not newDeadline or not newDifficulty or not newDescription:
        return redirect(url_for("list_deadlines"))
    try:
        newDeadline_dt = datetime.datetime.strptime(newDeadline, "%Y-%m-%d")
    except ValueError:
        return redirect(url_for("list_deadlines"))
    
    deadlines.update_one(
        {"_id": ObjectId(deadline_id)},
        {"$set": {"title": newTitle, "deadline":newDeadline_dt}}
    )

    return redirect(url_for("list_deadlines"))

@app.get("/deadlines/delete/<deadline_id>")
def delete_deadline_screen(deadline_id):
    try:
        oid = ObjectId(deadline_id)
    except InvalidId:
        return redirect(url_for("list_deadlines"))

    deadline = deadlines.find_one({"_id": oid})
    if not deadline:
        return redirect(url_for("list_deadlines"))

    return render_template("deadlines_delete_screen.html", deadline=deadline)


@app.post("/deadlines/delete/<deadline_id>")
def delete_deadline(deadline_id):
    try:
        oid = ObjectId(deadline_id)
    except InvalidId:
        return redirect(url_for("list_deadlines"))

    deadlines.delete_one({"_id": oid})
    return redirect(url_for("list_deadlines"))


if __name__ == "__main__":
    app.run(debug=True)