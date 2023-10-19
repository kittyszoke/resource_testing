import boto3
from modules.tfstate_resource import tfstate

client = boto3.client('ec2')


# Read the arn and tag name from the subnet resource
def read_sub_data():
    for data in tfstate.get("resources"):
        if data.get('type') == 'aws_subnet':
            subnet_id = data.get('instances')[0].get('attributes').get('id')
            # print(arn_subnet)
            subnet_name = data.get('instances')[0].get('attributes').get('tags').get('Name')
            # print(name_subnet)
    return subnet_name, subnet_id