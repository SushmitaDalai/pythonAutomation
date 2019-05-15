import boto3
import click

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


if __name__=='__main__':
    cli()
