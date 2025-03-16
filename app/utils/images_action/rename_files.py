import os
import shutil

# Prefix
prefix = "test"

# Folder ze zdjęciami i etykietami
image_dir = "../training/fyp-3/test/images"
label_dir = "../training/fyp-3/test/labels"

# Folder docelowy
dest_image_dir = "../training/my_data/test/images"
dest_label_dir = "../training/my_data/test/labels"


image_files = {
    os.path.splitext(f)[0] for f in os.listdir(image_dir) if f.endswith(".jpg")
}
labels_files = {
    os.path.splitext(f)[0] for f in os.listdir(label_dir) if f.endswith(".txt")
}

matched = sorted(image_files & labels_files)

for i, file_name in enumerate(matched, start=1):
    new_name = f"{str(i).zfill(5)}_{prefix}"

    old_image_path = os.path.join(image_dir, file_name + ".jpg")
    new_image_path = os.path.join(dest_image_dir, new_name + ".jpg")

    old_label_path = os.path.join(label_dir, file_name + ".txt")
    new_label_path = os.path.join(dest_label_dir, new_name + ".txt")

    # Kopiowanie i zmiana nazw
    shutil.copy(old_image_path, new_image_path)
    shutil.copy(old_label_path, new_label_path)
    print(f"✔ {file_name}.jpg -> {new_name}.jpg")
    print(f"✔ {file_name}.txt -> {new_name}.txt")

print("\n✅ Wszystkie dopasowane pliki zostały skopiowane i nazwane jednolicie!")
