from modules.subnet_resource import read_sub_data
import boto3

client = boto3.client('ec2')


# Test the aws SUBNET NAME against the the SUBNET NAME from the terraform state file.
def test_aws_subnet_name():
    Myec2 = client.describe_subnets()
    for subnet in Myec2['Subnets']:
        for tag in subnet['Tags']:
            if tag.get('Value') == read_sub_data()[0]:
                aws_instance_name = tag.get('Value')
    assert aws_instance_name == read_sub_data()[0]


# Test the aws SUBNET-ID against the the SUBNET-ID from the terraform state file.
def test_aws_subnet_id():
    Myec2 = client.describe_subnets()
    for subnet in Myec2['Subnets']:
        if subnet.get('SubnetId') == read_sub_data()[1]:
            aws_instance_id = subnet.get('SubnetId')
    assert aws_instance_id == read_sub_data()[1]