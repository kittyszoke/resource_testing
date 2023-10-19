# Modules 
import boto3
import re


class Ec2Resources:
    def __init__(self, region):
        self.region = region
        self.ec2 = boto3.resource('ec2', self.region)

    @staticmethod
    def make_dict_from_list(l):
        """
        return a python dictionary when given a list of Key-Value dictionaries.

            We use this to parse the results given to us by the boto3 library (in
            turn from the AWS API) into something that's easier to manipulate in Python
        """
        result = {}
        for kv_pair in l:
            k = kv_pair['Key']
            v = kv_pair['Value']
            result[k] = v
        return result

    def get_cohort_tags(self, cohort_identifier):
        # Iterate through ec2 instances
        instance_iterator = self.ec2.instances.filter(Filters=[{'Name': 'tag-key', 'Values': ['Name']}])
        cohort_list = []
        for instance in instance_iterator:
            # Identify instances by tags - Key: Name
            tags = self.make_dict_from_list(instance.tags)
            name_tag = tags['Name']
            if re.search(cohort_identifier, name_tag):
                # append to list if correct credentials exist
                cohort_list.append(name_tag)

        return cohort_list