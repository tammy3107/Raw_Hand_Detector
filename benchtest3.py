import cv2 
import numpy as np
import math

port = 1
bg = cv2.createBackgroundSubtractorMOG2()
camera = cv2.VideoCapture(port)
while (camera.isOpened()):
	ret, img= camera.read()
	if ret:
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	#edge = cv2.Canny(gray,50,150,apertureSize=3)
	gray = cv2.GaussianBlur(gray,(5,5),0)
	hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv,np.array([2,50,50]),np.array([15,255,255]))
	#####morphing#########
	k_square = np.ones((11,11),np.uint8)
	k_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))

	#ret, thresh = cv2.threshold(gray,45,255,cv2.THRESH_BINARY_INV)
	#thresh = cv2.erode(thresh,None,iterations=2)
	thresh = cv2.dilate(mask,k_ellipse,iterations=1)
	thresh = cv2.erode(thresh,k_square,iterations=1)
	thresh = cv2.dilate(thresh,k_ellipse,iterations=1)
	thresh1 = cv2.medianBlur(thresh,5)

	k_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(8,8))
	thresh = cv2.dilate(thresh1,k_ellipse,iterations=1)
	k_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
	thresh = cv2.medianBlur(thresh,5)
	ret, thresh = cv2.threshold(thresh,127,255,cv2.THRESH_BINARY)
	#thresh = bg.apply(thresh)
	#thresh = cv2.GaussianBlur(thresh,(5,5),0)
	image,contours,hier = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	max_ar = -1
	cnt_index = 0
	for i in range(len(contours)):
		cnt = contours[i]
		area = cv2.contourArea(cnt)
		if (area>max_ar):
			max_ar = area
			cnt_index = i
	cnts = contours[cnt_index]
	hull = cv2.convexHull(cnts)
	#print cnts
	#cv2.circle(img,(3,4),3,(0,0,255),3)
	hull2 = cv2.convexHull(cnts,returnPoints = False)
	defect = cv2.convexityDefects(cnts,hull2)
	fingers=0
	for i in range(defect.shape[0]):
		#fingers = 0
		s,e,f,d = defect[i,0]
		start = tuple(cnts[s][0])
		end = tuple(cnts[e][0])
		far = tuple(cnts[f][0])
		a = math.sqrt((end[0]-start[0])**2+(end[1]-start[1])**2)
		b = math.sqrt((far[0]-start[0])**2+(far[1]-start[1])**2)
		c = math.sqrt((end[0]-far[0])**2+(end[1]-far[1])**2)
		angle = math.acos((b**2+c**2-a**2)/(2*b*c))
		if angle<math.pi/2:
			fingers = fingers+1;
			cv2.circle(img,far,3,(0,0,255),3)
		cv2.line(img,start,end,(255,0,0),2)
		print fingers
		#cv2.circle(img,far,3,(0,0,255),3)
	cv2.drawContours(img,[hull],-1,(0,255,0),2)
    
    
    
	#contours = 
	#bgmask = cv2.GaussianBlur(bgmask,(5,5),0)
	"""for cnt in contours:
	    if not (cv2.isContourConvex(cnt)):
		    hull = cv2.convexHull(cnt)
		    cv2.drawContours(img,[hull],-1,(0,255,0),2)"""
	cv2.imshow("test",img)
	#cv2.imwrite("success_benchtest.mp4",img)
	k = cv2.waitKey(1)
	if k==27:
		break