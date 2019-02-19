import re


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
    
