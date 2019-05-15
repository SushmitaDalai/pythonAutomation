import boto3
import mimetypes
from botocore.exceptions import ClientError
from pathlib import Path

class BucketManager:

    def __init__(self,session):
        """Creating a session"""
        self.session=session
        self.s3=self.session.resource('s3')

    def list_all_buckets(self):
        """list all buckets"""
        return self.s3.buckets.all()

    def list_all_objects(self,bucket):
        """list all objects of buckets"""
        return self.s3.Bucket(bucket).objects.all()

    def init_bucket(self,bucket):
        """initialises bucket"""
        try:
            new_bucket=self.s3.create_bucket(Bucket=bucket,CreateBucketConfiguration={'LocationConstraint':self.session.region_name})
        except ClientError as e:
            if e.response['Error']['Code']=='BucketAlreadyExists' or 'BucketAlreadyOwnedByYou':
                new_bucket=self.s3.Bucket(bucket)
            else:
                raise e

        return new_bucket

    def defn_policy(self,bucket):
        """sets policy"""
        policy="""{
            "Version":"2012-10-17",
            "Statement":[{
            "Sid":"PublicReadGetObject",
            "Effect":"Allow",
            "Principal": "*",
            "Action":["s3:GetObject"],
            "Resource":["arn:aws:s3:::%s/*"]
             }
             ]
             }"""%bucket.name

        pol=bucket.Policy()
        pol.put(Policy=policy)

    def enable_website(self,bucket):
        """enables static website hosting"""
        bucket.Website().put(WebsiteConfiguration={'IndexDocument':{'Suffix':'index.html'}})

    def upload_file(self,bucket,path,key):
        """uploads files to bucket"""
        content_type=mimetypes.guess_type(key)[0] or 'text/plain'
        bucket.upload_file(path,key,ExtraArgs={'ContentType':content_type})

    def sync(self,path,bucket):
        """sync path and bucket to upload files"""
        bucket=self.s3.Bucket(bucket)
        root=Path(path).expanduser().resolve()
        def handle_dir(target):
            for p in target.iterdir():
                if p.is_dir():
                    handle_dir(p)
                if p.is_file():
                    self.upload_file(bucket,str(p),str(p.relative_to(root)))

        handle_dir(root)
