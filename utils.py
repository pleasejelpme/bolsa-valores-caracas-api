import re

def remove_dots(text):
    return re.sub(r'\.', '', text)