import numpy as np
from deepface import DeepFace
import os
from sklearn import metrics

class ModelValidator:
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
		for pair in pair_dirs[:self.dataPaths[self.dataset]['size']]:
			fileBasePath = path + '/matching/' + pair
			files = os.listdir(fileBasePath)
			result = model.verify(img1_path = fileBasePath+'/'+files[0], img2_path = fileBasePath+'/'+files[1], enforce_detection=False)
			scores.append(result['distance'])	
		
		pair_dirs = os.listdir(path+'/nonMatching')
		print('Testing on non matching pairs')
		for pair in pair_dirs[:self.dataPaths[self.dataset]['size']]:
			fileBasePath = path + '/nonMatching/' + pair
			files = os.listdir(fileBasePath)
			result = model.verify(img1_path = fileBasePath+'/'+files[0], img2_path = fileBasePath+'/'+files[1], enforce_detection=False)
			scores.append(result['distance'])	
		
		self.scores = np.array(scores)

	def classifierModule(self):
		self.scoresOutputtingModule()
		
		#preds = np.array([1 if i >= self.threshold else 0 for i in self.scores])
		return self.scores

	def getAUC(self):
		size = self.dataPaths[self.dataset]['size']
		
		# 0 is for matching and 1 is for non-matching
		targets = np.array([0 for i in range(size)] + [1 for i in range(size)])
		
		preds = self.classifierModule()
		fpr, tpr, thresholds = metrics.roc_curve(targets, preds, pos_label=1)	

		"""
 		#Code to verify calculation of tpr, fpr
		for thresh in thresholds:
			ctpr = (targets[size:] == np.array([1 if i >= thresh else 0 for i in self.scores])[size:]).sum()/size
			cfpr = (targets[:size] != np.array([1 if i >= thresh else 0 for i in self.scores])[:size]).sum()/size
			print(ctpr, cfpr)
			
		print(tpr, fpr)	
		"""
		return metrics.auc(fpr, tpr)	
		

if __name__ == '__main__':
	obj = ModelValidator(threshold = 0.4, dataset = 'LFW', model = 'Facenet')
	preds = obj.getAUC()
	print(preds)
				




