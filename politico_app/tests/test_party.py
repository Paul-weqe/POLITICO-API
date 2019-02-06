# allow for import from the politico_app folder 
import sys
sys.path.insert(0,'../../..')

import json
from politico_app.config import app 

"""
THE FOLLOWING ARE TESTS FOR THE OFFICE BLUEPRINT FUNCTIONS
THE FUNCTIONS WILL BE NAMED USING THE CONVENTION: 
    "test_[method_used]_[blueprint_tested]_[functionality_being_tested]"
    e.g 
    test_patch_party_partyID_is_negative
    has method_used                 - get
    blueprint_tested                - office
    functionality_being_tested      - when the officeID is negative
"""


# set up the application for testing 
client = app.test_client()

# test that partyID is not negative in '/parties/<partyID>/<partyName>' PATCH method 
# this request should return a 404 error
def test_patch_party_partyid_is_negative():

    response = client.patch("/parties/-1/newPartyName")
    assert(response.status_code == 404)
    assert(b"partyID has to be more than 0" in response.data)


# testing for when the partyID is 0 in '/parties/<partyID>/<partyName>' PATCH method
# should return a 404 error
def test_patch_party_partyid_is_zero():
    response = client.patch("/parties/0/newPartyName")
    assert(response.status_code == 404)
    assert(b"partyID has to be more than 0" in response.data)


# testing for when partyID is not a number in '/parties/<partyID>/<partyName>' PATCH method
# should return a 404 error
def test_patch_party_partyid_is_number():

    response = client.patch("/parties/not_number/newPartyName")
    assert(response.status_code == 404)
    assert(b"partyID has to be a number" in response.data)

# testing for when partyName in '/parties/<partyID>/<partyName>' contains special characters 
# special characters such as '@' and '$'
def test_patch_party_partyname_is_special():
    
    response = client.patch("/parties/1/special@character")
    assert(response.status_code == 404)
    assert(b"partyName cannot contain special characters like @ or $" in response.data)

# testing for when a party whose ID does not exist is input
def test_patch_party_partyid_does_not_exist():
    response = client.patch("/parties/40000/newPartyName")
    assert(response.status_code == 404)
    assert(b"cannot find party with ID 4000" in response.data)


