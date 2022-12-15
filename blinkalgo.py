import cv2
import dlib
import math
import smtplib
import ssl
import requests
import json
from timeit import default_timer as timer
import geocoder
from twilio.rest import Client

alertvalue = 6.0


def eudist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def findmid(p1, p2):
    return (p1.x + p2.x) / 2, (p1.y + p2.y) / 2



def gbr(eyevalue, facevalue):
    left = (facevalue.part(eyevalue[0]).x,facevalue.part(eyevalue[0]).y)
    right = (facevalue.part(eyevalue[3]).x,facevalue.part(eyevalue[3]).y)
    top = findmid(facevalue.part(eyevalue[1]),facevalue.part(eyevalue[2]))
    bottom = findmid(facevalue.part(eyevalue[5]),facevalue.part(eyevalue[4]))
    straightlen = eudist(left, right)
    updownlen = eudist(top, bottom)
    ans = straightlen / updownlen
    return ans


cap = cv2.VideoCapture(0)

cv2.namedWindow('Detector')
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("anydatafile.dat")
le = [37, 39, 34, 32, 33, 21]
re = [46, 40, 44, 41, 49, 48]
timeBlink = 0
while True:
    number = "+18283733"
    start = timer()
    TWIML_INSTRUCTIONS_URL = \"http://static.fullstackpython.com/phone-calls-python.xml"
    client = Client("AC6f812f16562c5667126df4110c20abfa","88512cef1bf394ac5483657d8a4a4bd4")
    retval, frame = cap.read()
    if not retval:
        print("Exiting")
    break
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces, _, _ = detector.run(image=frame, upsample_num_times=0,adjust_threshold=0.0)
    for face in faces:
        landmarks = predictor(frame, face)
    ler = gbr(le, landmarks)
    rer = gbr(re, landmarks)
    blinkratio = (ler + rer) / 2
    if blinkratio > alertvalue:
        timeBlink = timeBlink+1
    print(timeBlink)
    print(timer()-start)
    cv2.putText(frame, "BLINKING", (12, 43), cv2.FONT_HERSHEY_SIMPLEX,2, (255, 255, 255), 2, cv2.LINE_AA)
    port = 465
    password = "vaibhavhero1"
    context = ssl.create_default_context()
    if timeBlink >= 4 and timer()-start <= 5:
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("iotprt@gmail.com", password)
    myloc = geocoder.ip('me')
    print(myloc.latlng)
    message = "Hello, the device connected to this email has been found driving in an unsafe environmentnear " + \
              str(myloc.address)
    print("Dialing " + "+91382")
    client.calls.create(to="+916390014", from_=number, url=TWIML_INSTRUCTIONS_URL, method="GET")
    print(message)
    server.sendmail("iotprt@gmail.com", "temp@gmail.com", "Hello, the device connected to thisemail has been found driving in an unsafe environment near "+str(myloc.address) +". Exact
    location"+str(myloc.latlng)+". The engine has been shut down as a caution-measure. Please contact the driver
    ASAP")
    timeBlink = 0
    start = timer()
    cv2.imshow('Detector', frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()