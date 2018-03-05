import image_emotion_gender_demo as classify
import os

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-d", "--divider", dest="div",
help="Select a divider - executes 1T/d", default=1)

(options, args) = parser.parse_args()
div = int(options.div)


dir = os.path.dirname(__file__)
images_path = os.path.join(dir, '../runthrough/blumie.jpg')

# hard coded for ~1T instructions
for i in range(0,int(2400/div)):
	clss = classify.run_classify(images_path)

