# Code taken and modified from:
# http://flask.pocoo.org/docs/1.0/patterns/fileuploads/

import os
import requests
from flask import Flask, request, redirect, render_template
from werkzeug.utils import secure_filename

SECRET_KEY = 'cidru'.encode('utf8')
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'html'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY 

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			return render_template('try_again_upload.html')

		file = request.files['file']

		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			return render_template('try_again_upload.html')

		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

			# announce backend to run task
			post_data = {
				'arg': filename,
			}

			response = requests.post('http://queue:5001/enqueue', data = post_data)
			print(response.json(), response.status_code)

			return render_template('succes_upload.html')

	return render_template('upload.html')

if __name__ == '__main__':
	app.run(debug = True, host='0.0.0.0', port = 5000)
