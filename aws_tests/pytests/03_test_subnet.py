# Modules # 
from modules.subnet_resource import Subnet

# Global variables #
# PLEASE INPUT YOUR NAME HERE AS A STRING
TRAINEE_NAME = "<name>"

REGION = "eu-west-1"
COHORT_IDENTIFIER = "CH10.+"
DEFAULT_VPC = "<vpc_id>"
subnet = Subnet(region=REGION)


def test_subnets_in_vpc():
    for name in subnet.subnets_in_vpc(vpc=DEFAULT_VPC, trainee_name=TRAINEE_NAME, cohort_identifier=COHORT_IDENTIFIER):
        if TRAINEE_NAME.lower() in name.lower():
            assert True
            return
    assert False