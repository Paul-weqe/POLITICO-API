from random import randint

class GeneralModelMethods():
    """
    Contains static methods that may need to be used in various models such as office and party. 
    Is meant to avoid repetition 
    """

    # looks through the list_to_search
    # if it finds an item with id_number, it returns the item. If not, it returns None
    @staticmethod
    def find_item(dict_to_search, id_number):

        if id_number in dict_to_search:
            return dict_to_search[id_number]
        return None

    # method used to find if a particular ID can be used for a new element. 
    # returns True if the ID can ba used and false if the ID has already been taken
    @staticmethod
    def can_use_id(dict_to_search, id_number):
        if GeneralModelMethods.find_item(dict_to_search, id_number) == None:
            return True
        return False

    # returns an item with a particular id in a list of dictionary 
    # looks through the dict_to_search and returns only the particular element with the id_number
    @staticmethod
    def get_single_item(dict_to_search, id_number):
        return GeneralModelMethods.find_item(dict_to_search, id_number)

    # enables one to edit a particular item in a dictionary
    # looks through the dictionary for item with id_number then changes the item_to_change to new_value
    @staticmethod
    def edit_single_item(dict_to_search, id_number, item_to_change, new_value):

        if id_number in dict_to_search:
            dict_to_search[id_number][item_to_change] = new_value
            return dict_to_search[id_number]
        return False
    
    # deletes one particular item
    # looks through the list for an element with an id_number and deletes it
    @staticmethod
    def delete_single_item(dict_to_search, id_number):
        item = GeneralModelMethods.find_item(dict_to_search, id_number)
        if item != None:
            del dict_to_search[id_number]
            return True
        return False
    
    
    # creates a new item
    # adds the item to the list in reference
    @staticmethod
    def create_item(dict_to_append, item_details):
        try:
            id = randint(1, 1000)
            while GeneralModelMethods.can_use_id(dict_to_append, id) == False:
                id = randint(1, 1000)
                
            dict_to_append[id] = item_details
            print("####")
            print(item_details)
            item_details["id"] = id
            return item_details
            
        except Exception as e:
            print(e)
            return None

    

