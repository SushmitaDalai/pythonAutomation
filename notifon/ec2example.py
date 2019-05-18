import boto3
import os
import stat
import click
import time

session=boto3.Session(profile_name='pythonAutomation')
ec2=session.resource('ec2')

@click.group()
def cli():
    """Notifon creates EC2 Instances"""
    pass

@cli.command('create_key-pair')
@click.argument('keyname')
def create_key_pair(keyname):
    keypath=keyname+'.pem'
    key_pair=ec2.create_key_pair(KeyName=keyname)
    with open(keypath,'w') as f:
        f.write(key_pair.key_material)
    os.chmod(keypath, stat.S_IRUSR | stat.S_IWUSR)

@cli.command('create_ec2_instance')
@click.argument('keyname')
def create_ec2_instance(keyname):
    image_id='ami-0cb72367e98845d43'
    instances=ec2.create_instances(ImageId=image_id,MinCount=1,MaxCount=1,InstanceType='t2.micro',KeyName=keyname)
    instance=instances[0]
    instance.wait_until_running()
    instance.reload()
    print("instance id="+instance.id+", public ip address="+instance.public_ip_address+", public dns name="+instance.public_dns_name)





if __name__=='__main__':
    cli()
