# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

This app will be a central repository for all tasks that an individual must complete, providing overall visibility into one's workload that is usually divided between many different stores such as a college website, email, and calendar.

## User stories

- GitHub Issues (user stories): https://github.com/swe-students-spring2026/2-web-app-mosaic_mule/issues

## Steps necessary to run the software

### 1. Prerequisites
- Python 3.x installed
- Docker Desktop installed and running

### 2. Clone the repo
git clone <REPO_URL>
cd <REPO_FOLDER>

### 3. Start MongoDB (Docker)
Make sure Docker Desktop is running, then run: docker run --name mongodb_dockerhub -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=secret -d mongo:latest

### 4. Configure environment variables (.env)
Create a .env file based on env.example and fill in the real values: cp env.example .env

### 5. Install Pipenv (if you don’t have it)
pip install pipenv

### 6. Install dependencies with Pipenv
pipenv install
Pipenv will read the Pipfile (similar to requirements.txt) and install dependencies (currently Flask, PyMongo, and python-dotenv).

### 7. Run the app
pipenv run python main_app.py
Then open the app in your browser (typically): http://127.0.0.1:5000

## Task boards

- Sprint task boards (GitHub Projects): https://github.com/orgs/swe-students-spring2026/projects/33
