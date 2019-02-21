import re
import os

class RegularExpressions:

    @staticmethod
    def is_email(email):
        regex = re.compile("^([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)$")
        matches = regex.findall(email)
        if len(matches) != 1:
            return False
        return True
    
    @staticmethod
    def is_phone_number(phone_number):
        regex = re.compile("^\d{10}$")
        matches = regex.findall(phone_number)
        if len(matches) != 1:
            return False
        return True

    @staticmethod
    def is_http_input(url_input):
        regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        matches = regex.findall(url_input)
        if len(matches) != 1:
            return False
        return True

class Validate:

    @staticmethod
    def validate_password(password):
        # check for password length
        error = None
        if len(password) < 8:
            return "password length should be at least 8 characters long"
        
        # check if it is a commonly used password
        with open("common_passwords.txt") as f:
            lines = [line.strip("\n") for line in f.readlines()]
        
        if password in lines and error == None:
            return "password should not be a commonly used password. Use a stronger password"
        
        if password[0] == " " or password[-1] == " " and error == None:
            return "passwords should not end or begin with a space"
        
        special_characters_regex = re.compile(r'[!@#$%^&*(),.?":{}|<>]')
        capital_letters_regex = re.compile(r'[A-Z]')
        small_letters_regex = re.compile(r'[a-z]')
        all_numbers_regex = re.compile(r'[0-9]')
        
        matches_special = special_characters_regex.findall(password)
        matches_capital = capital_letters_regex.findall(password)
        matches_small = small_letters_regex.findall(password)
        matches_numbers = all_numbers_regex.findall(password)

        if (len(matches_special) == 0 or len(matches_capital) == 0 or len(matches_small) == 0 or len(matches_numbers) == 0):
            return "your password must have at least a special character, a small letter, a capital letter and a number"
        
        return True
    
    @staticmethod
    def validate_field(field):

        if field.strip() == "":
            return "{} Cannot be empty"
        
        elif field[0] == " " or field[-1] == " ":
            return "{} cannot start or end with a blank character"
        
        return True
