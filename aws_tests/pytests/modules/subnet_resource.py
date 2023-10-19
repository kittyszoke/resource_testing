# Modules

import boto3
from utilities import checks_lowercase_string


class Subnet:
    def __init__(self, region):
        self.ec2_client = boto3.client('ec2', region)
        self.subnet = self.ec2_client.describe_subnets(Filters=[{'Name': 'tag-key', 'Values': ['Name']}])

    def subnets_in_vpc(self, vpc, trainee_name, cohort_identifier):
        subnet_finder = self.subnet["Subnets"]
        identified_subnet_list = []
        # Allocating subnets by vpc - default vpc
        for vpc_subnet in subnet_finder:
            if vpc_subnet["VpcId"] == vpc:
                # Listing subnets by tags
                list_of_subnet = vpc_subnet["Tags"]
                # Find trainee's subnets by tags - trainee name and cohort
                for trainee_subnet in list_of_subnet:
                    result = trainee_subnet.get('Value')
                    # Checking trainee name and cohort - code removed extra regex code for cohort identifier
                    if checks_lowercase_string(result, trainee_name) and cohort_identifier.replace(".+", "") in result:
                        identified_subnet_list.append(result)
        return identified_subnet_list