from pymongo import MongoClient
import jwt
from datetime import datetime, timedelta
import hashlib
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect,
    url_for
)
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['UPLOAD_FOLDER'] = './static/profile_pics'

SECRET_KEY = 'N4'

MONGODB_CONNECTION_STRING = 'mongodb+srv://fauzunnaja:kamukepodeh@cluster0.kwi1dlp.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(MONGODB_CONNECTION_STRING)
db = client.dbsparta

TOKEN_KEY = 'mytoken'

@app.route('/', methods=['GET'])
def home():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        return render_template('index.html')
    except jwt.ExpiredSignatureError:
        msg = 'Your token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = 'There was a problem logging you in'
        return redirect(url_for('login', msg=msg))

@app.route('/login', methods=['GET'])
def login():
    msg = request.args.get('msg')
    return render_template('login.html', msg=msg)

@app.route('/user/<username>', methods=['GET'])
def user(username):
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        status = username == payload.get('id')
        user_info = db.user.find_one(
            {'username': username},
            {'_id': False}        
        )
        return render_template(
            'user.html',
            user_info=user_info,
            status=status
        )
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))

@app.route("/sign_in", methods=["POST"])
def sign_in():
    # Sign in
    username_receive = request.form["username_give"]
    password_receive = request.form["password_give"]
    pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
    result = db.users.find_one(
        {
            "username": username_receive,
            "password": pw_hash,
        }
    )
    if result:
        payload = {
            "id": username_receive,
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return jsonify(
            {
                "result": "success",
                "token": token,
            }
        )
    else:
        return jsonify(
            {
                "result": "fail",
                "msg": "We could not find a user with that id/password combination",
            }
        )

@app.route("/sign_up/save", methods=["POST"])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,                              
        "password": password_hash,                                 
        "profile_name": username_receive,                          
        "profile_pic": "",                                         
        "profile_pic_real": "profile_pics/default-profile.jpg", 
        "profile_info": ""                                       
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})

@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form.get('username_give')
    user = db.users.find_one({'username': username_receive})
    print(user)
    exists = bool(user)
    return jsonify({'result': 'success', 'exists': exists})

@app.route('/update_profile', methods=['POST'])
def update_profile():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        return jsonify({
            'result': 'success',
            'msg': 'Your profile has been updated'
        })
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))

@app.route('/posting', methods=['POST'])
def posting():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        return jsonify({
            'result': 'success',
            'msg': 'Posting successful!'
        })
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))

@app.route('/get_posts', methods=['GET'])
def get_posts():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        return jsonify({
            'result': 'success',
            'msg': 'Successfuly fetched all posts'
        })
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))

@app.route('/update_like', methods=['POST'])
def update_like():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        return jsonify({
            'result': 'success',
            'msg': 'updated!'
        })
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/secret', methods=['GET'])
def secret():
    return render_template('secret.html')
    # token_receive = request.cookies.get(TOKEN_KEY)
    # try:
    #     payload = jwt.decode(
    #         token_receive,
    #         SECRET_KEY,
    #         algorithms=['HS256']
    #     )
    #     return jsonify({
    #         'result': 'success',
    #         'msg': 'updated!'
    #     })
    # except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
    #     return redirect(url_for('home'))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)