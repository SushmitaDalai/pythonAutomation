import boto3
import click
from botocore.exceptions import ClientError
from pathlib import Path
import mimetypes

session=boto3.Session(profile_name='pythonAutomation')
s3=session.resource('s3')

@click.group()
def cli():
    "Webotron deploys websites to AWS"
    pass

@cli.command('list-buckets')
def list_buckets():
    "list all s3 buckets"
    for i in s3.buckets.all():
        print(i)

@cli.command('list-bucket-objects')
@click.argument('bucket_name')
def list_bucket_object(bucket_name):
    "list objects in the bucket"
    for i in s3.Bucket(bucket_name).objects.all():
        print(i)
@cli.command('setup-bucket')
@click.argument('bucket')
def set_up_bucket(bucket):
    "Create and configure S3 bucket"
    try:
        new_bucket=s3.create_bucket(Bucket='bucket',CreateBucketConfiguration={'LocationConstraint':session.region_name})
    except ClientError as e:
        if e.response['Error']['Code']=='BucketAlreadyExists':
            new_bucket=s3.Bucket(bucket)
        else:
            raise e

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
             }
             """%new_bucket.name
    pol=new_bucket.Policy()
    pol.put(Policy=policy)
    ws=new_bucket.Website()
    ws.put(WebsiteConfiguration={'IndexDocument':{'Suffix':'index.html'}})
    return

@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket_name')
def sync(pathname,bucket_name):
    "sync contents of pathname to bucket"
    s3_bucket=s3.Bucket(bucket_name)
    root=Path(pathname).expanduser().resolve()
    def handle_dir(target):
        for p in target.iterdir():
            if p.is_dir():
                handle_dir(p)
            if p.is_file():
                upload_file(s3_bucket,str(p),str(p.relative_to(root)))

    handle_dir(root)

def upload_file(bucket,path,key):
    content_type=mimetypes.guess_type(key)[0] or 'text/plain'
    bucket.upload_file(path,key,ExtraArgs={'ContentType':content_type})

if __name__=='__main__':
    cli()
