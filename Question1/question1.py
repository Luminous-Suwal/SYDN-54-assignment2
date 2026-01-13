with open("raw_text.txt", "r") as file:
    content = file.read()
    print(content)
print(ord("a"))
print(ord("A"))

def encrypt_text(shift1, shift2):
    encrypted_text = ""
    for char in content: #if alphabet is a to m (first half) then shift1 * shift2
        if char.isalpha():
            if char.islower():
                if ord(char) - ord('a') <= ord('m'):
                    encrypted_text += chr((ord(char) - ord('a') + (shift1 * shift2)) % 26 + ord('a'))
                else:
                    encrypted_text += chr((ord(char) - ord('a') + (shift1 * shift2)) % 26 + ord('a'))
            else:
                if ord(char) - ord('a') <= ord('m'):
                    encrypted_text += chr((ord(char) - ord('A') - shift1) % 26 + ord('A'))
                else:
                    encrypted_text += chr((ord(char) - ord('A') + (shift1 * shift1)) % 26 + ord('A'))
        else:
            encrypted_text += char

