def prepare_key(key):
    key = key.upper()
    key = key.replace('Î', 'I')
    key = key.replace(' ', '')

    prepared_key = ''
    for char in key:
        if char not in prepared_key:
            prepared_key += char
    return prepared_key


def build_matrix(key):
    alphabet = "ABCDEFGHIJKLMNOPQRSȘȚTUVWXYZĂÂ"

    prepared_key = prepare_key(key)

    matrix_string = prepared_key
    for letter in alphabet:
        if letter not in matrix_string:
            matrix_string += letter

    matrix = []
    for i in range(5):
        row = []
        for j in range(6):
            index = i * 6 + j
            if index < len(matrix_string):
                row.append(matrix_string[index])
            else:
                row.append('')
        matrix.append(row)
    return matrix


def display_matrix(matrix):
    print("\nEncryption Matrix:")
    print("+" + "-" * 47 + "+")
    for row in matrix:
        print("|", end="")
        for cell in row:
            if cell:
                print(f" {cell:^5} |", end="")
            else:
                print("      |", end="")
        print()
        print("+" + "-" * 47 + "+")
    print()


def prepare_text_encrypt(text):
    text = text.upper().replace(' ', '')
    text = text.replace('Î', 'I')

    valid_chars = "ABCDEFGHIJKLMNOPQRSȘȚTUVWXYZĂÂ"
    clean_text = ""
    for char in text:
        if char in valid_chars:
            clean_text += char
    return clean_text


def split_into_pairs(text):
    pairs = []
    i = 0
    while i < len(text):
        if i == len(text) - 1:
            pairs.append((text[i] + 'X'))
            i += 1
        elif text[i] == text[i + 1]:
            pairs.append((text[i] + 'X'))
            i += 1
        else:
            pairs.append((text[i] + text[i + 1]))
            i += 2
    return pairs


def find_position(matrix, letter):
    letter = letter.upper()
    if letter == 'Î':
        letter = 'I'

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == letter:
                return i, j
    return None, None


def encrypt_pair(matrix, pair):
    letter1, letter2 = pair[0], pair[1]
    row1, col1 = find_position(matrix, letter1)
    row2, col2 = find_position(matrix, letter2)

    if row1 is None or row2 is None:
        return pair

    #Rule 1: Rectangle - different rows and columns
    if row1 != row2 and col1 != col2:
        return matrix[row1][col2] + matrix[row2][col1]
    #Rule 2: Same Row
    elif row1 == row2:
        new_col1 = (col1 + 1) % 6
        new_col2 = (col2 + 1) % 6

        while not matrix[row1][new_col1]:
            new_col1 = (new_col1 + 1) % 6
        while not matrix[row2][new_col2]:
            new_col2 = (new_col2 + 1) % 6

        return matrix[row1][new_col1] + matrix[row2][new_col2]
    #Rule 3: Same Column
    else:
        new_row1 = (row1 + 1) % 5
        new_row2 = (row2 + 1) % 5
        return matrix[new_row1][col1] + matrix[new_row2][col2]


def decrypt_pair(matrix, pair):
    letter1, letter2 = pair[0], pair[1]
    row1, col1 = find_position(matrix, letter1)
    row2, col2 = find_position(matrix, letter2)

    if row1 is None or row2 is None:
        return pair

    #Rule 1: Rectangle - different rows and columns
    if row1 != row2 and col1 != col2:
        return matrix[row1][col2] + matrix[row2][col1]
    #Rule 2: Same Row
    elif row1 == row2:
        new_col1 = (col1 - 1) % 6
        new_col2 = (col2 - 1) % 6

        while not matrix[row1][new_col1]:
            new_col1 = (new_col1 - 1) % 6
        while not matrix[row2][new_col2]:
            new_col2 = (new_col2 - 1) % 6

        return matrix[row1][new_col1] + matrix[row2][new_col2]
    #Rule 3: Same Column
    else:
        new_row1 = (row1 - 1) % 5
        new_row2 = (row2 - 1) % 5
        return matrix[new_row1][col1] + matrix[new_row2][col2]


def encrypt_message(message, key):
    #a: prepare text
    prepared_text = prepare_text_encrypt(message)
    pairs = split_into_pairs(prepared_text)
    #b: build matrix
    matrix = build_matrix(key)
    #c: encrypt pairs
    ciphertext = ""
    for pair in pairs:
        ciphertext += encrypt_pair(matrix, pair)
    return ciphertext, matrix, pairs


def decrypt_message(ciphertext, key):
    #a: prepare text
    prepared_text = prepare_text_encrypt(ciphertext)
    pairs = split_into_pairs(prepared_text)
    #b: build matrix
    matrix = build_matrix(key)
    #c: decrypt pairs
    plaintext = ""
    for pair in pairs:
        plaintext += decrypt_pair(matrix, pair)
    return plaintext, matrix, pairs


def validate_input(text):
    valid_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZĂÂÎȘȚabcdefghijklmnopqrstuvwxyzăâîșț "

    invalid_chars = set()
    for char in text:
        if char not in valid_chars:
            invalid_chars.add(char)

    if invalid_chars:
        print(f"\nWARNING: Invalid characters detected: {', '.join(invalid_chars)}")
        print("Valid character range: A-Z, a-z (including Ă, Â, Î, Ș, Ț) and spaces")
        return False
    return True


def main():
    print("Playfair Cipher - Romanian Language (31 letters)")
    print("Note: Letters I and Î are combined in the same cell (I/Î)")

    while True:
        print("\nChoose operation:")
        print("  1. Encrypt a message")
        print("  2. Decrypt a ciphertext")
        print("  3. Exit")

        choice = input("\nEnter your choice (1/2/3): ").strip()

        if choice == '3':
            print("\nGoodbye!")
            break
        if choice not in ['1', '2']:
            print("Invalid choice! Please enter 1, 2, or 3.")
            continue

        while True:
            key = input("\nEnter the encryption key (minimum 7 characters): ").strip()
            if not validate_input(key):
                continue
            key_no_spaces = key.replace(' ', '')
            if len(key_no_spaces) < 7:
                print(f"Key is too short! You have {len(key_no_spaces)} characters.")
                print("Minimum required: 7 characters")
                continue
            break

        if choice == '1':
            while True:
                message = input("\nEnter the message to encrypt: ").strip()
                if validate_input(message):
                    break

            ciphertext, matrix, pairs = encrypt_message(message, key)

            print("\n" + "*" * 60)
            print("ENCRYPTION RESULT")

            print(f"\nKey used: {key}")
            print(f"Prepared key (no duplicates): {prepare_key(key)}")

            display_matrix(matrix)

            print(f"Original message: {message}")
            print(f"Prepared text (uppercase, no spaces): {prepare_text_encrypt(message)}")
            print(f"Split into pairs: {' '.join(pairs)}")
            print(f"\n{'Pair':<8} -> {'Encrypted':<10} (Rule applied)")
            print("-" * 50)

            #show encryption of each pair
            prepared_text = prepare_text_encrypt(message)
            pairs_display = split_into_pairs(prepared_text)
            for pair in pairs_display:
                encrypted = encrypt_pair(matrix, pair)
                row1, col1 = find_position(matrix, pair[0])
                row2, col2 = find_position(matrix, pair[1])
                if row1 == row2:
                    rule = "Same row"
                elif col1 == col2:
                    rule = "Same column"
                else:
                    rule = "Rectangle"
                print(f"{pair:<8} -> {encrypted:<10} ({rule})")

            print(f"\nFINAL CIPHERTEXT: {ciphertext}")
            print(f"Formatted in pairs: {' '.join([ciphertext[i:i + 2] for i in range(0, len(ciphertext), 2)])}")

        else:
            while True:
                ciphertext = input("\nEnter the ciphertext to decrypt: ").strip()
                if validate_input(ciphertext):
                    break

            plaintext, matrix, pairs = decrypt_message(ciphertext, key)

            print("\n" + "*" * 60)
            print("DECRYPTION RESULT")

            print(f"\nKey used: {key}")
            print(f"Prepared key (no duplicates): {prepare_key(key)}")

            display_matrix(matrix)

            print(f"Ciphertext: {ciphertext}")
            print(f"Split into pairs: {' '.join(pairs)}")
            print(f"\n{'Pair':<8} -> {'Decrypted':<10} (Rule applied)")
            print("-" * 50)

            #show decryption of each pair
            for pair in pairs:
                decrypted = decrypt_pair(matrix, pair)
                row1, col1 = find_position(matrix, pair[0])
                row2, col2 = find_position(matrix, pair[1])

                if row1 == row2:
                    rule = "Same row"
                elif col1 == col2:
                    rule = "Same column"
                else:
                    rule = "Rectangle"

                print(f"{pair:<8} -> {decrypted:<10} ({rule})")

            print(f"\nFINAL DECRYPTED MESSAGE: {plaintext}")
            print("\n" + "-" * 60)
            print("NOTE: You need to manually add spaces according to")
            print("      the language logic and message context.")
            print("      The letter X may indicate:")
            print("      - Separation of duplicate letters")
            print("      - Padding for odd-length text")
            print("-" * 60)


if __name__ == "__main__":
    main()
