from time import sleep
from flask import Flask, jsonify, make_response
import flask
import face_recognition
app = Flask(__name__)

@app.route("/facesvc/",methods=['POST'])
def detect_face():
    imagefile = flask.request.files['imagefile']
    print("image File",imagefile)
    imagefile.save("given.jpg")
    picture_of_me = face_recognition.load_image_file(imagefile)
    my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

    # my_face_encoding now contains a universal 'encoding' of my facial features that can be compared to any other picture of a face!

    unknown_picture = face_recognition.load_image_file("test.jpeg")
    unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

    # Now we can see the two face encodings are of the same person with `compare_faces`!

    results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)

    if results[0] == True:
        print("Recognized:True")
        
        return jsonify(error=False)
    else:
        
        print ('Recognized:false')
        return (jsonify(error=True))
        
if __name__=='__main__':
    app.run(debug=True)