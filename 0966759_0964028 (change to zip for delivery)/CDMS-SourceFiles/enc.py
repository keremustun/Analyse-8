

def cipher_wlookup(text, key, encrypt):
    import string
    characters = string.ascii_letters + string.digits + " " + string.punctuation
    print("Extended character set: " + characters)
    if key < 0:
        print("Key cannot be negative")
        return None
    
    n = len(characters)

    if not encrypt:
        key = n - key

    table = str.maketrans(characters, characters[key:]+characters[:key])

    translated_text = text.translate(table)
    return translated_text

plain_text = "My name is Dave Adams. I am living on the 99th street. Please send the supplies!"
x = cipher_wlookup(plain_text, 15, True)
print(x)
z = cipher_wlookup(x, 15, False)
print(z)