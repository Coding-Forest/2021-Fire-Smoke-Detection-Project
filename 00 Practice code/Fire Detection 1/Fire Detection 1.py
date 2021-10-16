import cv2
import os
import numpy as np
import smtplib
from playsound import playsound

# Video used: https://www.youtube.com/watch?v=aL9c-4EerTo&ab_channel=NBCNews
video = cv2.VideoCapture("video/Homes Evacuated As Wildfire Threatens To Engulf Manavgat, Turkey.mp4")

# while while is running, we extract the frames.
while True:

    ret, frame = video.read() # ret (boolean) - whether the frame data is there
    frame = cv2.resize(frame, dsize=(0,0), fx=0.65, fy=0.65)
    blur = cv2.GaussianBlur(frame, (15, 15), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # Set colour range for fire & smoke.
    # This range will be used to black out non-fire/smoke objects and highlight fire and smoke only.
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
