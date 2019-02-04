political_parties = [
    {
        "id": 1, "name": "Party 1", "hqAddress": "Nairobi", "logoUrl": "https://martialartsworldnews.com/wp-content/uploads/2015/11/1.jpg", "motto": "We are one", "members": 2000,
    },
    {
        "id": 2, "name": "Party 2", "hqAddress": "Mombasa", "logoUrl": "https://www.michels.ca/ckfinder/userfiles/images/number2tm.png", "motto": "we are two", "members": 2500,
    },
    {
        "id": 3, "name": "Party 3", "hqAddress": "Kisumu", "logoUrl", "https://vignette.wikia.nocookie.net/opartshunter/images/7/79/3.jpg/revision/latest?cb=20130603053056", "motto", "we are three", "members": 3000,
    }
]

users = [
    {
        "id": 1, "firstName": "Paul", "lastName": "Waswa", "otherName": "weqe", "email": "paul@paul.com", "isAdmin": False, "phoneNumber": "0701000302010", "passportUrl": "",
    },
    {
        "id": 2, "firstName": "Gideon", "lastName": "Smith", "otherName": "Salah", "email": "gidi@gidi.com", "isAdmin": False, "phoneNumber": "0710270374", "passportUrl": "",
    },
    {
        "id": 3, "firstName", "Peter", "lastName": "Kenyatta", "otherName": "lil", "email": "peter@peter.com", "isAdmin": True, "phoneNumber": "07374757282", "passportUrl": "",
    },
    {
        "id": 4, "firstName": "Brian", "lastName": "Kiasi", "otherName": "Ule msee", "email": "brian@brian.com", "isAdmin": True, "phoneNumber": "0712873873", "passportUrl": "",
    }
]

offices = [
    {
        "id": 1, "type": "local_government", "name": "chief",
    },
    {
        "id": 2, "type": "legislative", "name": "MP"
    },
    {
        "id": 3, "type": "state", "name": "president"
    },
    {
        "id": 4, "type": "federal", "name": "magistrate"
    }
]

candidates = [
    {
        "id": 1, "office": 2, "party": 1, "candidate": 1, 
    },
    {
        "id": 2, "office": 4, "party": 3, "candidate": 3
    },
    {
        "id": 3, "office": 1, "party": 2, "candidate": 2,
    }
]

votes = [
    {
        "id": 1, "candidateOn": 1, "createdBy": 1, "office": 1, "body": "",
    },
    {
        "id": 2, "candidateOn": 2, "createdBy": 2, "office": 2, "body": "",
    }
]