try:
    import boto3
    import botocore
except ImportError as e:
    print("This script require Boto3 to be installed and configured.")
    quit()

import csv


class IAMService:

    def __init__(self):
        self.IAMClient = boto3.client("iam")
        self.credReport = self.getCredReport()
        self.passwordPolicy = self.getPasswordPolicy()

    def getCredReport(self):
        try:
            credReport = self.IAMClient.get_credential_report()
        except botocore.exceptions.ClientError:
            response = self.IAMClient.generate_credential_report()
            while response["State"] != "COMPLETE":
                response = self.IAMClient.generate_credential_report()
            credReport = self.IAMClient.get_credential_report()

        return self.parseCredReport(credReport["Content"])

    def parseCredReport(self, credReport):
        report = []
        for row in csv.reader(credReport.splitlines(), delimiter=","):
            report.append(row)
        return report

    def getPasswordPolicy(self):
        try:
            passwordPolicy = self.IAMClient.get_account_password_policy()
            return passwordPolicy["PasswordPolicy"]
        except botocore.exceptions.ClientError:
            return None
