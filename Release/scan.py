#!/usr/bin/python
# Python script
# Made by Envido32

import os

def strip_leading_zeros(root_dir):
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
            if not (h.isdigit() and w.isdigit()):
                continue

            # Check that ID is hex
            try:
                int(file_id, 16)
            except ValueError:
                continue

            # Remove leading zeros
            new_id = file_id.lstrip("0")

            # If ID changed, rename file
            if new_id != file_id:
                new_name = f"{new_id}_{size_part}{ext}"
                old_path = os.path.join(dirpath, filename)
                new_path = os.path.join(dirpath, new_name)

                os.rename(old_path, new_path)
                print(f"Renamed: {old_path} -> {new_path}")

if __name__ == "__main__":
    root = os.getcwd()
    strip_leading_zeros(root)
