#runs the web server that serves as the interface for the user

from flask import Flask, render_template, request
from werkzeug import secure_filename

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0	#disable caching, so that the image from /static/ is forced to reload every time
import threeAxis

fname=''	#used to display the uploaded file name in the graph

@app.route('/upload')
@app.route('/')
def upload_file_html():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      global fname 
      fname=secure_filename(f.filename)
      f.save("uploaded_file")
      return render_template('doneUpload.html')

@app.route('/process')
def process():
	print(fname)
	results=threeAxis.analysis("uploaded_file",1,server=1,fname=fname)	#[filepath,read as utf-16?(unprocessed),server requesting?,fname]
	avg=results[0]
	x=results[1]
	y=results[2]
	z=results[3]

	return render_template('results.html',x=x,y=y,z=z,avg=avg,imgPath="static/results.png")
		
if __name__ == '__main__':
   app.run(debug = True,host = '192.168.1.68', port = 5000)