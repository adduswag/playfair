

import string

def create_key_square(keyword):
    alphabet = string.ascii_uppercase.replace('J', '')
    key_square = []
    used_letters = set()
    
    for char in keyword.upper():
        if char not in used_letters and char in alphabet:
            key_square.append(char)
            used_letters.add(char)
    
    for char in alphabet:
        if char not in used_letters:
            key_square.append(char)
    
    key_square_matrix = [key_square[i:i + 5] for i in range(0, 25, 5)]
    
    
    
    return key_square_matrix

def preprocess_text(text):
    text = text.upper().replace('J', 'I')
    processed_text = ""
    
    i = 0
    while i < len(text):
        if text[i] in string.ascii_uppercase:
            processed_text += text[i]
            if i + 1 < len(text) and text[i] == text[i + 1]:
                processed_text += 'X'
            elif i + 1 < len(text) and text[i + 1] in string.ascii_uppercase:
                processed_text += text[i + 1]
                i += 1
        i += 1
    
    if len(processed_text) % 2 != 0:
        processed_text += 'X'
    
    return processed_text

def find_position(key_square, char):
    for row in range(5):
        for col in range(5):
            if key_square[row][col] == char:
                return row, col
    return None, None

def encrypt_digraph(digraph, key_square):
    row1, col1 = find_position(key_square, digraph[0])
    row2, col2 = find_position(key_square, digraph[1])
    
    if row1 is None or row2 is None or col1 is None or col2 is None:
        raise ValueError("Invalid character in text")
    
    if row1 == row2:
        return key_square[row1][(col1 + 1) % 5] + key_square[row2][(col2 + 1) % 5]
    elif col1 == col2:
        return key_square[(row1 + 1) % 5][col1] + key_square[(row2 + 1) % 5][col2]
    else:
        return key_square[row1][col2] + key_square[row2][col1]

def decrypt_digraph(digraph, key_square):
    row1, col1 = find_position(key_square, digraph[0])
    row2, col2 = find_position(key_square, digraph[1])
    
    if row1 is None or row2 is None or col1 is None or col2 is None:
        raise ValueError("Invalid character in text")
    
    if row1 == row2:
        decrypted_pair = key_square[row1][(col1 - 1) % 5] + key_square[row2][(col2 - 1) % 5]
    elif col1 == col2:
        decrypted_pair = key_square[(row1 - 1) % 5][col1] + key_square[(row2 - 1) % 5][col2]
    else:
        decrypted_pair = key_square[row1][col2] + key_square[row2][col1]
    
    return decrypted_pair

def playfair_cipher(text, keyword, encrypt=True):
    key_square = create_key_square(keyword)
    text = preprocess_text(text)
    result = ""
    
    for i in range(0, len(text), 2):
        digraph = text[i:i+2]
        if encrypt:
            result += encrypt_digraph(digraph, key_square)
        else:
            result += decrypt_digraph(digraph, key_square)
    
    return result

def remove_inserted_x(text):
    result = ""
    i = 0
    while i < len(text):
        if i < len(text) - 2 and text[i] == text[i+2] and text[i+1] == 'X':
            result += text[i]
            i += 2
        else:
            result += text[i]
        i += 1
    
    if result.endswith('X'):
        result = result[:-1]
    
    return result


keyword = "SUPERSPY"
ciphertext = "IKEWENENXLNQLPZSLERUMRHEERYBOFNEINCHCV"
decryptedtext = playfair_cipher(ciphertext, keyword, encrypt=False)
cleaned_text = remove_inserted_x(decryptedtext)

print(cleaned_text)

