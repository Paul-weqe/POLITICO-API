from random import randint

class GeneralModelMethods():
    """
    Contains static methods that may need to be used in various models such as office and party. 
    Is meant to avoid repetition 
    """

    # looks through the list_to_search
    # if it finds an item with id_number, it returns the item. If not, it returns None
    @staticmethod
    def find_item(list_to_search, id_number):
        for item in list_to_search:
            if item["id"] == id_number:
                return item
        return None

    # method used to find if a particular ID can be used for a new element. 
    # returns True if the ID can ba used and false if the ID has already been taken
    @staticmethod
    def can_use_id(list_to_search, id_number):
        if GeneralModelMethods.find_item(list_to_search, id_number) == None:
            return True
        return False

    # returns an item with a particular id in a list of items 
    # looks through the list_to_search and returns only the particular element with the id_number
    @staticmethod
    def get_single_item(list_to_search, id_number):
        return GeneralModelMethods.find_item(list_to_search, id_number)

    # enables one to edit a particular item in a list
    # looks through the list for item with id_number then changes the item_to_change to new_value
    @staticmethod
    def edit_single_item(list_to_search, id_number, item_to_change, new_value):
        for item in list_to_search:
            if (item["id"] == id_number) and (item_to_change in item):
                item[item_to_change] = new_value
                return item
        return False
    
    # deletes one particular item
    # looks through the list for an element with an id_number and deletes it
    @staticmethod
    def delete_single_item(list_to_search, id_number):
        item = GeneralModelMethods.find_item(list_to_search, id_number)
        if item != None:
            list_to_search.remove(item)
            return True
        return False
    
    
    # creates a new item
    # adds the item to the list in reference
    @staticmethod
    def create_item(list_to_append, item_details):
        try:
            id = randint(1, 1000)
            while GeneralModelMethods.can_use_id(list_to_append, id) == False:
                id = randint(1, 1000)
            item_details["id"] = id
            list_to_append.append(item_details)
            return item_details
        except Exception as e:
            print(e)
            return None

    
    # deletes a particular item from a list_to_delete with id of item_id
    @staticmethod
    def delete_item(list_to_delete, item_id):
        item = GeneralModelMethods.find_item(list_to_delete, item_id)
        if item == None:
            return False
        list_to_delete.remove(item)
        return True

