import boto3
import click
from botocore.exceptions import ClientError
from pathlib import Path
import mimetypes
from bucket import BucketManager
from domain import DomainManager

session=boto3.Session(profile_name='pythonAutomation')
bucket_manager=BucketManager(session)   #object of class
domain_manager=DomainManager(session)

@click.group()
def cli():
    "Webotron deploys websites to AWS"
    pass

@cli.command('list-buckets')
def list_buckets():
    "list all s3 buckets"
    for i in bucket_manager.list_all_buckets():
        print(i)

@cli.command('list-bucket-objects')
@click.argument('bucket_name')
def list_bucket_object(bucket_name):
    "list objects in the bucket"
    for i in bucket_manager.list_all_objects(bucket_name):
        print(i)

@cli.command('setup-bucket')
@click.argument('bucket')
def set_up_bucket(bucket):
    "Create and configure S3 bucket"
    s3_bucket=bucket_manager.init_bucket(bucket)
    bucket_manager.defn_policy(s3_bucket)
    bucket_manager.enable_website(s3_bucket)
    print(bucket_manager.get_url(s3_bucket))


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket_name')
def sync(pathname,bucket_name):
    "sync contents of pathname to bucket"
    bucket_manager.sync(pathname,bucket_name)

@cli.command('setup-domain')
@click.argument('domain-name')
@click.argument('bucket-name')
def setup_domain(domain_name,bucket_name):
    """configure domain to point to bucket"""
    zone=domain_manager.find_hosted_zone(domain_name) or domain_manager.create_hostedzone(domain_name)
    print(zone)


if __name__=='__main__':
    cli()
