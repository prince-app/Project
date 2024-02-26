import face_recognition
import cv2
import numpy as np
import csv 
import os
import time
from datetime import datetime

video_capture = cv2.VideoCapture(0)

imgBackground=cv2.imread("Back_1.jpg")
#imgBackground=cv2.imread("Back_2.jpeg")

ratan_image =  face_recognition.load_image_file("ratan_tata.jpeg")
ratan_encoding= face_recognition.face_encodings(ratan_image)[0]

sadmona_image = face_recognition.load_image_file("sadmona.jpeg")
sadmona_encoding = face_recognition.face_encodings(sadmona_image)[0]

elon_image = face_recognition.load_image_file("elon.jpeg")
elon_encoding= face_recognition.face_encodings(elon_image)[0]

trump_image = face_recognition.load_image_file("trump.jpeg")
trump_encoding = face_recognition.face_encodings(trump_image)[0]


known_face_encoding = [ratan_encoding,sadmona_encoding,elon_encoding,trump_encoding]
known_face_names = ["ratan","sadmona","elon","trump"]


students = known_face_names.copy()

face_locations =[]
face_encodings = []

s=True

now =datetime.now()
current_date = now.strftime("%Y-%m-%d")

"""f = open(current_date+'csv','w+',newline= '')
lnwriter = csv.writer(f)
"""
COL_NAMES=['NAME','TIME']
capture=0

while True:
    _,b_frame = video_capture.read()
    frame = cv2.resize(b_frame, (640, 480))
    small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)# take 25% of width and height of the frame
    rgb_small_frame = small_frame[:,:,::-1] #used to convert BGR to RGB to access through face_recognition
    if s:
        face_locations = face_recognition.face_locations(rgb_small_frame)# get location of face
        face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)# encode rgb_small_frame of current video
        face_names=[]
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encoding,face_encoding)#compare know_face_encoding with face_encoding
            name=""
            face_distance = face_recognition.face_distance(known_face_encoding,face_encoding)# determine  Euclidean distance that determine simillarity or dissimilarity between given images
            best_match_index = np.argmin(face_distance)# vo photo nikalega jiska distance sbse kam hoga
            if matches[best_match_index]:
                name = known_face_names[best_match_index]  # here we get the name
            face_names.append(name)
            exist=os.path.isfile('attendence_'+current_date+'.csv')
            if name in known_face_names:
                if name in students:
                    index=students.index(name)
                    capture=students.pop(index)
                    print(capture)
                    ts=time.time()
                    timestamp=datetime.fromtimestamp(ts).strftime("%H-%M-%S")
                    attendence=[capture,str(timestamp)]
    #imgBackground[40:40+720,400:400+1280]=frame
    imgBackground[119:119+480,426:426+640]=frame
    cv2.imshow ("back",imgBackground)
    k=cv2.waitKey(1)
    if k==ord('o'):
        if exist:
            with open('attendence_'+current_date+'.csv','a') as csvfile:
                  writer=csv.writer(csvfile)
                  writer.writerow(attendence)
            csvfile.close()
        else:
            with open('attendence_'+current_date+'.csv','w') as csvfile:
                    writer=csv.writer(csvfile)
                    writer.writerow(COL_NAMES)
                    writer.writerow(attendence)
            csvfile.close()
        x, y, w, h = 20, 420, 380,60
        imgBackground[y:y+h, x:x+w] = [255, 255, 255]
        cv2.putText(imgBackground,capture+' attendence taken',(20,450),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,0,255),1)
        print(capture,"attendence taken")
    if k==27:
        break
video_capture.release()
cv2.destroyAllWindows()