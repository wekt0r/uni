def encrypt(text, key):
    return "".join(chr(ord(x)^key) for x in text)

decrypt = encrypt

print(encrypt("Python", 7))
print(decrypt(encrypt("Python", 7), 7))
