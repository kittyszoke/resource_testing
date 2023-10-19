# Modules # 
from modules.ec2_resources import Ec2Resources

# Global variables # 
# PLEASE INPUT YOUR NAME HERE AS A STRING
TRAINEE_NAME = "<name>"

REGION = "eu-west-1"
COHORT_IDENTIFIER = "CH10.+"
ec2 = Ec2Resources(region=REGION)


# Test #
def test_get_cohort_tags():
    for name in ec2.get_cohort_tags(cohort_identifier=COHORT_IDENTIFIER):
        if TRAINEE_NAME.lower() in name.lower():
            assert True
            return
    assert False