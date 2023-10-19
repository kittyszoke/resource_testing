# 1 -Find ALL Security groups
#   a. We need to grab the Group name alongside the IP address
# 2 -Make a new of security groups that match the names we care about
# 3 - Describe the security groups from step 2
# 4 - Loop over each security group and assert that inbound/outbound is 80
# If assertion fails, print the security group name

import boto3
import re


class SecurityGroup:
    def __init__(self, region, trainee_name, cohort_identifier):
        self.trainee_name = trainee_name
        self.cohort_identifier = cohort_identifier
        # boto3 initialisation
        self.ec2_client = boto3.client('ec2', region)
        self.owner_id = boto3.client('sts').get_caller_identity().get('Account')

        # Filters SGs and Users
        self.security_groups = self.ec2_client.describe_security_groups()['SecurityGroups']
        self.sg_for_user = self.get_sg_for_user()

        # Finding OwnerID, GroupName, IpPermissions
        self.sg_owner_id = ([{"name": f_group['OwnerId']} for f_group in self.security_groups])
        self.sg_names = ([{"name": f_group['GroupName']} for f_group in self.security_groups])
        self.sg_ports = ([{"name": f_group['IpPermissions']} for f_group in self.security_groups])

        self.allows_ssh = False
        self.allows_http = False
        self.allows_https = False

        self.sg_rule_user()

    def find_users_sg(self, sg):
        search_pattern = f'{self.cohort_identifier}_{self.trainee_name}(SG)?'
        if re.search(search_pattern, sg['GroupName']):
            return True

    def get_sg_for_user(self):
        return list(filter(lambda sg: self.find_users_sg(sg), self.security_groups))

    def sg_rule_user(self):
        # checking if SG list for trainee is empty or not
        if len(self.sg_for_user) == 0:
            print("User's security group not found")
            return
        elif len(self.sg_for_user) > 1:
            print("More than one security group found for user")
        for rule in self.sg_for_user[0]['IpPermissions']:
            # Don't be tempted to refactor this into the elif construct else we
            # won't detect the case when there is one rule which allows all three
            # services
            if rule['FromPort'] <= 80 and rule['ToPort'] >= 80:
                self.allows_http = True
            if rule['FromPort'] <= 22 and rule['ToPort'] >= 22:
                self.allows_ssh = True
            if rule['FromPort'] <= 443 and rule['ToPort'] >= 443:
                self.allows_https = True

        if self.allows_http and self.allows_https and self.allows_ssh:
            print("All 3 expected protocols are allowed")
        else:
            print("Not all expected traffic is allowed")