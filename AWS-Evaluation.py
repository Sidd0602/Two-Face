import json
import boto3

def lambda_handler(event, context):
    client = boto3.client("rekognition")
    s3 = boto3.client("s3")
    responseDict = {}
    s3_2 = boto3.resource('s3')
    my_bucket = s3_2.Bucket('') # insert the bucket name here 
    
    for my_bucket_object in my_bucket.objects.filter(Prefix = ""): # replace with folder name that contains images to be tested
        if ("jpg" in str(my_bucket_object.key)): # testing for jpg images
            image_name = str(my_bucket_object.key)
            response = client.detect_faces(Image = {"S3Object" : {"Bucket" : "", "Name" : image_name }}, Attributes=['ALL']) # emter bucket name where images are kept
            responseDict[image_name] = response
    

    fileName = "" # name of filw where output will be stored
    lambdaPath = "/tmp/" + fileName # storing to tmp folder
    s3Path = "output/" + fileName # output file will be stored in this folder 
    s3_1 = boto3.resource("s3")
    s3_1.Bucket("").put_object(Key=s3Path, Body=json.dumps(responseDict)) # this will put the output file in the bucket name specified
