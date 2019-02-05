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
