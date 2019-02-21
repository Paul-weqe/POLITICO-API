import json

# converts bytes responses to dictionaries. Meant for when the JSON response is received in bytes, it can be transformed to a dictionary
def bytes_to_dict(byte_input):
    dict_output = json.loads(byte_input.decode())
    return dict_output
