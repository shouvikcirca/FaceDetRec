import os
from PIL import Image

imageNames = os.listdir('Data')


def getImagePairData(path = 'pairs_CPLFW.txt'):
	imagePairData = []
	with open(path) as s:
		imagePairData = s.read().split('\n')
	imagePairData = imagePairData[:-1]
	return imagePairData

imagePairData = getImagePairData()

pair_1 = [imagePairData[i].split(' ')[0] for i in range(len(imagePairData)) if i%2 == 0]
pair_2 = [imagePairData[i].split(' ')[0] for i in range(len(imagePairData)) if i%2 == 1]


isExists = os.path.exists('./matching')
if not isExists:
	os.mkdir('matching')

isExists = os.path.exists('./nonMatching')
if not isExists:
	os.mkdir('nonMatching')

counter_matching = counter_nonMatching = 0

for i in range(len(imagePairData)//2):
	entry_1 = pair_1[i]
	entry_2 = pair_2[i]
	if ''.join(entry_1.split('_')[:-1]) == ''.join(entry_2.split('_')[:-1]):
		counter_matching+=1
		os.mkdir('matching/{}'.format(counter_matching))
		print('----')
		img = Image.open('Data/{}'.format(entry_1))
		img.save('matching/{}/{}'.format(counter_matching, entry_1))
		print('matching/{}/{}'.format(counter_matching, entry_1))
		img = Image.open('Data/{}'.format(entry_2))
		img.save('matching/{}/{}'.format(counter_matching, entry_2))
		print('matching/{}/{}'.format(counter_matching, entry_2))
		print('----')

	elif ''.join(entry_1.split('_')[:-1]) != ''.join(entry_2.split('_')[:-1]):
		counter_nonMatching+=1
		os.mkdir('nonMatching/{}'.format(counter_nonMatching))
		print('----')
		img = Image.open('Data/{}'.format(entry_1))
		img.save('nonMatching/{}/{}'.format(counter_nonMatching, entry_1))
		print('nonMatching/{}/{}'.format(counter_nonMatching, entry_1))
		img = Image.open('Data/{}'.format(entry_2))
		img.save('nonMatching/{}/{}'.format(counter_nonMatching, entry_2))
		print('nonMatching/{}/{}'.format(counter_nonMatching, entry_2))
		print('----')


# Max pose variations for any given entity is 3
"""
largestCardinality = 0
for key in uniqueNames:
	largestCardinality = max(largestCardinality, uniqueNames[key])

print(largestCardinality)
"""

