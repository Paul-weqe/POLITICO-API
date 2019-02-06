# allow for import from the politico_app folder 
import sys
sys.path.insert(0,'../..')

import json
from politico_app.config import app 

# set up the application for testing
client = app.test_client()

"""
THE FOLLOWING ARE TESTS FOR THE OFFICE BLUEPRINT FUNCTIONS
THE FUNCTIONS WILL BE NAMED USING THE CONVENTION: 
    "test_[method_used]_[blueprint_tested]_[functionality_being_tested]"
    e.g 
    test_get_offices_officeID_is_negative
    has method_used                 - get
    blueprint_tested                - office
    functionality_being_tested      - when the officeID is negative
"""


# test for if the officeID in the GET request for '/offices/<officeID>' is negative
# should return a 404 error whenever the officeID is negative. 
def test_get_offices_officeID_is_negative():
    response = client.get("/offices/-1")
    assert(response.status_code == 404)
    response = client.get("/offices/0")
    assert(response.status_code == 404)


# test for if the officeID in GET request for  '/office/officeID' is a real number
# should return a 404 error whenever the officeID is not a real number
def test_get_offices_officeID_is_real():
    response = client.get("/offices/-j")
    assert(response.status_code == 404)
    data = json.loads(response.data.decode())
    assert(data["error"] == "you must enter a real number at officeID in '/offices/<officeID>'")
    

# testing for when in the POST method of '/offices' route, the office_type in the JSON is not a string
# this should return a 404 error
def test_post_offices_office_type_not_string():
    # sending wrong type for office_type
    response = client.post("/offices", data=json.dumps(dict(
         office_type = 2, office_name = "Prime minister"
    )), content_type="application/json")
    assert(response.status_code == 404)
    assert(b"Field 'office_type' has to be a '<class 'str'>'" in response.data)


# testing for when in the POST method of '/offices' the office_name in the JSON is not a String
# this should return a 404 error
def test_post_offices_office_name_not_string():
    # sending wrong type for office_name
    response = client.post("/offices", data=json.dumps(dict(
        office_type = "", office_name = 3
    )), content_type="application/json")
    assert(response.status_code == 404)
    assert(b"Field 'office_name' has to be a '<class 'str'>'" in response.data)


# tests the '/offices' POST method with all the correct data types in the JSON data
# in this case, 'office_type' is  a String and 'office_name' is also a String. Should return a 404 error
def test_post_offices_correct_office_name_and_office_type():
    response = client.post("/offices", data=json.dumps(dict(
        office_type = "school", office_name = "headboy"
    )), content_type="application/json")
    assert(response.status_code == 200)


# does not input the 'office_name' in the JSON being sent to the '/offices' POST method
# the 'office_name' is a required field and this should therefore return a 404 error
def test_post_offices_without_office_name():
    response = client.post("/offices", data=json.dumps(dict(
        office_type="legislative"           # no office_type
    )))
    assert(response.status_code == 404)
    assert(b"Field 'office_name' is mandatory in the request body" in response.data)


# does not input the 'office_type' in the JSON being sent to the '/offices' POST method
# the 'office_type' is a required field and this should therefore bring a 404 error
def test_post_offices_without_office_type():
    # testing the data without 'office_type' in the JSON fields
    response = client.post("/offices", data=json.dumps(dict(
        office_name="Prime minister"        # notice no office_type
    )))
    assert(response.status_code == 404)
    assert(b"Field 'office_type' is mandatory in the request body" in response.data)


# inputs all the required JSON fields for '/offices' with POST method. 
# the required fields are: 'office_type' and 'office_name'. This should be successful
def test_post_offices_with_all_required_fields():
    response = client.post("/offices", data=json.dumps(dict(
        office_type="legislative", office_name="Prime minister"
    )))
    assert(response.status_code == 200)

