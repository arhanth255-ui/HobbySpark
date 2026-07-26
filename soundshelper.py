import math

notes = [
    ("C",  None),
    ("CS", "DF"),
    ("D",  None),
    ("DS", "EF"),
    ("E",  None),
    ("F",  None),
    ("FS", "GF"),
    ("G",  None),
    ("GS", "AF"),
    ("A",  None),
    ("AS", "BF"),
    ("B",  None),
]

midi = 24  # C1

print("REST = 0")
print()

for octave in range(1, 9):
    for sharp, flat in notes:
        if octave == 8 and sharp != "C":
            break

        freq = round(440 * (2 ** ((midi - 69) / 12)), 2)

        print(f"NOTE_{sharp}{octave} = {freq:.2f}")

        if flat is not None:
            print(f"NOTE_{flat}{octave} = NOTE_{sharp}{octave}")

        midi += 1