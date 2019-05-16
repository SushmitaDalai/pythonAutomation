class CertificateManager():

    def __init__(self,session):
        """Creating a session"""
        self.session=session
        self.client=self.session.client('acm',region_name='us-east-1')


    def find_certificate(self,domain):
        paginator=self.client.get_paginator('list_certificates')
        for page in paginator.paginate(CertificateStatuses=['ISSUED']):
            for cert in page['CertificateSummaryList']:
                if self.cert_matches(cert['CertificateArn'],domain):
                    return cert
        return None


    def cert_matches(self,cert_arn,domain_name):
        cert_details= self.client.describe_certificate(CertificateArn=cert_arn)
        alt_name= cert_details['Certificate']['SubjectAlternativeNames']
        for name in alt_name:
            if name==domain_name:
                return True
            if name[0]=='*' and domain_name.endswith(name[1:]):
                return True
        return False
