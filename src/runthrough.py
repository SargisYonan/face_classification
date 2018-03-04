import image_emotion_gender_demo as classify
import os

dir = os.path.dirname(__file__)
images_path = os.path.join(dir, '../runthrough/')

for filename in os.listdir(images_path):
    if filename.endswith(".jpg") or filename.endswith(".jpeg"): 
	clss = classify.run_classify(os.path.join(images_path, filename))
	print(filename.split('.')[0]  + ' is a ' + clss[1] + ' ' + clss[0] + '.')
	continue
    else:
        continue

