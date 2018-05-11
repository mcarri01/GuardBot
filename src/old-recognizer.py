import cv2
import numpy as np

recognizer = cv2.createLBPHFaceRecognizer()
recognizer.load('trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);


cam = cv2.VideoCapture(1)
font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1)
while True:
    ret, im =cam.read()
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray, 1.2,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
        Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
        print(id, conf)
        if(conf > 50):
            if(Id==1):
                Id="Matt"
            elif(Id==2):
                Id="Ben"
            elif(Id==3):
            	Id="Epstein"
            elif(Id==4):
            	Id="Rutt"
        else:
            Id="Unknown"
        cv2.cv.PutText(cv2.cv.fromarray(im),str(Id), (x,y+h),font, 255)
    cv2.imshow('im',im) 
    if cv2.waitKey(10) and 0xFF==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()