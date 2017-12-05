# -*- coding: utf-8 -*-
from flask import Blueprint
import face_recognition
from flask import request, redirect, jsonify, render_template

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

    return render_template("view.html")


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
        result = {
            "faces-match": face_match,
            "error": "no face found",
            "code": "500"
        }
        return jsonify(result)
    elif len(unknown_face_locations) == 0:
        result = {
            "faces-match": face_match,
            "error": "no face found",
            "code": "500"
        }
        return jsonify(result)
    else:
        known_face_encodings = face_recognition.face_encodings(known_image, known_face_locations)[0]
        unknown_face_encodings = face_recognition.face_encodings(unknown_image, unknown_face_locations)
        match = face_recognition.compare_faces([known_face_encodings], unknown_face_encodings[0], 0.50)
        if match[0]:
            face_match = True
        # Return the result as json
        result = {
            "faces-match": face_match,
            "error": "",
            "code": "200"
        }
        return jsonify(result)
