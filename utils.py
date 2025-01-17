import re


def remove_dots(text: str) -> str:
    return re.sub(r'\.', '', text)

def remove_quotes(text: str) -> str:
    return re.sub(r'"', '', text)