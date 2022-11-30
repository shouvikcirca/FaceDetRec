import numpy as np
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image
from PIL import Image
from deepface import DeepFace
import os
import cv2
import time

videoTitle = 'facedetrecvideo.mp4'
cap = cv2.VideoCapture(videoTitle)

height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
fps = int(cap.get(cv2.CAP_PROP_FPS))

if not cap.isOpened():
	cap = cv2.VideoCapture(0)
if not cap.isOpened():
	raise IOError("Cannot open video")


app = FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))

isExists = os.path.exists('outputVideo.avi')
if isExists:
	os.remove('outputVideo.avi')
fourcc = cv2.VideoWriter_fourcc('P','I','M','1')
out = cv2.VideoWriter('outputVideo.avi', fourcc, fps, (width, height))

start_time = time.time()

totalFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

j = 0
framesExhausted = 0

subjectImage = cv2.imread('facedetrecsubject.png')

while j<totalFrames:
	for i in range(1):
		ret, frame = cap.read()
		j+=1
		if j >= totalFrames:
			framesExhausted = 1
			break
		cv2.imshow('',np.array(frame, dtype = np.uint8))
		if cv2.waitKey(10) & 0xFF == ord('q'):
			break



	if framesExhausted == 1:
		break
	ret, frame = cap.read()
	j+=1
	faces = app.get(frame)
	if len(faces) == 0:
		#out.write(frame)
		cv2.imshow('',np.array(frame, dtype = np.uint8))
		if cv2.waitKey(10) & 0xFF == ord('q'):
			break
		continue
	victorDistance = float('inf')
	victorFace = ''
	for i in range(len(faces)):
		xmin, ymin, xmax, ymax = faces[i].bbox
		print(type(faces[i]), type(faces[i].bbox))
		croppedIm = Image.fromarray(frame).crop((xmin, ymin, xmax, ymax))
		result = DeepFace.verify(img1_Frame = np.asarray(croppedIm), img2_Frame = subjectImage, enforce_detection=False)
		cosineDistance = result['distance']
		if cosineDistance < victorDistance and cosineDistance < 0.4:
			victorDistance = cosineDistance
			victorFace = i
	
	if victorFace != '':
		xmin, ymin, xmax, ymax = faces[victorFace].bbox
		cv2.rectangle(frame,(int(xmin), int(ymin)),(int(xmax), int(ymax)),(255,0,0),2)
	cv2.imshow('',np.array(frame, dtype = np.uint8))
	#out.write(frame)

	
	if cv2.waitKey(10) & 0xFF == ord('q'):
		break
	
end_time = time.time()
duration = end_time - start_time

cap.release()
cv2.destroyAllWindows()
out.release()

"""
with open('buffalo_l_skipAlternate.txt','a') as wf:
	ws = str(duration)+'\n'
	wf.write(ws)
"""


