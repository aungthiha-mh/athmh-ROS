import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)

while cap.isOpened():
        _ , frame1 = cap.read()

        cv2.imshow("Background", frame1)
        key = cv2.waitKey(1)
        if key == 27:
            break

while cap.isOpened():
    
    _ , frame2 = cap.read()
    
    diff = cv2.absdiff(frame1, frame2)
    diff[diff>255] = 255
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 900:
            continue
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 3)
        cnt = contour
        moment = cv2.moments(cnt)
        cx = int(moment['m10']/moment['m00'])
        cy = int(moment['m01']/moment['m00'])
        print("Pixel shape" , frame2.shape)
        print("The centroid is ", cx , cy)
        
    #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

    image = cv2.resize(frame1, (1280,720))
    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()
    
    time.sleep(1)

    if cv2.waitKey(40) == 27:
        break

cap.release()
cv2.destroyAllWindows()