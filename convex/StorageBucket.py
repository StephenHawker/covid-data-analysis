"""S3 functions"""
import logging
import urllib.parse as urlparse
import datetime
import boto3
import uuid
import json
from botocore.exceptions import ClientError

class StorageBucket:
    ############################################################
    # constructor
    ############################################################
    def __init__(self):

        self.name = "Storage Bucket"
        self.bucketname = self.create_bucket_name("sth")
        self.LOGGER = logging.getLogger(__name__)
        self.client = boto3.client('s3')
        self.session = boto3.session.Session()
        self.current_region = self.session.region_name
        self.logger = logging.getLogger(__name__)

        self.s3resource = boto3.resource('s3')
        self.bucket = self.s3resource.Bucket('name')

    ############################################################
    # str
    ############################################################
    def __str__(self):

        return repr("Storage Bucket")

    ############################################################
    # Create S3 bucket name (must be unique)
    ############################################################
    def create_bucket_name(self, bucket_prefix):
        # The generated bucket name must be between 3 and 63 chars long
        return ''.join([bucket_prefix, str(uuid.uuid4())])

    ############################################################
    # Create S3 bucket - region eu-west-2
    ############################################################
    def create_bucket(self):

        try:
            bucket_response = self.s3resource.create_bucket(Bucket=self.bucketname,
                                  CreateBucketConfiguration={
                                      'LocationConstraint': self.current_region})
            bucket_response.wait_until_exists()

            self.logger.info("Created bucket '%s' in region=%s", bucket_response.name,
                        self.s3resource.meta.client.meta.region_name)
            print(self.bucketname, self.current_region)

        except ClientError as error:

            self.logger.exception("Couldn't create bucket named '%s' in region=%s.",
                             self.bucketname, self.current_region)
            if error.response['Error']['Code'] == 'IllegalLocationConstraintException':
                self.logger.error("When the session Region is anything other than us-east-1, "
                             "you must specify a LocationConstraint that matches the "
                             "session Region. The current session Region is %s and the "
                             "LocationConstraint Region is %s.",
                             self.s3resources3.meta.client.meta.region_name, self.current_region)
            raise error
        else:
            return bucket_response

    ############################################################
    # create temp file
    ############################################################
    def create_temp_file(self, size, file_name, file_content):

        random_file_name = ''.join([str(uuid.uuid4().hex[:6]), file_name])
        with open(random_file_name, 'w') as f:
            f.write(str(file_content) * size)
        return random_file_name

    ############################################################
    # Retrieve the list of existing buckets
    ############################################################
    def list_buckets(self):

        response = self.client.list_buckets()

        # Output the bucket names
        print('Existing buckets:')
        for bucket in response['Buckets']:
            print(f'  {bucket["Name"]}')


    ############################################################
    # Check if a bucket exists
    ############################################################
    def bucket_exists(self, bucket_name):
        """
        Determine whether a bucket with the specified name exists.
        Usage is shown in usage_demo at the end of this module.
        :param bucket_name: The name of the bucket to check.
        :return: True when the bucket exists; otherwise, False.
        """
        try:
            self.s3resource.meta.client.head_bucket(Bucket=bucket_name)
            self.logger.info("Bucket %s exists.", bucket_name)
            exists = True
        except ClientError:
            self.logger.warning("Bucket %s doesn't exist or you don't have access to it.",
                           bucket_name)
            exists = False
        return exists

    ############################################################
    # Check if a bucket exists
    ############################################################
    def delete_bucket(self, bucket):
        """
        Delete a bucket. The bucket must be empty or an error is raised.
        Usage is shown in usage_demo at the end of this module.
        :param bucket: The bucket to delete.
        """
        try:
            bucket.delete()
            bucket.wait_until_not_exists()
            self.logger.info("Bucket %s successfully deleted.", bucket.name)
        except ClientError:
            self.logger.exception("Couldn't delete bucket %s.", bucket.name)
            raise

    ############################################################
    # Get ACL of bucket
    ############################################################
    def get_acl(self, bucket_name):
        """
        Get the ACL of the specified bucket.
        Usage is shown in usage_demo at the end of this module.
        :param bucket_name: The name of the bucket to retrieve.
        :return: The ACL of the bucket.
        """

        try:
            acl = self.s3resource.Bucket(bucket_name).Acl()
            self.logger.info("Got ACL for bucket %s owned by %s.",
                        bucket_name, acl.owner['DisplayName'])
        except ClientError:
            self.logger.exception("Couldn't get ACL for bucket %s.", bucket_name)
            raise
        else:
            return acl

    ############################################################
    # put policy on bucket
    ############################################################
    def put_policy(self, bucket_name, policy):
        """
        Apply a security policy to a bucket. Policies typically grant users the ability
        to perform specific actions, such as listing the objects in the bucket.
        Usage is shown in usage_demo at the end of this module.
        :param bucket_name: The name of the bucket to receive the policy.
        :param policy: The policy to apply to the bucket.
        """

        try:
            # The policy must be in JSON format.
            self.s3resource.Bucket(bucket_name).Policy().put(Policy=json.dumps(policy))
            self.logger.info("Put policy %s for bucket '%s'.", policy, bucket_name)
        except ClientError:
            self.logger.exception("Couldn't apply policy to bucket '%s'.", bucket_name)
            raise

    ############################################################
    # get policy on bucket
    ############################################################
    def get_policy(self, bucket_name):
        """
        Get the security policy of a bucket.
        Usage is shown in usage_demo at the end of this module.
        :param bucket_name: The bucket to retrieve.
        :return: The security policy of the specified bucket.
        """
        try:
            policy = self.s3resource.Bucket(bucket_name).Policy()
            self.logger.info("Got policy %s for bucket '%s'.", policy.policy, bucket_name)
        except ClientError:
            self.logger.exception("Couldn't get policy for bucket '%s'.", bucket_name)
            raise
        else:
            return json.loads(policy.policy)

    ############################################################
    # delete policy on bucket
    ############################################################
    def delete_policy(self, bucket_name):
        """
        Delete the security policy from the specified bucket.
        Usage is shown in usage_demo at the end of this module.
        :param bucket_name: The name of the bucket to update.
        """
        try:
            self.s3resource.Bucket(bucket_name).Policy().delete()
            self.logger.info("Deleted policy for bucket '%s'.", bucket_name)
        except ClientError:
            self.logger.exception("Couldn't delete policy for bucket '%s'.", bucket_name)
            raise
