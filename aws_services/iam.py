try:
    import boto3
    import botocore
except ImportError as e:
    print("This script require Boto3 to be installed and configured.")
    quit()


class IAMService:

    def __init__(self):
        self.iam_client = boto3.client("iam")

    def get_credential_report(self):
        try:
            self.credential_report = self.iam_client.get_credential_report()
        except botocore.exceptions.ClientError:
            self.iam_client.generate_credential_report()
            self.credential_report = self.iam_client.get_credential_report()
        return self.credential_report
