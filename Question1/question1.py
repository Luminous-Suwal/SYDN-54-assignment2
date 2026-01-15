def encrypt_text(input_file, output_file, shift1, shift2):
    try:
        with open(input_file, 'r') as f:
            content = f.read()
        
        encrypted_chars = []
        for char in content:
            if char.islower():
                # Lowercase Logic
                if char <= 'm': # First half (a-m)
                    # Shift forward by shift1 * shift2
                    shift = shift1 * shift2
                    new_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
                else: # Second half (n-z)
                    # Shift backward by shift1 + shift2
                    shift = shift1 + shift2
                    new_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                encrypted_chars.append(new_char)
                
            elif char.isupper():
                # Uppercase Logic
                if char <= 'M': # First half (A-M)
                    # Shift backward by shift1
                    shift = shift1
                    new_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                else: # Second half (N-Z)
                    # Shift forward by shift2 squared
                    shift = shift2 ** 2
                    new_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                encrypted_chars.append(new_char)
                
            else:
                # Numbers/Symbols remain unchanged
                encrypted_chars.append(char)
        
        encrypted_text = "".join(encrypted_chars)
        
        with open(output_file, 'w') as f:
            f.write(encrypted_text)
            
        print(f"Encryption successful! Saved to '{output_file}'")
        
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")

def decrypt_text(input_file, output_file, shift1, shift2):
    try:
        with open(input_file, 'r') as f:
            content = f.read()            
        decrypted_chars = []
        for char in content:
            if char.islower():
                # We don't know if the original was Group 1 (a-m) or Group 2 (n-z).
                # We calculate BOTH possibilities and see which one is valid.                
                # Option 1: Reverse Group 1 logic (+ shift becomes - shift)
                s1 = shift1 * shift2
                candidate1 = chr((ord(char) - ord('a') - s1) % 26 + ord('a'))
                
                # Option 2: Reverse Group 2 logic (- shift becomes + shift)
                s2 = shift1 + shift2
                candidate2 = chr((ord(char) - ord('a') + s2) % 26 + ord('a'))
                
                # Check validity
                c1_valid = candidate1 <= 'm' # Must fall in a-m
                c2_valid = candidate2 > 'm'  # Must fall in n-z
                
                if c1_valid and not c2_valid:
                    decrypted_chars.append(candidate1)
                elif c2_valid and not c1_valid:
                    decrypted_chars.append(candidate2)
                elif c1_valid and c2_valid:
                    # Collision: Both are mathematically possible. 
                    # Defaulting to candidate 1 (standard behavior for this assignment type)
                    decrypted_chars.append(candidate1)
                else:
                    decrypted_chars.append(char) # Should not happen

            elif char.isupper():
                # Same check for Uppercase               
                # Option 1: Reverse Group 1 (A-M) logic (- becomes +)
                s1 = shift1
                candidate1 = chr((ord(char) - ord('A') + s1) % 26 + ord('A'))              
                # Option 2: Reverse Group 2 (N-Z) logic (+ becomes -)
                s2 = shift2 ** 2
                candidate2 = chr((ord(char) - ord('A') - s2) % 26 + ord('A'))              
                c1_valid = candidate1 <= 'M'
                c2_valid = candidate2 > 'M'               
                if c1_valid and not c2_valid:
                    decrypted_chars.append(candidate1)
                elif c2_valid and not c1_valid:
                    decrypted_chars.append(candidate2)
                elif c1_valid and c2_valid:
                    decrypted_chars.append(candidate1)
                else:
                    decrypted_chars.append(char)
            
            else:
                decrypted_chars.append(char)

        decrypted_text = "".join(decrypted_chars)
        
        with open(output_file, 'w') as f:
            f.write(decrypted_text)
            
        print(f"Decryption successful! Saved to '{output_file}'")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")

def verify_decryption(original_file, decrypted_file):
    try:
        with open(original_file, 'r') as f1:
            original = f1.read()
        with open(decrypted_file, 'r') as f2:
            decrypted = f2.read()
            
        print("\n--- Verification Results ---")
        if original == decrypted:
            print("SUCCESS: The decrypted text matches the original exactly.")
        else:
            print("FAILURE: The decrypted text does NOT match the original.")
            print("Note: If you used inputs like 2 and 3, this may be due to mathematical collisions")
            print("inherent in the assignment rules (e.g. 'l' and 'w' mapping to the same letter).")
            
    except FileNotFoundError:
        print("Error: Could not find files to verify.")

# --- Main Execution Block ---
if __name__ == "__main__":
            
    print("--- Assignment 1: Encryption Tool ---")
    try:
        # 1. Prompt User
        s1 = int(input("Enter integer for shift1: "))
        s2 = int(input("Enter integer for shift2: "))
        
        # 2. Encrypt
        encrypt_text("raw_text.txt", "encrypted_text.txt", s1, s2)
        
        # 3. Decrypt
        decrypt_text("encrypted_text.txt", "decrypted_text.txt", s1, s2)
        
        # 4. Verify
        verify_decryption("raw_text.txt", "decrypted_text.txt")
        
    except ValueError:
        print("Invalid input! Please enter whole numbers.")