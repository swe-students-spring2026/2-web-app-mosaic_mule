from flask import Flask, render_template
from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()

app            = Flask(__name__, template_folder="web_pages")
app.secret_key = os.getenv("SECRET_KEY", "dev")

client         = MongoClient(os.getenv("MONGO_URI"))
db             = client[os.getenv("MONGO_DB", "ddl_manager")]
deadlines      = db["deadlines"]

@app.get("/")
def list_deadlines():
    items = list(deadlines.find())
    return render_template("deadlines_list_screen.html", items=items)

if __name__ == "__main__":
    app.run(debug=True)