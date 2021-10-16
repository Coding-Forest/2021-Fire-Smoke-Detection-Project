import cv2
import os
import numpy as np
import smtplib
from playsound import playsound

FIRE_REPORTED = 0
ALARM_STATUS = False
EMAIL_STATUS = False
audio = os.path.dirname(__file__) + "/firealarm.wav"

def send_email_alert():
    receiver_email = "Fire Engine Email Address"
    receiver_email = receiver_email.lower()

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("system_email", "password")
        server.sendmail("system_email", receiver_email, "Warning: a fire incident has been reported in your office.")
        print("sent to {}".format(receiver_email))
    except Exception as e:
        print(e)


video = cv2.VideoCapture("video/Homes Evacuated As Wildfire Threatens To Engulf Manavgat, Turkey.mp4")

# while while is running, we extract the frames.
while True:

    ret, frame = video.read() # ret (boolean) - whether the frame data is there
    frame = cv2.resize(frame, dsize=(0,0), fx=0.65, fy=0.65)
    blur = cv2.GaussianBlur(frame, (15, 15), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # Set colour range for fire & smoke.
    lower = [18, 50, 50]
    upper = [35, 255, 255]

    lower = np.array(lower, dtype='uint8')
    upper = np.array(upper, dtype='uint8')

    # create a mask
    # we are looking for two types of colours (lower & upper) in the hsv frames.
    mask = cv2.inRange(hsv, lower, upper)

    output = cv2.bitwise_and(frame, hsv, mask=mask)

    # filter fire image by the size of fire
    fire_size = cv2.countNonZero(mask)

    if int(fire_size) > 50000:
        #print("Fire detected")
        FIRE_REPORTED += 1

        if FIRE_REPORTED >= 1:
            if ALARM_STATUS == False:
                #playsound('audio/firealarm.wav')
                ALARM_STATUS = True
            if (EMAIL_STATUS == False):
                send_email_alert()
                EMAIL_STATUS = True

    if (ret == False):
        break           # if no frame, break out.

    cv2.imshow("Output", output)

    if cv2.waitKey(7) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
video.release()
