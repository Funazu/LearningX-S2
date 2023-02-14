from flask import Flask, requests, render_template, redirect, url_for, jsonfiy

app = Flask(__name__)

@app.route('/practice')
def practice():
    return render_template('practice.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)