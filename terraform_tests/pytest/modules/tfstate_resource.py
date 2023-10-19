import json
import os
import boto3

client = boto3.client('ec2')


# Read the terraform state file
def read_terraform_state():
    with open(os.path.join(os.path.dirname(__file__), "terraform.tfstate")) as f:
        state = json.load(f)
    return state


tfstate = read_terraform_state()