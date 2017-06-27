#!/usr/bin/env python3

import boto3.session

class s3client:
    def __init__(self):
        session = boto3.session.Session()
        self.session = session.client('s3', config= boto3.session.Config(signature_version='s3v4'))

    def getbucketinfo(self, bucketname):
        bucket = self.session.list_objects(Bucket=bucketname)
        return bucket

    def putobject(self, obj, bucket, path):
        try:
            self.session.upload_file(obj, bucket, path)
        except Exception as err:
            print('error uploading file:', err)

    def moveobject(self, sourceobj, destobj):
        copysource = {
            'Bucket': sourceobj[0],
            'Key': sourceobj[1]
        }
        try:
            self.session.copy(copysource, destobj[0], destobj[1])
        except Exception as err:
            print(err)
        try:
            self.session.delete_object(Bucket=sourceobj[0], Key=sourceobj[1])
        except Exception as err:
            print(err)

