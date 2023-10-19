from modules.route_resource import read_route_data
import boto3

client = boto3.client('ec2')


# Test the aws ROUTE TAG NAME against the ROUTE TAG NAME from the terraform state file.
def test_aws_route_name():
    Myec2 = client.describe_route_tables()
    for route_table in Myec2['RouteTables']:
        for tag_route in route_table['Tags']:
            if tag_route.get('Value') == read_route_data()[0]:  # print(tag.get('Value'))
                aws_route_name = tag_route.get('Value')
    assert aws_route_name == read_route_data()[0]


# Test the aws ROUTE-ID against the ROUTE-ID from the terraform state file.
def test_aws_route_id():
    Myec2 = client.describe_route_tables()
    for route_table in Myec2['RouteTables']:
        if route_table.get('RouteTableId') == read_route_data()[1]:
            aws_route_id = route_table.get('RouteTableId')
    assert aws_route_id == read_route_data()[1]