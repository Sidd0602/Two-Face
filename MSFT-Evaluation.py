import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO

# To install this module, run:
# python -m pip install Pillow
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person

import pickle


# Add key
KEY = ""

# Add Azure endpoint
ENDPOINT = ""

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))


# files to store the output for successful and unsuccessful calls
fout = open('results.pkl', 'a+b')
ffailed = open('failed.csv', 'a+')

with open('Input.csv', encoding='utf-8') as fin:
    for line in fin.readlines()[1:]:
        dirname = '' # directory where images are stored
        filename = str(line[:-1])
        image_path = os.path.join(dirname, filename)

        print('Running for %s' % image_path)
        if not os.path.exists(image_path):
            ffailed.write("%s,%s,%s\n" % (dirname, filename, ' File does not exist'))
        else:
            test_image_array = glob.glob(image_path)
            image = open(test_image_array[0], 'r+b')
    
            time.sleep(4)
            try:
                # We use detection model 1 to get better performance.
                faces = face_client.face.detect_with_stream(image, return_face_attributes=['gender', 'age', 'smile'], return_face_landmarks=False, detection_model='detection_01')

                face = faces[0]
                pickle.dump((dirname, filename, face), fout) # result is stored in pickle file

            except:
                ffailed.write("%s,%s,%s\n" % (dirname, filename, sys.exc_info()[0]))

fout.close()
ffailed.close()
