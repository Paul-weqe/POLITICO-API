from random import randint

parties = [

]

class Party:

    def __init__(self, party_name, hq_address, logo_url):
        self.id = randint(1, 100)
        self.party_name = party_name
        self.hq_address = hq_address
        self.logo_url = logo_url

    def createParty(self):
        dict_info = {
            "id": self.id, "name": self.party_name, "hqAddress": self.hq_address, "logoUrl": self.logo_url
        }
        parties.append(dict_info)
        return dict_info

    @staticmethod
    def getAllParties():
        return parties
    
    @staticmethod
    def getSingleParty(partyID):
        for party in parties:
            if party["id"] == partyID:
                return party
        return False

    @staticmethod
    def editParty(partyID, partyName):
        for party in parties:
            if party["id"] == int(partyID):
                party["name"] = partyName
                return party
        return False
    
    @staticmethod
    def deleteParty(partyID):
        for party in parties:
            if party["id"] == partyID:
                parties.remove(party)
                return True
        return False

parties += [
    {
        "id": 1, "name": "Party 1", "hqAddress": "Nairobi", "logoUrl": "https://martialartsworldnews.com/wp-content/uploads/2015/11/1.jpg", "motto": "We are one", "members": 2000,
    },
    {
        "id": 2, "name": "Party 2", "hqAddress": "Mombasa", "logoUrl": "https://www.michels.ca/ckfinder/userfiles/images/number2tm.png", "motto": "we are two", "members": 2500,
    },
    {
        "id": 3, "name": "Party 3", "hqAddress": "Kisumu", "logoUrl": "https://vignette.wikia.nocookie.net/opartshunter/images/7/79/3.jpg/revision/latest?cb=20130603053056", "motto": "we are three", "members": 3000,
    }
]