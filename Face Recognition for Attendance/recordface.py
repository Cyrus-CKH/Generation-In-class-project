import cv2
import os
import pymysql
import time

# build connection to database
db = pymysql.connect(host ='localhost',
                    user= 'root',
                    password ='********',
                    database = 'facetest')

# create cursor
cursor = db.cursor()

# create recognizer
if not os.path.exists('dataset'): # if dataset folder does not exist
    os.mkdir('dataset') # create dataset folder
    print('folder created') 

# Ask for user ID
user_id = input('Please enter your ID: ')
print("\n [INFO] face capture. Look at the camera and wait ...")

imgCapture = 30 # each user will have 30 images
saveFace = False # flag to save face
frameColor = (255,0,0) # color of rectangle around face
userDir = "User_" # directory name for each user
beginTime = 0 # start time

# open camera
webcam = cv2.VideoCapture(0)
webcam.set(3, 640) # set video width
webcam.set(4, 480) # set video height

#  create classifier
detector = cv2.CascadeClassifier('.venv/lib/python3.10/site-packages/cv2/data/haarcascade_frontalface_default.xml')

# start capturing images
count = 0 # initialize count
frameRate = 5 # set frame rate
prevTime = 0 # initialize previous time
while webcam.isOpened():
    timeElapsed = time.time() - prevTime
    ok, frame = webcam.read() # read frame from webcam
    if not ok: break
    cv2.putText(frame, "Press 'f' to start face capture", (10, 480-10), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,255,255), 2)

    if timeElapsed > 1./frameRate:
        prevTime = time.time()
        # face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # transform to gray scale
        faces = detector.detectMultiScale(gray, scaleFactor = 1.3, minNeighbors = 5) # detect faces
        # if face is detected
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 2) # draw rectangle around face
            # save face
            if saveFace:
                roiGray = gray[y:y+h, x:x+w] # get face region of interest
                fileName = userDir + "/" + f'{count:02}' + ".jpg" # create file name
                cv2.imwrite(fileName, roiGray) # save image
                cv2.imshow("face", roiGray) # show face
                count += 1 # count+1

    cv2.imshow('frame', frame) # show frame
    # Press 'f' to begin detect,
    # Press ESC or 'q' to quit
    key = cv2.waitKey(1) & 0xff
    if key == 27 or key == ord('q'):
        break
    elif key == ord('f') and not saveFace: # if 'f' is pressed and face is not saved
        saveFace = True # save face
        frameColor = (0, 255, 0) # change frame color to green
        beginTime = time.time() # start time
        # create directory for each user
        userDir = "dataset/" + user_id
        userpic = os.path.join('dataset/'+ str(user_id) + '.' + str(count) + ".jpg") # create file name
        if not os.path.exists(userDir): # if directory does not exist
            os.makedirs(userDir) # create directory
    
    # break when count >= imgCapture 
    if count > imgCapture:
        break

# release camera
webcam.release()

# SQL query to insert user ID into database
sql = """INSERT INTO student_info(student_id,
         full_name, age, sex)
         VALUES ('Chan', 'Ka Ho', 28, 'M'), ('Chan','Kaa Hoo', 24, 'F')"""
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()
 
# SQL query to select all records from the table
db.close()

cv2.destroyAllWindows()
print("DONE")
elapsedTime = round(time.time() - beginTime, 4)
print("Elapsed time: " + str(elapsedTime) + "s")