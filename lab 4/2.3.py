import random
from prettytable import PrettyTable

PC2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32]

SHIFTS = [
    1, 1, 2, 2,
    2, 2, 2, 2,
    1, 2, 2, 2,
    2, 2, 2, 1,
]


def left_shift(bits, n):
    return bits[n:] + bits[:n]


def permute(bits, table):
    return ''.join(bits[i-1] for i in table)


def get_k_plus():
    while True:
        print("How would you like to provide K⁺ (56-bit key)?")
        print("  1) Enter manually")
        print("  2) Generate randomly")
        choice = input("Enter 1 or 2: ").strip()
        if choice in {"1", "2"}:
            break
        print("Invalid choice. Please enter 1 or 2.\n")

    if choice == "2":
        k_plus = ''.join(random.choice('01') for _ in range(56))
        print(f"Generated random K⁺: {k_plus}")
        return k_plus

    # Manual entry path
    while True:
        k_plus = input("Enter K⁺ (exactly 56 bits, only 0/1): ").strip().replace(" ", "")
        if len(k_plus) != 56:
            print(f"Invalid length: got {len(k_plus)}. K⁺ must be exactly 56 bits. Please try again.\n")
            continue
        if any(ch not in {'0', '1'} for ch in k_plus):
            print("Invalid characters detected. Use only '0' and '1'. Please try again.\n")
            continue
        return k_plus


def get_round_number():
    while True:
        raw = input("Enter round number i (1-16): ").strip()
        try:
            i = int(raw)
            if 1 <= i <= 16:
                return i
            print("Round number must be between 1 and 16. Please try again.\n")
        except ValueError:
            print("Please enter a valid integer between 1 and 16.\n")


def show_tables():
    print("\nUsed Tables:")
    headers = ["", *[str(i) for i in range(1, 17)]]
    round_row = ["Round", *[str(i) for i in range(1, 17)]]
    shifts_row = ["Left Shifts", *[str(s) for s in SHIFTS]]

    if PrettyTable is None:
        print("Shifts (rows):")
        print(" | ".join(headers))
        print(" | ".join(round_row))
        print(" | ".join(shifts_row))
        print("PC-2 Table:", PC2)
        print("\nTip: install PrettyTable with: pip install prettytable")
        return

    # Shifts table with 2 rows across 16 columns
    shifts_tbl = PrettyTable()
    shifts_tbl.title = "Shifts per Round (Rows)"
    shifts_tbl.field_names = headers
    shifts_tbl.add_row(round_row)
    shifts_tbl.add_row(shifts_row)

    # PC-2 table as 6 rows x 8 columns (48 entries)
    pc2_tbl = PrettyTable()
    pc2_tbl.title = "PC-2 Permutation (48 positions)"
    pc2_tbl.field_names = [f"Col {c}" for c in range(1, 8 + 1)]
    for r in range(0, len(PC2), 8):
        pc2_tbl.add_row(PC2[r:r+8])

    print(shifts_tbl)
    print(pc2_tbl)


def main():
    # 1. choose how to get k+
    k_plus = get_k_plus()

    # 2. divide into C0 and D0
    C0, D0 = k_plus[:28], k_plus[28:]
    print(f"C₀: {C0}")
    print(f"D₀: {D0}")

    # 3. choose round i (validated)
    i = get_round_number()

    # 4. perform left shifts cumulatively up to round i
    Ci, Di = C0, D0
    for r in range(i):
        Ci = left_shift(Ci, SHIFTS[r])
        Di = left_shift(Di, SHIFTS[r])
    print(f"After round {i}: C{i} = {Ci}, D{i} = {Di}")

    # 5. combine Ci and Di, then apply PC-2 to get subkey K_i
    Ki = permute(Ci + Di, PC2)
    print(f"K{i} (subkey for round {i} - {len(Ki)} bits): {Ki}")

    # 6. display used tables (pretty if available)
    show_tables()

if __name__ == "__main__":
    main()
