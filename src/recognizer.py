import face_recognition
import cv2
from datetime import datetime
import os
from os import listdir
from os.path import isfile, join
from pickle import load
import pyttsx3
import speech_recognition as sr


video_capture = cv2.VideoCapture(1)

r = sr.Recognizer()


NUM_FACES = 3.0

THRESHOLD = 0.5

GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""{
  "type": "service_account",
  "project_id": "guardbot-200023",
  "private_key_id": "ca92ff685e8f39366871f64ed523aa3a12d1a989",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDlSnGQzm+fgzpt\nJkWslK/DZU7VgAoJI+k/3sZUeWRKNA2IwWjNDHGk6jvZjARkqwieSmUzMtOMvnPl\ntidrCPnTtQi755KB7KDoSO9i09jAS8I4RcvwUk5VN11yRn2jBojcroqkKPNvTsHR\nuU6g/+pfW39ACUYmYGsfqU4R1gDSFA1N6PfbhUqGkrkrFBHCV1cUp6uP1ieI0bJr\nRAGY1sAgJj+M9KQl3eBRFEUKAsYwbvHbtUe8/8Xp+wv8lmbpqsCbRYtAvndI7UzY\nL3HLlFCOTLDO+vssEfdAbcm9ed7bYSvyjXDDhWfAlv5NSk/9lVUJCAfWPdeSmXYw\nD/I7Mx4TAgMBAAECggEAQOFyRi/r7P6Um0sfnwiJvageiRJMhK6ZM14Fz+RzqP2W\nsNJNpev2AlzXZ6UTnyq4axYREc45h1Ni9ya2e7aT/sB0wrrxvXroQyJUPqpEZJFr\nWUICxbN8f+eFNS9WILnaI1vuVipSS/ZEqOQfKDaSKr54wPV+2KAi39goA6sDG25Q\n0MxL6pSYBSrXdbzBETeSgF5fCJbuYS7aAFwf9znIfsAmHStfvdsiseKtX73YTfyP\n4fEmfQzTCe4zHiUx13JkowEBelqs3wSXmvEog6TgBlufhhAhohEkNCuQ1YSQPL7O\nwvxUsUErOQLmva2Y3NAZmIWYynpMT3qnWunWWiWC9QKBgQD/haDu62TRm0mCK0qt\n9GyDPWX2u8n/QKuR4QDt7n5hu6AfMzUxU0nLZE0Qln/oodxKgSaELST3mxqjA9Uf\ncTr+/kL1DVgAR8YS/EHmtlx/vyRE6I4ECO0zyXvOU4EZ5EYEYA1QLalRpNFY7WkM\nMFlQN3GVwwXHjLqBs+cmaEq2XwKBgQDluECuVT7h7yj8daQJh4TGFBTl2yL71hP8\nOyHS6PIdYRkwYVjzSs3/lSly6VEgcVRgPTcpIjbI8QXDxFPdJS11Wd6LByIypfCL\nTlLAp4x02LAdodXPEQyBS3M1CkzXzefQp3050a8asi+EYyPbmwcLeInKElkbXdPf\nR7hFXfFszQKBgHWJQEfmW4/XQG7x/v4Ziriry3U9WGNjmggWWdkYdWX7amIvqe4w\ng6ddUd2pfNjDa5OR6Oev5GtJG22U27oE2cBlsOML6kjmuwQMqTu48r+IauSPnJPa\nj1HdAmgcHSyNxm9Ix5b0CgiWKf4f5sxGiS7O8h6TgNsTrs7utAsEuik9AoGATT2K\n4hNftXBJA7o6kcmzZzbRYAgy1yLATYtEcDpLTn2bjpzs38FDSrDI4w54bMQubr2m\nknoimaYRHiYhXLZndpHlNjIL2aPaIb0QLh8oJxHFBfGohptg7QiFkEwKUnW1gH8Q\nqCRNEFjhiU4cfHbAA6dgDUXmGEGQP/9Jgml4B/ECgYAPEXVgvNZb7ZsXphIgzMWJ\ntj4FcuWxgXwW9uBsJ3Ma50ijuYZiTiGOH2N2n848OYF0K+8YuCrdDbrq5rVasA46\n5IKdDkNMol/SEsQvmMNeb+xhFJER71YEt6Jr9NOmJKq+Esh/ssXmwMYi7ceru77Z\nJMdYOSppNzzZXKqxECrDnw==\n-----END PRIVATE KEY-----\n",
  "client_email": "guardbot@guardbot-200023.iam.gserviceaccount.com",
  "client_id": "112203121764581840115",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/guardbot%40guardbot-200023.iam.gserviceaccount.com"
}
"""

def get_response():
    with sr.Microphone(device_index=0) as source:
        audio = r.listen(source)
    with open("microphone-results.wav", "wb") as f:
        f.write(audio.get_wav_data())

    try: 
        text =  (r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)).rstrip().lower()
    except Exception as e:
        print(e)
        text = ""
    return text

with open("kfn.pickle", "rb") as f:
    known_face_names = load(f)
    f.close()

with open("kfe.pickle", "rb") as f:
    known_face_encodings = load(f)
    f.close()

face_locations = []
face_names = []
process_this_frame = True

starttime = datetime.now()

seenFace = False

while (datetime.now()-starttime).total_seconds() < 5 and not seenFace:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []

        if len(face_encodings) > 0:
            seenFace = True
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    #print(matches.count(True))
                    matchCount = {"Matt":0, "Ben":0, "Epstein":0}

                    #print(len(matches))

                    for i in range(len(matches)):
                        if matches[i]:
                            matchCount[known_face_names[i]] += 1


                    print(matchCount)

                    maxCount = -1
                    maxName = "Unknown"        
                    for (name, count) in matchCount.items():
                        if count > maxCount:
                            maxName = name
                            maxCount = count

                    if maxCount > ((len(known_face_names)/NUM_FACES)*THRESHOLD):
                        face_names.append(maxName)
                    else:
                        face_names.append("Unknown")

                else:
                    face_names.append("Unknown")
                #face_names.append(name)

                for face in face_names:
                    engine = pyttsx3.init()
                    #engine.getProperty('rate')
                    engine.getProperty('volume')
                    #engine.setProperty('rate', 100)
                    engine.setProperty('volume', 1)
                    if face == "Unknown":
                        engine.say("I don't know who you are! What is the passphrase?")
                        engine.runAndWait()
                       # print(get_response())
                        resp = get_response()
                        print(resp)
                        if resp == "the quick brown fox jumped over the lazy dog":
                            engine.say("Welcome to Halligan. Have a great day!")
                            engine.runAndWait()
                        else:
                            filename = "intruder" + str(datetime.now()) + ".jpg"
                            cv2.imwrite("../intruders/" + filename, frame)
                            engine.say("Intruder alert!")
                            engine.runAndWait()
                    else:
                        engine.say("Hello " + face)
                        engine.runAndWait()
                    

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()