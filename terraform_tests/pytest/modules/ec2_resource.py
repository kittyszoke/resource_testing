import boto3
from modules.tfstate_resource import tfstate

client = boto3.client('ec2')


# Read the arn and tag name from the instance resource
def read_instance_data():
    for data in tfstate.get("resources"):
        if data.get('type') == 'aws_instance':
            instance_id = data.get('instances')[0].get('attributes').get('id')
            # print(instance_id)
            instance_name = data.get('instances')[0].get('attributes').get('tags').get('Name')
            # print(instance_name)
    return instance_name, instance_id