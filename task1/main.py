import os
from duplicate_detection import find_duplicates
from visualization import visualize_duplicates

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_folder = os.path.join(script_dir, '5 Flower Types Classification Dataset')

    if not os.path.exists(root_folder):
        print(f"Error: The folder '{root_folder}' does not exist.")
    else:
        duplicates = []

        for subdir in os.listdir(root_folder):
            folder_path = os.path.join(root_folder, subdir)
            if os.path.isdir(folder_path):
                duplicates = find_duplicates(folder_path)
                if duplicates:
                    duplicates.extend(duplicates)

        folder1 = os.path.join(script_dir, 'folder1')
        folder2 = os.path.join(script_dir, 'folder2')

        if os.path.exists(folder1) and os.path.exists(folder2):
            duplicates_between_folders = find_duplicates(folder1, folder2)
            if duplicates_between_folders:
                duplicates.extend(duplicates_between_folders)
        else:
            print("One or both of the comparison folders do not exist.")

        if duplicates:
            print("Duplicates found:")
            for pair in duplicates:
                print(f'{pair[0]} and {pair[1]}')

            visualize_duplicates(duplicates)
        else:
            print('No duplicates found.')
