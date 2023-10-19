# Modules
from modules.sg_resources import *

# Global variables #

# PLEASE INPUT YOUR NAME HERE AS A STRING #
TRAINEE_NAME = "<name>"

REGION = "eu-west-1"
KEY_TAG = "Name"
COHORT_IDENTIFIER = "CH10"
DEFAULT_VPC = "<vpc_id>"

sg = SecurityGroup(region=REGION, trainee_name=TRAINEE_NAME, cohort_identifier=COHORT_IDENTIFIER)


def test_sg_resource_has_all_three_expected_protocols():
    assert sg.allows_http
    assert sg.allows_https
    assert sg.allows_ssh