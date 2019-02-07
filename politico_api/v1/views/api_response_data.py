
mandatory_fields = {

    "create_office": {
        "office_type": str,
        "office_name": str
    },

    "create_party": {
        "party_name": str, 
        "party_hq_address": str, 
        "party_logo_url": str, 
        "party_motto": str, 
        "party_members": int
    }

}

error_dictionary = {

    "create_office": {
        "MANDATORY_FIELD": "Field '{}' is mandatory in the requested body",
        "WRONG_DATA_TYPE": "Field '{}' has to be a '{}'",
        "UNABLE_TO_ADD_OFFICE": "unable to add office"
    },

    "get_single_office": {
        "OFFICEID_MUST_BE_REAL_NUMBER": "you must enter a real number at officeID in '/offices/<officeID>'",
        "OFFICEID_CANNOT_BE_ZERO_OR_NEGATIVE": "officeID cannot be zero or a negative number",
        "COULD_NOT_FIND_OFFICE": "Could not find office with id {}",
    },

    "edit_party": {
        "ID_HAS_TO_BE_NUMBER": "partyID has to be a number",
        "ID_HAS_TO_BE_MORE_THAN_ZERO": "partyID has to be more than 0",
        "NAME_CANNOT_CONTAIN_SPECIAL_CHARACTERS": "partyName cannot contain special characters like @ or $",
        "CANNOT_FIND_PARTY": "cannot find party with ID {}"
    },
    "delete_party": {
        "ID_HAS_TO_BE_NUMBER": "partyID has to be a number",
        "UNABLE_TO_FIND_PARTY": "unable to delete party with ID {}",
        "ID_HAS_TO_BE_POSITIVE": "partyID cannot be 0 or a negative number"
    }
    
}