import sys
import time
import requests
import cv2
import operator
import numpy as np
import simplejson 
from pprint import pprint
from pylab import figure, axes, pie, title, show
	
# Import library to display results
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import os

fullpath=os.path.dirname(os.path.realpath(__file__))

# System Arguments
timestamp = sys.argv[1]
file_ext = sys.argv[2]


# Display images within Jupyter
_url = 'https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/RecognizeText'
_key = '6688df549cf447259aa777d268f653c0'
_maxNumRetries = 10

def processRequest( json, data, headers, params ):

	"""
	Helper function to process the request to Project Oxford

	Parameters:
	json: Used when processing images from its URL. See API Documentation
	data: Used when processing image read from disk. See API Documentation
	headers: Used to pass the key information and the data type request
	"""

	retries = 0
	result = None

	while True:
		response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )

		if response.status_code == 429:
			print( "Message: %s" % ( response.json() ) )
			if retries <= _maxNumRetries: 
				time.sleep(1) 
				retries += 1
				continue
			else: 
				print( 'Error: failed after retrying!' )
				break
		elif response.status_code == 202:
			result = response.headers['Operation-Location']
		else:
			print( "Error code: %d" % ( response.status_code ) )
			print( "Message: %s" % ( response.json() ) )
		break	

	return result

def getOCRTextResult( operationLocation, headers ):

	retries = 0
	result = None

	while True:
		response = requests.request('get', operationLocation, json=None, data=None, headers=headers, params=None)
		if response.status_code == 429:
			print("Message: %s" % (response.json()))
			if retries <= _maxNumRetries:
				time.sleep(1)
				retries += 1
				continue
			else:
				print('Error: failed after retrying!')
				break
		elif response.status_code == 200:
			result = response.json()
		else:
			print("Error code: %d" % (response.status_code))
			print("Message: %s" % (response.json()))
		break
	# bboxtext=[]
	# for i, x in enumerate(result['recognitionResult']['lines']):
	# 	bboxtext.append([x['boundingBox'], x['text']])

	
	with open(fullpath+'/uploads/'+timestamp+'/data.txt', 'w') as outfile:
		simplejson.dump(result, outfile, indent=4)
	return result

def showResultOnImage( result, img ):
	
	"""Display the obtained results onto the input image"""
	img = img[:, :, (2, 1, 0)]
	fig, ax = plt.subplots(figsize=(12, 12))
	ax.imshow(img, aspect='equal')

	lines = result['recognitionResult']['lines']

	for i in range(len(lines)):
		words = lines[i]['words']
		for j in range(len(words)):
			tl = (words[j]['boundingBox'][0], words[j]['boundingBox'][1])
			tr = (words[j]['boundingBox'][2], words[j]['boundingBox'][3])
			br = (words[j]['boundingBox'][4], words[j]['boundingBox'][5])
			bl = (words[j]['boundingBox'][6], words[j]['boundingBox'][7])
			text = words[j]['text']
			x = [tl[0], tr[0], tr[0], br[0], br[0], bl[0], bl[0], tl[0]]
			y = [tl[1], tr[1], tr[1], br[1], br[1], bl[1], bl[1], tl[1]]
			line = Line2D(x, y, linewidth=1, color='red')
			ax.add_line(line)
			# ax.text(tl[0], tl[1] - 2, '{:s}'.format(text),
			# bbox=dict(facecolor='blue', alpha=0.5),
			# fontsize=14, color='white')

	plt.axis('off')
	plt.tight_layout()
	plt.draw()
	# x123 - words
	plt.savefig(fullpath+'/uploads/'+timestamp+'/words_level_segmented.'+file_ext)
	#cv2.imwrite('image_cv.jpg',img)
	#plt.show()


# x123
pathToFileInDisk = fullpath+'/uploads/'+timestamp+'/preprocessed-resized.'+file_ext
with open(pathToFileInDisk, 'rb') as f:
	data = f.read()

# Computer Vision parameters
params = {'handwriting' : 'true'}

headers = dict()
headers['Ocp-Apim-Subscription-Key'] = _key
headers['Content-Type'] = 'application/octet-stream'

json = None

operationLocation = processRequest(json, data, headers, params)

result = None
if (operationLocation != None):
	headers = {}
	headers['Ocp-Apim-Subscription-Key'] = _key
	while True:
		time.sleep(1)
		result = getOCRTextResult(operationLocation, headers)
		if result['status'] == 'Succeeded' or result['status'] == 'Failed':
			break


# Load the original image, fetched from the URL
if result is not None and result['status'] == 'Succeeded':
	data8uint = np.fromstring(data, np.uint8)  # Convert string to an unsigned int array
	img = cv2.cvtColor(cv2.imdecode(data8uint, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)

	showResultOnImage(result, img)
