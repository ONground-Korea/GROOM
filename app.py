import os, sys
from flask import Flask, request, redirect, url_for
from flask.templating import render_template
#from werkzeug import secure_filename
import crawling
app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crawl', methods=['GET', 'POST'])
def crawl():
    if request.method == 'POST':
        prompt = request.form['prompt']
        crawling.main(prompt)

    return redirect(url_for('result'))

@app.route('/result', methods=['GET', 'POST'])
def result():
    return render_template('result.html')

if __name__ == "__main__":
    app.run()