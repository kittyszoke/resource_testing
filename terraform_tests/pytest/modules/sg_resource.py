import boto3
from modules.tfstate_resource import tfstate

client = boto3.client('ec2')


# Read the arn and tag name from the security group resource
def read_sg_data():
    for data in tfstate.get("resources"):
        if data.get('type') == 'aws_security_group':
            sg_id = data.get('instances')[0].get('attributes').get('id')
            # print(sg_id)
            sg_name = data.get('instances')[0].get('attributes').get('name')
            # print(sg_name)
    return sg_name, sg_id