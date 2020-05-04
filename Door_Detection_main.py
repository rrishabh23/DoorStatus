
import datetime
import imutils
import cv2
import time

minarea=500 #thershold for ignoring small changes
refPt = []
cropping = False
start=time.time()
pvtext="Closed"

def getROI(image):
    def click_and_crop(event, x, y, flags, param):
        global refPt, cropping
        if event == cv2.EVENT_LBUTTONDOWN:
            refPt = [(x, y)]
            cropping = True
        elif event == cv2.EVENT_LBUTTONUP:
            refPt.append((x, y))
            cropping = False
            cv2.rectangle(image,refPt[0],refPt[1],(0,255,0),2)
            cv2.imshow("BGimage", image)
    
    clone = image.copy()
    cv2.namedWindow("BGimage")
    cv2.setMouseCallback("BGimage", click_and_crop)
    while True:
    	cv2.imshow("BGimage", image)
    	key = cv2.waitKey(1) & 0xFF
    	if key == ord("r"):
    		image = clone.copy()
    	elif key == ord("c"):
    		break
    if len(refPt) == 2:
        roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        cv2.imshow("ROI", roi)
    key = cv2.waitKey(1) & 0xFF
    cv2.destroyAllWindows()

cap = cv2.VideoCapture('DoorProblem.mp4')# cv2.VideoCapture(0) for live from camera
firstFrame = None
ret, frame = cap.read()
getROI(frame)

while True:
    ret, frame = cap.read()
    if frame is None:
        break

    text="Closed"
    frame=frame[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    if firstFrame is None:
        firstFrame = gray
        continue
    
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)    
    for c in cnts:
        if cv2.contourArea(c) < minarea:
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Opened"

        
    cv2.putText(frame, "Door Status: {}".format(text), (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    if text == "Opened" and pvtext =="Closed":
        pvtext="Opened"
        start=time.time()
        stat=datetime.datetime.now().strftime("%I:%M:%S%p %A %d %B %Y")
        outdict=text+" at "+stat+"\n"
        print(outdict)
        with open('output.txt', 'a') as file:
            file.write(outdict)
            
    if text == "Closed" and pvtext =="Opened":
        pvtext="Closed"
        end=time.time()
        duration=str(end-start)
        stat=datetime.datetime.now().strftime("%I:%M:%S%p %A %d %B %Y")
        outdict=text+" at "+stat+"\n Duration : "+duration+"\n"
        print(outdict)
        with open('output.txt', 'a') as file:
            file.write(outdict)
            
    cv2.imshow("Video Feed", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()        
