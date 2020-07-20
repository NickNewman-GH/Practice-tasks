from __future__ import print_function
import cv2 as cv
import numpy as np
import argparse

cap = cv.VideoCapture('Elster.mp4')
feature_params = dict( maxCorners = 100, 
                       qualityLevel = 0.3, 
                       minDistance = 7, 
                       blockSize = 7) 
lk_params = dict( winSize = (15, 15), 
                  maxLevel = 2, 
                  criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))
color = np.random.randint(0, 255, (100, 3))
ret, old_frame = cap.read()
old_frame = cv.resize(old_frame,(1600,900))
old_gray = cv.cvtColor(old_frame, cv.COLOR_BGR2GRAY) 
p0 = cv.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
mask = np.zeros_like(old_frame)
while(1):
    ret, frame = cap.read()
    try:
        frame = cv.resize(frame,(1600,900))
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    except:
        cv.destroyAllWindows() 
        cap.release()
        exit(0)

    p1, st, err = cv.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    good_new = p1[st==1]
    good_old = p0[st==1]

    for i,(new,old) in enumerate(zip(good_new, good_old)):
        a,b = new.ravel()
        c,d = old.ravel()
        mask = cv.line(mask, (a,b),(c,d), color[i].tolist(), 2)
        frame = cv.circle(frame,(a,b),5,color[i].tolist(),-1)
    img = cv.add(frame,mask)

    cv.imshow('frame',img)
    k = cv.waitKey(10)
    if k >= 10: 
        break

    old_gray = frame_gray.copy() 
    p0 = good_new.reshape(-1, 1, 2)
  
cv.destroyAllWindows() 
cap.release()
