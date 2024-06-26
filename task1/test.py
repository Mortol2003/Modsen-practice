import os
import cv2
import hashlib
import unittest
import tempfile
import shutil
from pathlib import Path

# Assuming the functions load_images_from_folder, image_hash, and find_duplicates are defined in a file named `image_duplicates.py`
from task1 import load_images_from_folder, image_hash, find_duplicates

class TestImageDuplicateFinder(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

        # Create some test images
        self.img1_path = os.path.join(self.test_dir, 'img1.jpg')
        self.img2_path = os.path.join(self.test_dir, 'img2.jpg')
        self.img3_path = os.path.join(self.test_dir, 'img3.jpg')

        self.create_test_image(self.img1_path, (255, 0, 0))  # Red image
        self.create_test_image(self.img2_path, (0, 255, 0))  # Green image
        self.create_test_image(self.img3_path, (255, 0, 0))  # Duplicate red image

        # Create another temporary directory
        self.test_dir2 = tempfile.mkdtemp()
        self.img4_path = os.path.join(self.test_dir2, 'img4.jpg')
        self.create_test_image(self.img4_path, (255, 0, 0))  # Another duplicate red image

    def tearDown(self):
        # Remove the temporary directory after the test
        shutil.rmtree(self.test_dir)
        shutil.rmtree(self.test_dir2)

    def create_test_image(self, path, color):
        img = cv2.imread(path)
        img = cv2.rectangle(img, (0, 0), (100, 100), color, -1)
        cv2.imwrite(path, img)

    def test_load_images_from_folder(self):
        images = load_images_from_folder(self.test_dir)
        self.assertEqual(len(images), 3)
        self.assertTrue(all(isinstance(img, tuple) and len(img) == 2 for img in images))

    def test_image_hash(self):
        img = cv2.imread(self.img1_path)
        hash1 = image_hash(img)
        img = cv2.imread(self.img3_path)
        hash2 = image_hash(img)
        self.assertEqual(hash1, hash2)

    def test_find_duplicates_within_folder(self):
        duplicates = find_duplicates(self.test_dir)
        self.assertEqual(len(duplicates), 1)
        self.assertEqual(duplicates[0], (self.img1_path, self.img3_path))

    def test_find_duplicates_across_folders(self):
        duplicates = find_duplicates(self.test_dir, self.test_dir2)
        self.assertEqual(len(duplicates), 2)
        self.assertTrue((self.img1_path, self.img4_path) in duplicates or (self.img4_path, self.img1_path) in duplicates)
        self.assertTrue((self.img3_path, self.img4_path) in duplicates or (self.img4_path, self.img3_path) in duplicates)

if __name__ == "__main__":
    unittest.main()
