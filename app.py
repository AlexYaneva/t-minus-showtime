from flask import Flask
from flask import render_template, url_for, request, redirect
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')

@app.route('/index', methods=['GET', 'POST'])
def index():
	return render_template('index.html')



if __name__ == '__main__':
	app.run(debug=True)
