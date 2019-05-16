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


    def create_cf_domain_record(self, zone, domain_name, cf_domain):
        """Create a domain record in zone for domain_name."""
        return self.client.change_resource_record_sets(
            HostedZoneId=zone['Id'],
            ChangeBatch={
                'Comment': 'Created by webotron',
                'Changes': [{
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': domain_name,
                            'Type': 'A',
                            'AliasTarget': {
                                'HostedZoneId': 'Z2FDTNDATAQYW2',
                                'DNSName': cf_domain,
                                'EvaluateTargetHealth': False
                            }
                        }
                    }
                ]
            }
        )
