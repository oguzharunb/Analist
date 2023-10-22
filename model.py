import string

def isalandnum(input:str) -> bool: 
    cond1 = False
    cond2 = False
    for x in input:

        if x.isdigit():
            cond1 = True
        if x.isalpha():
            cond2 = True
    return cond1 and cond2

def convert_to_username(input:list) -> str:
    return replace_turkish_characters(''.join(input)).lower()

def replace_turkish_characters(text:str) -> str:
    turkish_to_english = {
        "ç": "c",
        "ğ": "g",
        "ı": "i",
        "ö": "o",
        "ş": "s",
        "ü": "u",
        "Ç": "C",
        "Ğ": "G",
        "İ": "I",
        "Ö": "O",
        "Ş": "S",
        "Ü": "U"
    }

    return ''.join(turkish_to_english.get(char, char) for char in text)

caesar_hashing_dict ={'a': 'l',
 'b': 'e',
 'c': 'w',
 'd': '7',
 'e': 'd',
 'f': '9',
 'g': '2',
 'h': 'o',
 'i': 'v',
 'j': 'r',
 'k': 'g',
 'l': '0',
 'm': 'm',
 'n': 'y',
 'o': '1',
 'p': 't',
 'q': 'c',
 'r': 'b',
 's': 'a',
 't': 'k',
 'u': 'z',
 'v': 'f',
 'w': 's',
 'x': 'x',
 'y': 'h',
 'z': '8',
 '0': 'u',
 '1': '3',
 '2': 'i',
 '3': '6',
 '4': 'p',
 '5': 'n',
 '6': '4',
 '7': 'q',
 '8': 'j',
 '9': '5'}
def caesar_hashing(input: str) -> str:
    return ''.join([caesar_hashing_dict[letter] for letter in input])