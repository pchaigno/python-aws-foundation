try:
    import boto3
    # import botocore
except ImportError as e:
    print("This script require Boto3 to be installed and configured.")
    quit()


class S3Service:

    def __init__(self):
        self.S3Client = boto3.client("s3")
        self.CTBucketName = None
        # self.S3BucketACL = None
        # self.S3BucketPolicy = None

    def getS3BucketAcl(self, bucket_name):
            return self.S3Client.get_bucket_acl(Bucket=bucket_name)

    def getS3BucketPolicy(self, bucket_name):
            return self.S3Client.get_bucket_policy(Bucket=bucket_name)
