import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image
from PIL import Image
from deepface import DeepFace
import os
import cv2

videoTitle = 'facedetrecvideo.mp4'
cap = cv2.VideoCapture(videoTitle)

if not cap.isOpened():
	cap = cv2.VideoCapture(0)
if not cap.isOpened():
	raise IOError("Cannot open video")

app = FaceAnalysis(providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))

while True:
	ret, frame = cap.read()
	faces = app.get(frame)
	victorDistance = float('inf')
	victorFace = ''
	for i in range(len(faces)):
		xmin, ymin, xmax, ymax = faces[i].bbox
		croppedIm = Image.fromarray(frame).crop((xmin, ymin, xmax, ymax))
		isExists = os.path.exists('face.jpg')
		if isExists:
			os.remove('face.jpg')
		croppedIm.save('face.jpg')
		result = DeepFace.verify(img1_path = "face.jpg", img2_path = 'facedetrecsubject.png', enforce_detection=False)
		cosineDistance = result['distance']
		if cosineDistance < victorDistance:
			victorDistance = cosineDistance
			victorFace = i
	xmin, ymin, xmax, ymax = faces[victorFace].bbox
	cv2.rectangle(frame,(int(xmin), int(ymin)),(int(xmax), int(ymax)),(255,0,0),2)
	cv2.imshow('',frame)

	if cv2.waitKey(2) & 0xFF == ord('q'):
		break


cap.release()
cv2.destroyAllWindows()


#ClassIndex, confidence, bbox = model.detect(frame, confThreshold=0.55)
#xmin, ymin, xmax, ymax = bbox
#croppedIm = Image.fromarray(frame).crop((xmin, ymin, xmax, ymax))
