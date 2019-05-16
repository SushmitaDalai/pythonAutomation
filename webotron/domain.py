import uuid

class DomainManager():

    def __init__(self,session):
        """Creating a session"""
        self.session=session
        self.client=self.session.client('route53')

    def find_hosted_zone(self,domain):
        paginator=self.client.get_paginator('list_hosted_zones')
        for page in paginator.paginate():
            for zone in page['HostedZones']:
                if domain.endswith(zone['Name'][:-1]):
                    return zone
        return None

    def create_hostedzone(self,domain):
        zone='.'.join(domain.split('.')[-2:])+'.'
        return self.client.create_hosted_zone(Name=zone,CallerReference=str(uuid.uuid4()))
