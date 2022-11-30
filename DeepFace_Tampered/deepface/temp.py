from deepface import DeepFace
from PIL import Image
import numpy as np


subject = np.asarray(Image.open('face.jpg'))
result = DeepFace.verify(img1_Frame = subject, img2_Frame = subject, enforce_detection = False)
print(result['distance'])
