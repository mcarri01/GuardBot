import face_recognition
import cv2
from os import listdir
from os.path import isfile, join
from pickle import dump


mypath = "dataset/"

trainingFiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

known_face_encodings = []

known_face_names = []

failed = 0
recognized = 0

NUM_FACES = 2.0

THRESHOLD = 0.5

print(len(trainingFiles))

for f in trainingFiles:
    
    image = face_recognition.load_image_file("dataset/" + f)
    try: 
        face_encoding = face_recognition.face_encodings(image)[0]
        fArr = f.split('.')
        if fArr[1] == '1':
            print(f, "Matt CF")
            known_face_names.append("Matt CF")
            known_face_encodings.append(face_encoding)
        elif fArr[1] == '2':
            print(f, "Ben")
            known_face_names.append("Ben")
            known_face_encodings.append(face_encoding)
        elif fArr[1] == '3':
            print(f, "Matt")
            known_face_names.append("Matt")
            known_face_encodings.append(face_encoding)

        elif fArr[1] == '4':
            print(f, "Cool Tom")
            known_face_names.append("Cool Tom")
            known_face_encodings.append(face_encoding)

        recognized += 1
    except:
        failed += 1
        pass


#print(known_face_encodings)
#print(known_face_names)

with open("kfe.pickle", "wb") as f:
    dump(known_face_encodings, f)
    f.close()

with open("kfn.pickle", "wb") as f:
    dump(known_face_names, f)
    f.close()



print(len(known_face_encodings), len(known_face_names))

print(recognized, failed)