#  Modules
import boto3
import re


class KeyPair:
    def __init__(self, region):
        self.ec2_client = boto3.client('ec2', region)
        self.key_pair = self.ec2_client.describe_key_pairs()

    def find_key_pair(self, cohort_identifier):
        data_key_finder = self.key_pair["KeyPairs"]
        key_list = []
        for key in data_key_finder:
            # Identify rsa keys
            if key["KeyType"] == "rsa":
                result = key["KeyPairId"], key["KeyFingerprint"], key["KeyName"]
                for rsa in result:
                    if re.search(cohort_identifier, rsa):
                        key_list.append(rsa)
        return key_list
