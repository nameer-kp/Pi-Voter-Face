import psycopg2

import boto3
from flask import Flask, jsonify, make_response
import flask
import face_recognition
app = Flask(__name__)
s3 = boto3.client("s3")

@app.route("/facesvc/",methods=['POST'])
def detect_face():
    conn = psycopg2.connect(
   database="bvoter", user='postgres', password='123456', host='127.0.0.1', port= '5432'
)
    imagefile = flask.request.files['imagefile']
    voter_id=flask.request.form.get("voterid")
    candidate_id=flask.request.form.get("candidateid")
    print("image File",imagefile)
    print("voter id:",voter_id)
    print("candidate id:",candidate_id)
    imagefile.save("given.jpg")
    picture_of_me = face_recognition.load_image_file(imagefile)
    my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

    # downloading the original photo from s3 
    s3.download_file(
    Bucket="bvoter", Key=voter_id+".jpg", Filename="test.jpg")



    # my_face_encoding now contains a universal 'encoding' of my facial features that can be compared to any other picture of a face!

    unknown_picture = face_recognition.load_image_file("test.jpg")
    unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

    # Now we can see the two face encodings are of the same person with `compare_faces`!

    results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)

    if results[0] == True:
        print("Recognized:True")
        # running vote casting 
        cursor = conn.cursor()
        
        cursor.execute('UPDATE candidate SET votes = votes + 1 WHERE candidate_id ='+candidate_id+';')
        conn.commit()
        conn.close()
        return jsonify(error=False)
    else:
        
        print ('Recognized:false')
        conn.close()
        return (jsonify(error=True))
