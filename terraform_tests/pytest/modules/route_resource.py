import boto3
from modules.tfstate_resource import tfstate

client = boto3.client('ec2')


# Read the arn and tag name from the route resource    
def read_route_data():
    for data in tfstate.get("resources"):
        if data.get('type') == 'aws_route_table':
            route_id = data.get('instances')[0].get('attributes').get('id')
            # print(route_id)
            route_name = data.get('instances')[0].get('attributes').get('tags').get('Name')
            # print(route_name)
    return route_name, route_id