def letter_to_index(ch):
    return ord(ch) - ord('A')

def index_to_letter(i):
    return chr((i % 26) + ord('A'))

def caesar_with_two_keys(text, key1, key2, mode):
    alphabet = [chr(i) for i in range(ord('A'), ord('Z')+1)]
    n = len(alphabet)

    # validate key1
    if not (1 <= key1 <= 25):
        raise ValueError("Key1 must be between 1 and 25.")

    # validate key2
    key2 = key2.upper()
    if len(key2) < 7 or any(ch not in alphabet for ch in key2):
        raise ValueError("Key2 must contain only letters and be at least 7 characters long.")

    # preprocess text
    text = text.upper().replace(" ", "")
    for ch in text:
        if ch not in alphabet:
            raise ValueError("Text must contain only A–Z or a–z.")

    result = ""
    for i, ch in enumerate(text):
        index = letter_to_index(ch)

        if mode == "encrypt":
            # first Caesar with key1
            index = (index + key1) % n
            # then Vigenere with key2
            k2_shift = letter_to_index(key2[i % len(key2)])
            index = (index + k2_shift) % n
        else:  # decrypt
            # undo Vigenere first
            k2_shift = letter_to_index(key2[i % len(key2)])
            index = (index - k2_shift) % n
            # then undo Caesar
            index = (index - key1) % n

        result += index_to_letter(index)

    return result


def main():
    print("Caesar Cipher with 2 Keys")
    print("1. Encrypt")
    print("2. Decrypt")

    choice = input("Choose an option (1/2): ").strip()
    if choice not in ["1", "2"]:
        print("Invalid option.")
        return

    try:
        key1 = int(input("Enter Key1 (1–25): ").strip())
    except ValueError:
        print("Key1 must be a number between 1 and 25.")
        return

    key2 = input("Enter Key2 (letters only, length ≥ 7): ").strip()

    text = input("Enter the text: ").strip()

    if choice == "1":
        result = caesar_with_two_keys(text, key1, key2, "encrypt")
        print("Encrypted result:", result)
    else:
        result = caesar_with_two_keys(text, key1, key2, "decrypt")
        print("Decrypted result:", result)


if __name__ == "__main__":
    main()
