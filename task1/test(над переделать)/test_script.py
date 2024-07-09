import pytest
import os
import cv2
from unittest.mock import patch, MagicMock
from task import load_images_from_folder, image_hash, find_duplicates

@pytest.fixture
def mock_images():
    # Create mock images
    img1 = (r'C:\Student\practik\task1\Modsen-practice\task1\5 Flower Types Classification Dataset\image1.jpg', MagicMock())
    img2 = (r'C:\Student\practik\task1\Modsen-practice\task1\5 Flower Types Classification Dataset\image2.jpg', MagicMock())
    img3 = (r'C:\Student\practik\task1\Modsen-practice\task1\5 Flower Types Classification Dataset\image3.jpg', MagicMock())
    return [img1, img2, img3]

@pytest.fixture
def mock_image_hash():
    return 'mock_hash'

@patch('task.os.walk')
@patch('task.cv2.imread')
def test_load_images_from_folder(mock_imread, mock_os_walk, mock_images):
    folder = r'C:\Student\practik\task1\Modsen-practice\task1\5 Flower Types Classification Dataset'
    mock_os_walk.return_value = [
        (folder, [], ['image1.jpg', 'image2.jpg', 'image3.jpg'])
    ]
    mock_imread.side_effect = [img for _, img in mock_images]

    print(f"Running test_load_images_from_folder with folder: {folder}")
    images = load_images_from_folder(folder)
    assert len(images) == 3
    for i, img in enumerate(images):
        assert img[0] == mock_images[i][0]

@patch('task.cv2.cvtColor')
@patch('task.cv2.resize')
@patch('task.hashlib.md5')
def test_image_hash(mock_md5, mock_resize, mock_cvtColor):
    image = MagicMock()
    mock_cvtColor.return_value = image
    mock_resize.return_value = image
    mock_md5.return_value.hexdigest.return_value = 'mock_hash'

    print("Running test_image_hash")
    hash_val = image_hash(image)
    assert hash_val == 'mock_hash'

@patch('task.load_images_from_folder')
@patch('task.image_hash')
def test_find_duplicates(mock_image_hash, mock_load_images, mock_images):
    folder = r'C:\Student\practik\task1\Modsen-practice\task1\5 Flower Types Classification Dataset'
    mock_load_images.return_value = mock_images
    mock_image_hash.side_effect = ['mock_hash1', 'mock_hash2', 'mock_hash1']

    print(f"Running test_find_duplicates with folder: {folder}")
    duplicates = find_duplicates(folder)
    assert len(duplicates) == 1
    assert duplicates[0] == (mock_images[0][0], mock_images[2][0])

@patch('task.load_images_from_folder')
@patch('task.image_hash')
def test_find_duplicates_two_folders(mock_image_hash, mock_load_images, mock_images):
    folder1 = r'C:\Student\practik\task1\Modsen-practice\task1\5 Flower Types Classification Dataset'
    folder2 = r'C:\Student\practik\task1\Modsen-practice\task1\5 Flower Types Classification Dataset'
    mock_load_images.side_effect = [mock_images, mock_images]
    mock_image_hash.side_effect = ['mock_hash1', 'mock_hash2', 'mock_hash1', 'mock_hash1', 'mock_hash2', 'mock_hash1']

    print(f"Running test_find_duplicates_two_folders with folders: {folder1}, {folder2}")
    duplicates = find_duplicates(folder1, folder2)
    assert len(duplicates) == 3
    assert duplicates[0] == (mock_images[0][0], mock_images[2][0])
    assert duplicates[1] == (mock_images[0][0], mock_images[0][0])
    assert duplicates[2] == (mock_images[2][0], mock_images[2][0])

if __name__ == "__main__":
    pytest.main()
