import json
import unicodedata

def save_dict(data, file_name):
    """ Saves the dict mapping university and institution names to cantons to canton_dict.json"""
    with open(file_name, 'w') as fp:
        json.dump(data, fp, sort_keys=True, indent=4)
        
def load_dict(file_name):
    """Loads dict mapping university and institution names to cantons"""
    with open(file_name, 'r') as fp:
        return json.load(fp)
    

def normalize_caseless(text):
    return unicodedata.normalize("NFKD", text.casefold())

def caseless_contains(str1, str2):
    """Returns true if str1 is a substring of str2 (len(str1) <= len(str2))"""
    return normalize_caseless(str1) in normalize_caseless(str2)