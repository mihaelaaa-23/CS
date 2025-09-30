def caesar_cipher(text, key, mode):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    n = len(alphabet)

    text = text.upper().replace(" ", "")

    for ch in text:
        if ch not in alphabet:
            raise ValueError("The text must contain only letters A–Z or a–z.")

    result = ""
    for ch in text:
        index = alphabet.index(ch)
        if mode == "encrypt":
            new_index = (index + key) % n
        else:  # decrypt
            new_index = (index - key) % n
        result += alphabet[new_index]

    return result


def main():
    print("Caesar Cipher")
    print("1. Encrypt")
    print("2. Decrypt")

    choice = input("Choose an option (1/2): ").strip()
    if choice not in ["1", "2"]:
        print("Please enter either 1 or 2.")
        return

    try:
        key = int(input("Enter the key (1–25): ").strip())
        if not (1 <= key <= 25):
            print("The key must be between 1 and 25.")
            return
    except ValueError:
        print("You must enter a number between 1 and 25.")
        return

    text = input("Enter the text: ").strip()

    if choice == "1":
        result = caesar_cipher(text, key, "encrypt")
        print("Encrypted result:", result)
    else:
        result = caesar_cipher(text, key, "decrypt")
        print("Decrypted result:", result)


if __name__ == "__main__":
    main()
