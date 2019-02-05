from random import randint

offices = [

]

class Office:

    def __init__(self, office_name, office_type):
        self.id = randint(1, 100)
        self.type = office_type
        self.name = office_name

    def createOffice(self):
        try:
            dict_info = { "id": self.id, "type": self.type, "name": self.name }
            offices.append(dict_info)
            return dict_info
        except Exception:
            return None
    
    @staticmethod
    def getAllOffices():
        return offices

    @staticmethod
    def getOffice(officeID):
        for office in offices:
            if office["id"] == officeID:
                return office
        return None 

    
    


