from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for
)

from pymongo import MongoClient

app = Flask(__name__)

password = 'kamukepodeh'
cxn_str = f'mongodb+srv://fauzunnaja:{password}@cluster0.kwi1dlp.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(cxn_str)
db = client.dbsparta

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    return jsonify({
        'result': 'success',
        'restaurants': [],
    })

@app.route('/map')
def map_example():
    return render_template('prac_map.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)