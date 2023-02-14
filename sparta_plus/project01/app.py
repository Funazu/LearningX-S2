from flask import Flask, render_template, jsonify, request
from datetime import datetime
from pymongo import MongoClient

db_url = 'mongodb+srv://fauzunnaja:kamukepodeh@cluster0.kwi1dlp.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(db_url)
db = client.dbsparta

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
        'content': content
    }
    db.diary.insert_one(data)
    return jsonify({ 'message': 'disampaikan' })


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)