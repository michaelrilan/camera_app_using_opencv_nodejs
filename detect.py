from time import time
import cv2, pandas
import requests
from datetime import datetime
import base64

# Assigning our data_frame to None
data_frame = None
# detect_list when any moving object appear
detect_list = [None,None]
# Time of movement
time = []

# Capturing video
video = cv2.VideoCapture(0)
print('')


def convertToBinaryData(filename):
    # Convert digital data to binary format
    path = filename
    with open(path, 'rb') as file:
        imageBase64 = base64.b64encode(file.read())
        url = 'http://localhost:4676/tolongges'
        check =  {"datetime": str(datetime.now().strftime("%B %d, %Y - ")+ str(datetime.now().strftime("%H:%M %S sec"))), "image": str(imageBase64.decode('utf-8'))}
        sent = requests.post(url, json=check)
        print(sent.text)

    return imageBase64.decode('utf-8')

# Infinite while loop to treat stack of image as video
while True:
    current_dateTime = datetime.now()
    file_name =str(current_dateTime.hour)+str(current_dateTime.minute) + str(current_dateTime.second) + str(current_dateTime.microsecond)


    check, frame = video.read()
    status = 0
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(5, 5),0)

    if data_frame is None:
        data_frame=gray
        continue
    
    delta_frame=cv2.absdiff(data_frame,gray)
    thresh_frame=cv2.threshold(delta_frame, 100, 255, cv2.THRESH_BINARY)[1]
    thresh_frame=cv2.dilate(thresh_frame, None, iterations=2)

    cnts,_=cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        status=1
        (x, y, w, h)=cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 3)
        
    detect_list.append(status)
    detect_list=detect_list[-2:]

    # Appending Start time of motion
    if detect_list[-1] == 1 and detect_list[-2] == 0:
        time.append(datetime.now())

	# Appending End time of motion
    if detect_list[-1] == 0 and detect_list[-2] == 1:
        time.append(datetime.now())
        print("MOTION DETECTED" ,datetime.now())
        cv2.imwrite("./upload/image"+str(file_name)+".jpg", frame)
        convertToBinaryData(filename="./upload/image"+str(file_name)+".jpg")

            
    cv2.imshow("MOTION DETECTOR CAMERA",frame)
    # WAITKEY
    key=cv2.waitKey(1)
    if key == ord('c'):
        break
    

video.release()
cv2.destroyAllWindows
