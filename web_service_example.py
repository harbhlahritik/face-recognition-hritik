# This is a _very simple_ example of a web service that recognizes faces in uploaded images.
# Upload an image file and it will check if the image contains a picture of Barack hritik.
# The result is returned as json. For example:
#
# $ curl -XPOST -F "file=@hritik2.jpg" http://127.0.0.1:5001
#
# Returns:
#
# {
#  "face_found_in_image": true,
#  "is_picture_of_hritik": true
# }
#
# This example is based on the Flask file upload example: http://flask.pocoo.org/docs/0.12/patterns/fileuploads/

# NOTE: This example requires flask to be installed! You can install it with pip:
# $ pip3 install flask

import face_recognition
from flask import Flask, jsonify, request, redirect
from flask_cors import CORS

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
cors = CORS(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        print(request)
        print(request.files)
        print('POST req made')
        if 'file' not in request.files:
            print('cond1')
            return redirect(request.url)
            
        file = request.files['file']

        # if file.filename == '':
        #     print('cond2')
        #     return redirect(request.url)
            

        if file: #and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            print('cond3')
            return detect_faces_in_image(file)
            

    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
    <title>Is this a picture of Hritik?</title>
    <h1>Upload a picture and see if it's a picture of Hritik!</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''


def detect_faces_in_image(file_stream):
    # Pre-calculated face encoding of hritik generated with face_recognition.face_encodings(img)
    known_face_encoding = known_encoding = [-0.14189549,  0.02840434,  0.03060029, -0.04220764, -0.08258746, -0.01038735,
                                            -0.05054608,  0.01341709,  0.13794267, -0.05054399,  0.12679884, -0.02941008,
                                            -0.17247473, -0.07214808, -0.03888275,  0.18218063, -0.09585102, -0.13972518,
                                            -0.05326696, -0.10763577,  0.03755522,  0.01990773,  0.00477302,  0.07811141,
                                            -0.16968998, -0.39463857, -0.0853466,  -0.13178149, -0.04387482, -0.12261344,
                                            -0.00914054,  0.09322724, -0.12963828, -0.03260205,  0.02331699,  0.09727034,
                                             0.00072699, -0.04090156,  0.20119995,  0.02345594, -0.13058566, -0.0208432,
                                             0.07213442,  0.29717186,  0.1562805,   0.07015238,  0.04946823, -0.0162633,
                                             0.10699353, -0.16787107,  0.09763248,  0.11137456,  0.04723993,  0.04325373,
                                             0.11783434, -0.08900361,  0.04189414,  0.0874739,  -0.14165829,  0.04684374,
                                            -0.01174501, -0.04831273, -0.01679802, -0.06638986,  0.25587323,  0.07443199,
                                            -0.0791087,  -0.08679259,  0.16118896, -0.12538114, -0.04018664, -0.03619158,
                                            -0.14280993, -0.12820593, -0.31923297,  0.05977997,  0.37364471,  0.15574211,
                                            -0.18282041,  0.08106919, -0.0116168,  -0.04587944,  0.09462462,  0.09454387,
                                            -0.12680344,  0.01578439, -0.07384188,  0.0394046,   0.18211065,  0.05594469,
                                            -0.04645434,  0.14667167, -0.0099638,   0.04305034,  0.06307471, -0.0110201,
                                            -0.13049966, -0.01394295, -0.09960652, -0.02880733,  0.07726152, -0.04985272,
                                             0.02243743,  0.14216198, -0.1423347,   0.08754129, -0.03184474,  0.00518119,
                                            -0.03532645,  0.14164242, -0.18028848, -0.09034695,  0.12778267, -0.14696278,
                                             0.10954713,  0.14433029,  0.00956202,  0.11875574,  0.13283458,  0.09769689,
                                            -0.02975816,  0.03685673, -0.16462086, -0.00170297,  0.11134495,  0.00113312,
                                             0.10447399,  0.08343621]

    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image
    unknown_face_encodings = face_recognition.face_encodings(img)

    face_found = False
    is_hritik = False

    if len(unknown_face_encodings) > 0:
        face_found = True
        # See if the first face in the uploaded image matches the known face of hritik
        match_results = face_recognition.compare_faces([known_face_encoding], unknown_face_encodings[0])
        if match_results[0]:
            is_hritik = True

    # Return the result as json
    result = {
        "face_found_in_image": face_found,
        "is_picture_of_hritik": is_hritik
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=False)
