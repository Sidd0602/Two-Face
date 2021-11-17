import pandas
from facepplib import FacePP
import time


facepp = FacePP(api_key='',api_secret='') # add api key and secret
opFile = open("", "w") # filename where the output will be written

df = pandas.read_csv('') # file containing names of all image files to be tested

numImages = df['filename'].size
counter = 0

for i in range (numImages):
    print(df['filename'][i])
    image = facepp.image.get(image_file=df['filename'][i], return_attributes=['gender','age','smiling','beauty']) # add attributes that are to be collected
    if(len(image.faces)) == 1: # if only one face is detected
        counter += 1
        opFile.write(str(df['filename'][i]) + ',' + '1' + ',' + str(image.faces[0].gender['value']) + ',' + str(image.faces[0].age['value']) + ',' + str(image.faces[0].smile['value']) + ',' + str(image.faces[0].beauty['male_score']) + ',' + str(image.faces[0].beauty['female_score']) + ',' + str(image.faces[0].face_rectangle['left']) + ',' + str(image.faces[0].face_rectangle['top']) + ',' + str(image.faces[0].face_rectangle['width']) + ',' + str(image.faces[0].face_rectangle['height']) + '\n')
        time.sleep(8)
    else: # if more than one face is detected
        print(len(image.faces))
        opFile.write(str(df['filename'][i]) + ',' + '0,,,,,,,,,\n')

print("done " + str(counter))
opFile.close()
