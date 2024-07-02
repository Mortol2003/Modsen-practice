import os
import cv2
import hashlib
import numpy as np

import os
import cv2
import hashlib
import numpy as np

def load_images_from_folder(folder):
    images = []
    try:
        for root, _, files in os.walk(folder):
            for filename in files:
                path = os.path.join(root, filename)
                if os.path.isfile(path) and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    img = cv2.imread(path)
                    if img is not None:
                        images.append((path, img))
    except Exception as e:
        print(f"Error loading images from {folder}: {str(e)}")
    return images

def image_hash(image):
    try:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(image, (8, 8), interpolation=cv2.INTER_AREA)
        avg = resized.mean()
        hash_val = sum(1 << (i + 8*j) for j, row in enumerate(resized) for i, value in enumerate(row) if value > avg)
        return hashlib.md5(hash_val.to_bytes((hash_val.bit_length() + 7) // 8, byteorder='big')).hexdigest()
    except Exception as e:
        print(f"Error hashing image: {str(e)}")
        return None

# Остальная часть кода остается без изменений

def find_duplicates(folder1, folder2=None):
    images1 = load_images_from_folder(folder1)
    images2 = load_images_from_folder(folder2) if folder2 else []

    hashes = {}
    duplicates = []

    for path, img in images1:
        hash_val = image_hash(img)
        if hash_val in hashes:
            duplicates.append((hashes[hash_val], path))
        else:
            hashes[hash_val] = path

    if folder2:
        for path, img in images2:
            hash_val = image_hash(img)
            if hash_val in hashes:
                duplicates.append((hashes[hash_val], path))
            else:
                hashes[hash_val] = path

    return duplicates

def visualize_duplicates(duplicates):
    for pair in duplicates:
        img1 = cv2.imread(pair[0])
        img2 = cv2.imread(pair[1])

        # Resize images to the same size for horizontal stacking
        height = max(img1.shape[0], img2.shape[0])
        img1_resized = cv2.resize(img1, (int(img1.shape[1] * height / img1.shape[0]), height))
        img2_resized = cv2.resize(img2, (int(img2.shape[1] * height / img2.shape[0]), height))

        # Combine images horizontally
        combined_img = np.hstack((img1_resized, img2_resized))

        cv2.imshow('Duplicates', combined_img)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root_folder = r'C:\Student\practik\task1\Modsen-practice\task1\5 Flower Types Classification Dataset'

    all_duplicates = []

    for subdir in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, subdir)
        if os.path.isdir(folder_path):
            duplicates = find_duplicates(folder_path)
            if duplicates:
                all_duplicates.extend(duplicates)

    folder1 = r'C:\Student\practik\task1\Modsen-practice\task1\folder1'
    folder2 = r'C:\Student\practik\task1\Modsen-practice\task1\folder2'
    duplicates_between_folders = find_duplicates(folder1, folder2)
    if duplicates_between_folders:
        all_duplicates.extend(duplicates_between_folders)

    if all_duplicates:
        print("Duplicates found:")
        for pair in all_duplicates:
            print(f'{pair[0]} and {pair[1]}')
        
        visualize_duplicates(all_duplicates)
    else:
        print('No duplicates found.')
