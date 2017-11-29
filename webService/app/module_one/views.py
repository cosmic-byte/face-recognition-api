# -*- coding: utf-8 -*-
from flask import Blueprint
import face_recognition
from flask import request, redirect, jsonify

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

module_one = Blueprint(
    'module_one',
     __name__,
     static_folder='static',
     template_folder='templates',
     static_url_path='/static/module-one'

)


@module_one.route('/face-recognition/compare', methods=['GET', 'POST'])
def compare():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file1' not in request.files and 'file2' not in request.files:
            # flash('No file part')
            return redirect(request.url)
        file = request.files['file1']
        file2 = request.files['file2']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '' or file2.filename == '':
            # flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename) and allowed_file(file2.filename):
            return process_images(file, file2)

    return '''
    <!doctype html>
    <title>Compare</title>
    <head>
        <style> 
        #main {
            width: 600px;
            height: 300px;
            border: 1px solid #c3c3c3;

        }
        #main div {
            display: inline-block;
            width: 400px;
            margin: 20px;
        }
        #main b {
            margin: 0 10px 0 0;
        }
        </style>
    </head>
    <h1>Upload Pictures to Compare</h1>
    <form method=post enctype=multipart/form-data id=main>
      <div><b>known image:</b><input type=file name=file1></div>
      <div><b>unknown image:</b><input type=file name=file2></div>
      <div><input type=submit value=process></div>
    </form>
    '''


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def process_images(file, file2):

    face_match = False
    known_image = face_recognition.load_image_file(file)
    unknown_image = face_recognition.load_image_file(file2)
    known_face_locations = face_recognition.face_locations(known_image)
    unknown_face_locations = face_recognition.face_locations(unknown_image)

    if len(known_face_locations) == 0:
        return '''
                <!doctype html>
                <title>Error Page</title>
                <h1>No face detected on Image1</h1>
                '''
    elif len(unknown_face_locations) == 0:
        return '''
                <!doctype html>
                <title>Error Page</title>
                <h1>No face Detected on Image2</h1>
                '''
    else:
        known_face_encodings = face_recognition.face_encodings(known_image, known_face_locations)[0]
        unknown_face_encodings = face_recognition.face_encodings(unknown_image, unknown_face_locations)
        match = face_recognition.compare_faces([known_face_encodings], unknown_face_encodings[0], 0.50)
        if match[0]:
            face_match = True
        # Return the result as json
        result = {
            "Faces_Match": face_match
        }
        return jsonify(result)
