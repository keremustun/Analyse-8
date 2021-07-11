shift = 3

text = "Hoi"

encText = ""
decText = ""

for c in text:
    #check for upper
    if c.isupper():
        c_unicode = ord(c)
        c_index = ord(c) - ord("A")

        #perform shift
        new_index = (c_index + shift) % 26

        #convert to new char
        new_unicode = new_index + ord("A")

        new_char = chr(new_unicode)

        #append to encrypted string
        encText += new_char

    else:
        encText += c

print("Plain text: ",text)
print("Enc text: ", encText)

for c in encText:
    if c.isupper():
        c_unicode = ord(c)
        c_index = ord(c) - ord("A")

        new_index = (c_index - shift) % 26

        new_unicode = new_index + ord("A")

        new_char = chr(new_unicode)

        decText += new_char

    else:
        decText += c

print(decText)