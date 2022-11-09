import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image
from PIL import Image
from deepface import DeepFace
import os
import cv2

app = FaceAnalysis(providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))
img = ins_get_image('facesImage')
faces = app.get(img)

for i in range(len(faces)):
            xmin, ymin, xmax, ymax = faces[i].bbox
            croppedIm = Image.fromarray(img).crop((xmin, ymin, xmax, ymax))
            croppedIm.save('{}_face.jpg'.format(i))



victorDistance = float('inf')
victorFace = ''
for i in range(len(faces)):
    imageName = '{}_face.jpg'.format(i)
    result = DeepFace.verify(img1_path = "facesImage4.jpg", img2_path = imageName, enforce_detection=False)
    print('{}: {}'.format(i, result['distance']))
    if result['distance'] < victorDistance:
        victorDistance = result['distance']
        victorFace = i



# To draw box on the face with the smallest cosine distance
victorFace = [faces[victorFace]]
rimg = app.draw_on(img, victorFace)
cv2.imwrite("./t1_output.jpg", rimg)




# Removing the generated clipped versions
for i in range(len(faces)):
    imageName = '{}_face.jpg'.format(i)
    os.remove(imageName)


videoTitle = ''
cap = cv2.VideoCapture(videoTitle)


if not cap.isOpened():
	cap = cv2.VideoCapture(0)
if not cap.isOpened():
	raise IOError("Cannot open video")



while True:
	ret, frame = cap.read()
	ClassIndex, confidence, bbox = 





