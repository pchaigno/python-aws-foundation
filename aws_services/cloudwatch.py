try:
    import boto3
    # import botocore
except ImportError as e:
    print("This script require Boto3 to be installed and configured.")
    quit()


class CloudWatchService:

    def __init__(self):
        self.CWClient = boto3.client("logs")
        self.logGroupName = None

    def getMetricFilters(self, groupName):
        return self.CWClient.describe_metric_filters(logGroupName=groupName)
