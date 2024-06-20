import os
import cv2
import hashlib

def load_images_from_folder(folder):
    images = []
    for root, _, files in os.walk(folder):
        for filename in files:
            path = os.path.join(root, filename)
            if os.path.isfile(path) and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                img = cv2.imread(path)
                if img is not None:
                    images.append((path, img))
    return images

def image_hash(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(image, (8, 8), interpolation=cv2.INTER_AREA)
    avg = resized.mean()
    hash_val = sum(1 << (i + 8*j) for j, row in enumerate(resized) for i, value in enumerate(row) if value > avg)
    return hashlib.md5(hash_val.to_bytes(8, byteorder='big')).hexdigest()

def find_duplicates(folder):
    images = load_images_from_folder(folder)
    hashes = {}
    duplicates = []

    for path, img in images:
        hash_val = image_hash(img)
        if hash_val in hashes:
            duplicates.append((hashes[hash_val], path))
        else:
            hashes[hash_val] = path

    return duplicates

if __name__ == "__main__":
    root_folder = r'C:\Student\practik\task1\Modsen-practice\task1\5 Flower Types Classification Dataset'

    all_duplicates = []
    for subdir in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, subdir)
        if os.path.isdir(folder_path):
            duplicates = find_duplicates(folder_path)
            if duplicates:
                all_duplicates.extend(duplicates)

    if all_duplicates:
        print("Duplicates found:")
        for pair in all_duplicates:
            print(f'{pair[0]} and {pair[1]}')
    else:
        print('No duplicates found.')
