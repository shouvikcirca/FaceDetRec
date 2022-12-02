from PIL import Image
import os

class txtParser:
	def __init__(self, filePath):
		self.filePath = filePath
		self.di = {
			'matching':0,
			'nonMatching':0
		}
		self.new_s = []
		self.extractData()


	def extractData(self):
		s = ''
		with open(self.filePath,'r') as f:
			s = f.read()
			s = s.split('\n')

		s = s[1:-1]

		for j in range(len(s)):
			self.new_s.append(s[j].split('\t'))

		for i in range(len(self.new_s)):
			if len(self.new_s[i]) == 3:
				self.di['matching']+=1
			elif len(self.new_s[i]) == 4:
				self.di['nonMatching']+=1

	def returnCounts(self):
		return self.di

	def getExtractedData(self):
		return self.new_s


def getImagePaths(pathList):	
	imgPaths = []
	if len(pathList) == 3:
		imgPaths.append('Data/{0}/{0}_{1}.jpg'.format(pathList[0], ''.join([str(0)]*(4 - len(pathList[1]))) + pathList[1] ))
		imgPaths.append('Data/{0}/{0}_{1}.jpg'.format(pathList[0], ''.join([str(0)]*(4 - len(pathList[2]))) + pathList[2] ))
	else:
		imgPaths.append('Data/{0}/{0}_{1}.jpg'.format(pathList[0], ''.join([str(0)]*(4 - len(pathList[1]))) + pathList[1] ))
		imgPaths.append('Data/{0}/{0}_{1}.jpg'.format(pathList[2], ''.join([str(0)]*(4 - len(pathList[3]))) + pathList[3] ))

	return imgPaths


if __name__ == "__main__":
	obj = txtParser('pairsDevTest.txt')
	#print(obj.returnCounts())
	parsedData = obj.getExtractedData()

	counter_matching = counter_nonMatching = 0

	isExists = os.path.exists('./matching')
	if not isExists:
		os.mkdir('matching')
	isExists = os.path.exists('./nonMatching')
	if not isExists:
		os.mkdir('nonMatching')



	for entry in parsedData:
		if len(entry) == 3:
			counter_matching+=1
			os.mkdir('matching/{}'.format(counter_matching))
			print('----')
			imgGot = getImagePaths(entry)
			img = Image.open(imgGot[0])
			img.save('matching/{}/{}'.format(counter_matching, imgGot[0].split('/')[-1]))
			print('matching/{}/{}'.format(counter_matching, imgGot[0].split('/')[-1]))
			img = Image.open(imgGot[1])
			img.save('matching/{}/{}'.format(counter_matching, imgGot[1].split('/')[-1]))
			print('matching/{}/{}'.format(counter_matching, imgGot[1].split('/')[-1]))
			print('----')
		else:
			counter_nonMatching+=1
			os.mkdir('nonMatching/{}'.format(counter_nonMatching))
			print('----')
			imgGot = getImagePaths(entry)
			img = Image.open(imgGot[0])
			img.save('nonMatching/{}/{}'.format(counter_nonMatching, imgGot[0].split('/')[-1]))
			print('nonMatching/{}/{}'.format(counter_nonMatching, imgGot[0].split('/')[-1]))
			img = Image.open(imgGot[1])
			img.save('nonMatching/{}/{}'.format(counter_nonMatching, imgGot[1].split('/')[-1]))
			print('nonMatching/{}/{}'.format(counter_nonMatching, imgGot[1].split('/')[-1]))
			print('----')



