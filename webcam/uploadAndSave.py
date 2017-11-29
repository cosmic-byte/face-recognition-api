import os
import face_recognition
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import PIL
from PIL import Image

UPLOAD_FOLDER = os.path.abspath("images/")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            # flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            # flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            new_file = resize_image(file)
            new_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            _image = face_recognition.load_image_file(file)
            face_locations = face_recognition.face_locations(_image)
            if len(face_locations) > 0:
                return '''
                <!doctype html>
                <title>Success Page</title>
                <h1>File Successfully Uploaded</h1>
                '''
            else:
                os.remove("images/"+filename)
                return '''
                <!doctype html>
                <title>Error Page</title>
                <h1>No face Detected</h1>
                '''

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


def resize_image(img):
    base = 800
    new_image = Image.open(img)
    w_percent = (base / float(new_image.size[0]))
    h_size = int((float(new_image.size[1]) * float(w_percent)))
    new_image = new_image.resize((base, h_size), PIL.Image.ANTIALIAS)
    return new_image

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)