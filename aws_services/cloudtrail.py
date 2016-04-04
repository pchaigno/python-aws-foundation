try:
    import boto3
    # import botocore
except ImportError as e:
    print("This script require Boto3 to be installed and configured.")
    quit()


class CloudTrailService:

    def __init__(self):
        self.CTClient = boto3.client("cloudtrail")
        self.trailsReport = self.getTrailsReport()

    def getTrailsReport(self):
        trailsReport = self.CTClient.describe_trails()
        return trailsReport["trailList"]

    def getTrailStatus(self, name):
        return self.CTClient.get_trail_status(Name=name)

    def getLogGroupArn(self):
        pass
        # for trail in self.trailsReport:
