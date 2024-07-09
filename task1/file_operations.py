import os
import cv2

SUPPORTED_EXTENSIONS = ('.png', '.jpg', '.jpeg')

def load_images_from_folder(folder):
    images = []
    try:
        for root, _, files in os.walk(folder):
            for filename in files:
                path = os.path.join(root, filename)
                if os.path.isfile(path) and filename.lower().endswith(SUPPORTED_EXTENSIONS):
                    img = cv2.imread(path)
                    if img is not None:
                        images.append((path, img))
    except Exception as e:
        print(f"Error loading images from {folder}: {str(e)}")
    return images
