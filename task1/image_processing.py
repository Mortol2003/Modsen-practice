import cv2
import hashlib

IMAGE_SIZE = (8, 8)

def image_hash(image):
    try:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(image, IMAGE_SIZE, interpolation=cv2.INTER_AREA)
        avg = resized.mean()
        hash_val = sum(1 << (i + 8 * j) for j, row in enumerate(resized) for i, value in enumerate(row) if value > avg)
        return hashlib.md5(hash_val.to_bytes((hash_val.bit_length() + 7) // 8, byteorder='big')).hexdigest()
    except Exception as e:
        print(f"Error hashing image: {str(e)}")
        return None
