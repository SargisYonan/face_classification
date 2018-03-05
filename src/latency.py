import image_emotion_gender_demo as classify
import os

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-n", "--inputsize", dest="n",
help="Number of photos to classify", default=1)

(options, args) = parser.parse_args()
n = int(options.n)


dir = os.path.dirname(__file__)
images_path = os.path.join(dir, '../runthrough/blumie.jpg')

# hard coded for ~1T instructions
for i in range(0,n):
	clss = classify.run_classify(images_path)

