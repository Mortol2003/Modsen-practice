from image_processing import image_hash
from file_operations import load_images_from_folder

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
