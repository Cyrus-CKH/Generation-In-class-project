import cv2
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont
import face_recognition

recognizer = cv2.face.LBPHFaceRecognizer_create()  
recognizer.read('/Users/cyrus/Desktop/Face/recognizer/trainingData.yml')
cascadePath = '.venv/lib/python3.10/site-packages/cv2/data/haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascadePath);
font = ImageFont.load_default #sudo apt-get install fonts-noto-cjk
id = 0
names = ['None', 'Cyrus'] #the names of the people in the dataset
camema = cv2.VideoCapture(0)
camema.set(3, 640) # set video widht
camema.set(4, 480) # set video height
minW = 0.1*camema.get(3)
minH = 0.1*camema.get(4)
blue = (255,0,0)
green = (0,255,0)
red = (0,0,255)
while True:
    ret, img = camema.read()
    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor = 1.2, minNeighbors = 5, minSize = (int(minW), int(minH)) )
    for(x,y,w,h) in faces:
        match_results = []
        cur_face_locs = face_recognition.face_locations(img)
        cv2.rectangle(img, (x,y), (x+w,y+h), green, 2)
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        if (confidence < 100):
            name = names[id]
            confidence = str(100 - round(confidence)) +"%"
        else:
            name = "未知"
            confidence = str(100 - round(confidence)) +"%" 
        
        match_results.append({
            'name': name,
            'location': cur_face_locs,
        })
    cv2.imshow('image',img) 
    k = cv2.waitKey(10) & 0xff # wait0.01s , press 'ESC' to exit
    if k == 27:
        break

print("\n程式結束")
camema.release()
cv2.destroyAllWindows()