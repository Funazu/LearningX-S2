import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, jsonify, request
from datetime import datetime
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    data = list(db.diary.find({}, {'_id': False}))

    return jsonify({ 'data': data })

@app.route('/diary', methods=['POST'])
def save_diary():
    title = request.form.get('title')
    content = request.form.get('content')

    today = datetime.now()
    time = today.strftime('%Y-%m-%d-%H-%M-%S')
    timenow = today.strftime('%Y.%m.%d')

    file = request.files['file']
    extension = file.filename.split('.')[-1]
    filename = f'post-{time}.{extension}'
    save_to = f'static/{filename}'
    file.save(save_to)

    profile = request.files['profile']
    extension = profile.filename.split('.')[-1]
    profilename = f'profile-{time}.{extension}'
    save_to = f'static/{profilename}'
    profile.save(save_to)    


    
    data = {
        'file': filename,
        'profile': profilename,
        'title': title,
        'content': content,
        'timenow': timenow,
    }
    db.diary.insert_one(data)
    return jsonify({ 'message': 'disampaikan' })


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)