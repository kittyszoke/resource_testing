# Modules
from modules.keypair_resource import KeyPair

# Global variables # 
# PLEASE INPUT YOUR NAME HERE AS A STRING
TRAINEE_NAME = "<name>"

REGION = "eu-west-1"
COHORT_IDENTIFIER = "CH10.+"

keypair = KeyPair(region=REGION)


def test_find_key_pair():
    for name in keypair.find_key_pair(cohort_identifier=COHORT_IDENTIFIER):
        if TRAINEE_NAME.lower() in name.lower():
            assert True
            return
    assert False