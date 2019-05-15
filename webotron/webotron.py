import boto3
import click
from botocore.exceptions import ClientError

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


if __name__=='__main__':
    cli()
