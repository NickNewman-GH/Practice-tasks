from __future__ import print_function
import cv2 as cv
import numpy as np
import argparse

#parser = argparse.ArgumentParser(description='Code for Feature Detection tutorial.')
#parser.add_argument('--input', help='Path to input image.', default='picture1.png')
#args = parser.parse_args()
                #cv.samples.findFile(args.input)
a=0
if a:
    src = cv.imread('picture1.png', cv.IMREAD_GRAYSCALE)
    if src is None:
        print('Could not open or find the image')
        exit(0)

    #-- Step 1: Detect the keypoints using SURF Detector
    minHessian = 2000
    detector = cv.xfeatures2d_SURF.create(hessianThreshold=minHessian)
    keypoints = detector.detect(src)

    #-- Draw keypoints
    img_keypoints = np.empty((src.shape[0], src.shape[1], 3), dtype=np.uint8)
    cv.drawKeypoints(src, keypoints, img_keypoints)

    #-- Show detected (drawn) keypoints
    cv.imshow('SURF Keypoints', img_keypoints)

    cv.waitKey(5000)
#################################
else:
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

        # calculate optical flow
        p1, st, err = cv.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

        # Select good points
        good_new = p1[st==1]
        good_old = p0[st==1]

        # draw the tracks
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

        # Now update the previous frame and previous points
        old_gray = frame_gray.copy() 
        p0 = good_new.reshape(-1, 1, 2)
  
    cv.destroyAllWindows() 
    cap.release()