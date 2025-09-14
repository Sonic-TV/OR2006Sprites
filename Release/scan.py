#!/usr/bin/python
# Python script
# Made by Envido32

import os

def scan_directory(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if not filename.endswith(".dds"):
                continue

            name, ext = os.path.splitext(filename)
            parts = name.split("_")

            # Must be exactly 2 parts: id and hxw
            if len(parts) != 2:
                continue

            file_id, size_part = parts
            if "x" not in size_part:
                continue

            h, w = size_part.split("x", 1)

            # Check that h and w are integers
            if not (h.isdigit() and w.isdigit()):
                continue

            # Check that ID is hex
            try:
                int(file_id, 16)  # will raise ValueError if not hex
            except ValueError:
                continue

            # Check length of ID
            id_len = len(file_id)
            
            # Too long → just report
            if id_len > 8:
                print(f"Invalid ID length ({id_len} digits): {os.path.join(dirpath, filename)}")

            # Too short → pad with zeros and rename
            elif id_len < 8:
                new_id = file_id.zfill(8)  # pad with leading zeros
                new_name = f"{new_id}_{size_part}{ext}"
                old_path = os.path.join(dirpath, filename)
                new_path = os.path.join(dirpath, new_name)

                # Rename file
                os.rename(old_path, new_path)
                print(f"Renamed: {old_path} → {new_path}")

            # Exactly 8 → OK (do nothing)
            else:
                pass

if __name__ == "__main__":
    # root = input("Enter directory to scan: ").strip()
    root = os.getcwd()
    scan_directory(root)
