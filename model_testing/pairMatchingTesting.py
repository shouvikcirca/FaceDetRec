import numpy as np
from deepface import DeepFace
import os

class DataValidator:
	def __init__(self, threshold, dataset='LFW', model = 'VGG-Face'):
		self.model = model
		self.dataset = dataset
		self.threshold = threshold
		self.dataPaths = {
			'LFW':{
				'path':'LFW',
				'size':500
			}
		}
		self.scores = []

	def modelLoadingModule(self):
		return DeepFace	
	
	def scoresOutputtingModule(self):
		path = self.dataPaths[self.dataset]['path']
		scores = []

		model = self.modelLoadingModule()
		
		pair_dirs = os.listdir(path+'/matching')
		print('Testing on Matching Pairs')
		for pair in pair_dirs:
			fileBasePath = path + '/matching/' + pair
			files = os.listdir(fileBasePath)
			result = model.verify(img1_path = fileBasePath+'/'+files[0], img2_path = fileBasePath+'/'+files[1], enforce_detection=False)
			scores.append(result['distance'])	
		
		pair_dirs = os.listdir(path+'/nonMatching')
		print('Testing on non matching pairs')
		for pair in pair_dirs:
			fileBasePath = path + '/nonMatching/' + pair
			files = os.listdir(fileBasePath)
			result = model.verify(img1_path = fileBasePath+'/'+files[0], img2_path = fileBasePath+'/'+files[1], enforce_detection=False)
			scores.append(result['distance'])	
		
		self.scores = np.array(scores)

	def classifierModule(self):
		size = self.dataPaths[self.dataset]['size']
		targets = np.array([1 for i in range(size)] + [0 for i in range(size)])
		
		self.scoresOutputtingModule()
		
		preds = np.array([1 if i < self.threshold else 0 for i in self.scores])
		return preds


	
	
		
		



if __name__ == '__main__':
	obj = DataValidator(threshold = 0.4, dataset = 'LFW', model = 'Facenet')
	preds = obj.classifierModule()
	print(preds)
				




