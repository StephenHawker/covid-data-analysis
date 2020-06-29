"""AWS IAM functions """
import logging
import json
import boto3

from botocore.exceptions import ClientError

class IAMAdmin:
    """
    Iam Admin functions
    """
    ############################################################
    # constructor
    ############################################################
    def __init__(self, region, path, profile_name):
        """
        Constructor
        :param region: The region to use
        :param path: Path to use
        :param profile_name: Profile to connect with
        """

        self.name = "IAM Admin"
        self.LOGGER = logging.getLogger(__name__)
        self.path = path
        self.region = region
        self.session = boto3.session.Session(profile_name=profile_name,
                                             region_name=region)
        self.client = boto3.client('iam')
        self.iamresource = boto3.resource('iam')

    ############################################################
    # str
    ############################################################
    def __str__(self):

        return repr("IAM Admin")

    ############################################################
    # create role
    ############################################################
    def create_role(self, role_name, role_description):
        """
        Get the security policy of a bucket.
        :param role_name: The role name to create
        :param role_description: Role description
        """
        try:
            iam = self.session.client('iam')
            role_name = role_name
            description = role_description

            trust_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "",
                        "Effect": "Allow",
                        "Principal": {
                            "Service": "ec2.amazonaws.com"
                        },
                        "Action": "sts:AssumeRole"
                    }
                ]
            }

            response = iam.create_role(
                Path='/' + self.path + '/',
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy),
                Description=description,
                MaxSessionDuration=3600
            )


            role_arn = response['Role']['Arn']

            self.LOGGER.debug(" Created IAM role: %s", role_arn)

        except ClientError as error:

            self.LOGGER.exception("Couldn't create role named '%s' in region=%s.",
                                  role_name, self.region)

            raise error
        else:
            return role_arn

    ############################################################
    # create Policy and attach to Role
    ############################################################
    def create_policy(self, policy_content, policy_name, role_name):
        """
        Get the policy and attach it to the role
        Usage is shown in usage_demo at the end of this module.
        :param policy_content : The json content of the policy
        :param policy_name: The name of the policy.
        :param role_name : The name of the Role to attach the policy to
        """
        try:
            iam = self.session.client('iam')

            response = iam.create_policy(
                PolicyName=policy_name,
                PolicyDocument=json.dumps(policy_content)
            )
            policy_arn = response['Policy']['Arn']

            iam.attach_role_policy(
                PolicyArn=policy_arn,
                RoleName=role_name
            )

            self.LOGGER.debug(" Created IAM policy: %s, arn: %s",
                        response,
                        policy_arn
                        )

        except ClientError as error:

            self.LOGGER.exception("Couldn't create policy named '%s' for role_name %s.",
                                  policy_name,
                                  role_name)
            self.LOGGER.exception("Error:  %s", repr(error))
            raise error
        else:
            return response

    ############################################################
    # delete role
    ############################################################
    def delete_role(self, role_name):
        """
        Delete IAM role
        :param role_name : The name of the Role to delete
        """
        try:
            iam = self.session.client('iam')

            role = self.iamresource.Role(name=role_name)

            # Get all Managed Policies and detatch them
            self.LOGGER.debug("Removing Managed Policies from %s", role.name)
            [role.detach_policy(PolicyArn=policy.arn)
             for policy in role.attached_policies.all()]

            # Get all Instance Profiles and detatch them
            self.LOGGER.debug("Removing role from InstanceProfiles")
            [profile.remove_role(RoleName=role.name)
             for profile in role.instance_profiles.all()]

            # Get all Inline Policies and delete them
            self.LOGGER.debug("Deleting Inline Policies")
            [role_policy.delete() for role_policy in role.policies.all()]

            role.delete()

            print("+ Deleted IAM Role: %s", role_name)

        except ClientError as error:

            self.LOGGER.exception("Couldn't delete role named '%s' ",
                                  role_name)
            self.LOGGER.exception("Error:  %s", repr(error))
            raise error
        else:
            return True


    ############################################################
    # create Instance Profile
    ############################################################
    def create_instance_profile(self, profile_name):
        """
        Create Instance Profile
        :param profile_name: The name of the instance profile
        :return profile_arn: The arn for the profile created
        """
        try:
            iam = self.session.client('iam')

            instance_profile = iam.create_instance_profile(
                InstanceProfileName=profile_name,
                Path='/' + self.path + '/'
            )

            profile_arn = instance_profile['InstanceProfile']['Arn']

            self.LOGGER.debug("Created IAM Instance profile: %s ", profile_arn)

        except ClientError as error:

            self.LOGGER.exception("Couldn't instance profile named '%s'.",
                                  profile_name)
            self.LOGGER.exception("Error:  %s", repr(error))
            #raise error
        else:
            return profile_arn


    ############################################################
    # Add Role to Instance Profile
    ############################################################
    def add_role_instance_profile(self, profile_name, profile_arn, role_name):
        """
        Add Role to instance profile
        :param profile_name: The name of the profile
        :param profile_arn: The arn of the profile
        :param role_name: The role name
        :retu
        """
        try:
            iam = self.session.client('iam')

            instance_role_profile = iam.add_role_to_instance_profile(
                InstanceProfileName=profile_name,
                RoleName=role_name
            )

            self.LOGGER(" Added Role to IAM Instance profile: %s ", profile_arn)

        except ClientError as error:

            self.LOGGER.exception("Couldn't Add role named '%s "
                                  " to instance profile: %s  in region=%s.",
                                  role_name,
                                  profile_name,
                                  self.region)
            self.LOGGER.exception("Response : %s", instance_role_profile)
            self.LOGGER.exception("Error:  %s", repr(error))
            raise error
        else:
            return profile_arn


    ############################################################
    # Get Instance Profile
    ############################################################
    def get_instance_profile(self, profile_name):
        """
        Get Instance Profile
        :param profile_name: The instance profile name
        :return profile_arn: The instance profile arn
        """
        try:

            instance_profile = self.iamresource.InstanceProfile(profile_name)

            profile_arn = instance_profile.arn

            self.LOGGER.debug(" Get IAM Instance profile: %s ", profile_arn)

        except ClientError as error:

            self.LOGGER.exception("Couldn't get instance profile named '%s' in region=%s.",
                                  profile_name,
                                  self.region)
            self.LOGGER.exception("Error:  %s", repr(error))

            #raise error
        else:
            return profile_arn
