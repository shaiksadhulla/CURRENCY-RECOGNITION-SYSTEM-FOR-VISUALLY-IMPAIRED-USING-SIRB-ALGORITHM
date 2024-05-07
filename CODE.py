# test file
# TODO:
# Figure out four point transform
# Figure out testing data warping
# Use webcam as input
# Figure out how to use contours
# Currently detects inner rect -> detect outermost rectangle
# Try using video stream from android phone
from utils import*
from matplotlib import pyplot as plt
import subprocess
from gtts import gTTS
import pyglet
import cv2
#from playsound import playsound
# histogram(img)
# fourier(img)
# img = harris_edge(img)
# display('image',img)
# show the original image and the edge detected image
# cv2.imshow("Image", image)
# cv2.imshow("Edged", edged)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
# must define here
max_val = 8
max_pt = -1
max_kp = 0
orb = cv2.ORB_create()
# orb is an alternative to SIFT
#test_img = read_img('files/test_100_2.jpg')
#test_img = read_img('files/test_100_2.jpg')
#test_img = read_img('files/test_100_3.jpg')
#test_img = read_img('files/test_20_4.jpg')
cap = cv2.VideoCapture(0)
ret,frame = cap.read()
cap.release()
cv2.imwrite('PIC .JPG',frame)
test_img = ('PIC .JPG')
# resizing must be dynamic
original = (test_img, 0.4)
('original', original)
# keypoints and descriptors
# (kp1, des1) = orb.detectAndCompute(test_img, None)
(kp1, des1) = orb.detectAndCompute(test_img, None)
training_set = ['files/10.jpg','files/20.jpg', 'files/50.jpg', 'files/100.jpg',
'files/500.jpg','files/500.jpg']
for i in range(0, len(training_set)):
# train image
    train_img = cv2.imread(training_set[i])
    (kp2, des2) = orb.detectAndCompute(train_img, None)
# brute force matcher
    bf = cv2.BFMatcher()
    all_matches = bf.knnMatch(des1, des2, k=2)
    good = []
# give an arbitrary number -> 0.789
# if good -> append to list of good matches
for (m, n) in all_matches:
    if m.distance < 0.789 * n.distance:
        good.append([m])
if len(good) > max_val:
    max_val = len(good)
    max_pt = i
    max_kp = kp2
    print(i, ' ', training_set[i], ' ', len(good))
    if max_val != 8:
        print(training_set[max_pt])
        print('good matches ', max_val)
        train_img = cv2.imread(training_set[max_pt])
        img3 = cv2.drawMatchesKnn(test_img, kp1, train_img, max_kp, good, 4)
        note = str(training_set[max_pt])[6:-4]
        print('\nDetected denomination: Rs. ', note)
        audio_file = 'audio/' + note + '.mp3'
        audio = pyglet.media.load(audio_file,streaming=False)
        audio.play()
        pyglet.clock.schedule_once(lambda dt:pyglet.app.exit() , audio.duration)
        pyglet.app.run()
        # audio_file = "value.mp3
        # tts = gTTS(text=speech_out, lang="en")
        # tts.save(audio_file)
        #return_code = subprocess.call(["afplay", audio_file])
        (plt.imshow(img3), plt.show())
else:
    print('No Matches')
App.py
from flask import Flask, request, jsonify
import flask
import werkzeug
import re
# from detect import *
app = Flask(__name__)
@app.route('/', methods=['GET'])
def check():
    return 'OK'
@app.route('/post', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you arejust testing the POST functionality
    if param:
        return jsonify({"Message": "Welcome {param} to our awesome platform!!","METHOD": "POST"})
    else:
        return jsonify({"ERROR": "no name found, please send a name."})
@app.route('/image', methods=['POST'])
def handle_request():
    files_ids = list(flask.request.files)
    image_num = 1
    file_name = ""
    for file_id in files_ids:
        imagefile = flask.request.files[file_id]
        filename = werkzeug.utils.secure_filename(imagefile.filename)
        print("Image Filename : " + imagefile.filename)
        imagefile.save(filename)
        file_name = filename
        image_num = image_num + 1
        from detect import helper
        note = helper(file_name)
        note += ".jpg"
        print("Detected note: ", note)
        currency = ""
        if(re.findall(".*[2][0][0][0].*", note)):
            currency = "2000"
        elif(re.findall(".*[2][0][0][^0].*", note)):
            currency = "200"
        elif(re.findall(".*[2][0][^0].*", note)):
            currency = "20"
        elif(re.findall(".*[1][0][0][^0].*", note)):
            currency = "100"
        elif(re.findall(".*[1][0][^0].*", note)):
            currency = "10"
        elif(re.findall(".*[5][0][0].*", note)):
            currency = "500"
        elif(re.findall(".*[5][0][^0].*", note)):
            currency = "50"
        else:
            currency = "-1"
            print("Detected Currency: ", currency)
            if currency != "-1":
                return jsonify({"note": currency})
            else:
                return jsonify({"note": -1})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4555, debug=True)
# from flask import Flask, request
# import flask
# import werkzeug
# import re
# import cv2
# from detect import helper
# import time
# import requests
# app = Flask(__name__)
# @app.route('/', methods=['GET', 'POST'])
# def check():
# return 'OK'
# @app.route('/image', methods=['POST'])
# def handle_request():
# camera = cv2.VideoCapture(0)
# _, img = camera.read() # Captures the image from the camera
# # Write the captured image to disk
# cv2.imwrite('currency_note.jpg', img)
# # Release the camera
# camera.release()
# # Capture the image from the camera
# cap = cv2.VideoCapture(0)
# ret, frame = cap.read()
# cap.release()
# # Save the image
# cv2.imwrite("note.jpg", frame)
# # Process the image using the detect module
# note = helper("note.jpg")
# note += ".jpg"
# print("Detected note: ", note)
# currency = ""
# if(re.findall(".*[2][0][0][0].*", note)):
# currency = "2000"
# elif(re.findall(".*[2][0][0][^0].*", note)):
# currency = "200"
# elif(re.findall(".*[2][0][^0].*", note)):
# currency = "20"
# elif(re.findall(".*[1][0][0][^0].*", note)):
# currency = "100"
# elif(re.findall(".*[1][0][^0].*", note)):
# currency = "10"
# elif(re.findall(".*[5][0][0].*", note)):
# currency = "500"
# elif(re.findall(".*[5][0][^0].*", note)):
# currency = "50"
# else:
# currency = "-1"
# print("Detected Currency: ", currency)
# if currency != "-1":
# return jsonify({
# "note": currency
# })
# else:
# return jsonify({
# "note": -1
# })
# if __name__ == "__main__":
# app.run(host="0.0.0.0", port=4555, debug=True)
