from modules.sg_resource import read_sg_data
import boto3

client = boto3.client('ec2')


# Test the aws SECURITY GROUP NAME against the SECURITY GROUP NAME from the terraform state file.
def test_aws_sg_name():
    Myec2 = client.describe_security_groups()
    for sg_name in Myec2['SecurityGroups']:
        if sg_name.get('GroupName') == read_sg_data()[0]:
            aws_route_name = sg_name.get('GroupName')
    assert aws_route_name == read_sg_data()[0]


# # Test the aws SECURITY GROUP-ID against the SECURITY GROUP-ID from the terraform state file.
def test_aws_sg_id():
    Myec2 = client.describe_security_groups()
    for sg in Myec2['SecurityGroups']:
        if sg.get('GroupId') == read_sg_data()[1]:
            aws_sg_id = sg.get('GroupId')
    assert aws_sg_id == read_sg_data()[1]