import string

def encrypt_text(file_path, output_path, n, m):
    def encrypt_char(c, n, m):
        if c.islower():
            if c in string.ascii_lowercase[:13]:  # a-m
                return chr((ord(c) - ord('a') + n * m) % 26 + ord('a'))
            else:  # n-z
                return chr((ord(c) - ord('a') - (n + m)) % 26 + ord('a'))
        elif c.isupper():
            if c in string.ascii_uppercase[:13]:  # A-M
                return chr((ord(c) - ord('A') - n) % 26 + ord('A'))
            else:  # N-Z
                return chr((ord(c) - ord('A') + m ** 2) % 26 + ord('A'))
        else:
            return c

    with open(file_path, 'r') as file:
        raw_text = file.read()
    
    encrypted_text = ''.join(encrypt_char(c, n, m) for c in raw_text)
    
    with open(output_path, 'w') as file:
        file.write(encrypted_text)

def decrypt_text(input_path, output_path, n, m):
    def decrypt_char(c, n, m):
        if c.islower():
            if c in string.ascii_lowercase[:13]:  # a-m
                return chr((ord(c) - ord('a') - n * m) % 26 + ord('a'))
            else:  # n-z
                return chr((ord(c) - ord('a') + (n + m)) % 26 + ord('a'))
        elif c.isupper():
            if c in string.ascii_uppercase[:13]:  # A-M
                return chr((ord(c) - ord('A') + n) % 26 + ord('A'))
            else:  # N-Z
                return chr((ord(c) - ord('A') - m ** 2) % 26 + ord('A'))
        else:
            return c

    with open(input_path, 'r') as file:
        encrypted_text = file.read()
    
    decrypted_text = ''.join(decrypt_char(c, n, m) for c in encrypted_text)
    
    with open(output_path, 'w') as file:
        file.write(decrypted_text)

def check_correctness(original_file, decrypted_file):
    with open(original_file, 'r') as orig_file:
        original_text = orig_file.read()
    with open(decrypted_file, 'r') as dec_file:
        decrypted_text = dec_file.read()
    return original_text == decrypted_text

# Example usage:
if __name__ == "__main__":
    # Inputs
    n = 2
    m = 3
    raw_file = "raw_text.txt"
    encrypted_file = "encrypted_text.txt"
    decrypted_file = "decrypted_text.txt"

    # Encryption
    encrypt_text(raw_file, encrypted_file, n, m)
    print("Encryption complete. Encrypted text written to", encrypted_file)

    # Decryption
    decrypt_text(encrypted_file, decrypted_file, n, m)
    print("Decryption complete. Decrypted text written to", decrypted_file)

    # Check correctness
    if check_correctness(raw_file, decrypted_file):
        print("Success: Decrypted text matches the original text!")
    else:
        print("Error: Decrypted text does not match the original text.")