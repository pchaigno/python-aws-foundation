try:
    import boto3
    # import botocore
except ImportError as e:
    print("This script require Boto3 to be installed and configured.")
    quit()


class EC2Service:

    def __init__(self):
        self.ec2_client = boto3.client("ec2")
        self.securityGroups = self.getSecurityGroups()

    def getSecurityGroups(self):
        securityGroups = self.ec2_client.describe_security_groups()
        return securityGroups["SecurityGroups"]

    def getSecurityGroupIDs(self):
        security_groups = self.getSecurityGroups()
        return [sg["GroupId"] for sg in security_groups["SecurityGroups"]]

    def getSecurityGroupIpPermissions(self, sg_id):
        return self.ec2_client.describe_security_groups(GroupIds=[sg_id])
