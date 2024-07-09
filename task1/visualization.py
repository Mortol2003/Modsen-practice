import cv2
import numpy as np

def visualize_duplicates(duplicates):
    for pair in duplicates:
        img1 = cv2.imread(pair[0])
        img2 = cv2.imread(pair[1])

        height = max(img1.shape[0], img2.shape[0])
        img1_resized = cv2.resize(img1, (int(img1.shape[1] * height / img1.shape[0]), height))
        img2_resized = cv2.resize(img2, (int(img2.shape[1] * height / img2.shape[0]), height))

        combined_img = np.hstack((img1_resized, img2_resized))

        cv2.imshow('Duplicates', combined_img)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
