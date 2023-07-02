import face_recognition
import os
import json
import cv2

BLOCK_SIZE = 1000
cwd = os.getcwd()

def process_dataset():
    counter = 0
    # Save the root folder path
    dataset = os.path.join(cwd, "dataset")
    # List all the sub_folders name from the root folder
    dataset_listdir = os.listdir(dataset)
    # Initialize a dict that will have as a key the path of an image and as its value the characteristic vector
    image_dict = {}

    # Iterate over all the sub_folders
    for person_folder in dataset_listdir:
        # Save the path of each sub_folder
        person_folder_path = os.path.join(dataset, person_folder)
        # List the names of all the images from the subfolder where we are in
        person_folder_listdir = os.listdir(person_folder_path)
        # Iterate over all the images
        for image in person_folder_listdir:
            # Save the path of the image
            image_path = os.path.join(person_folder_path, image)
            # Load the image
            face = face_recognition.load_image_file(image_path)
            # Identifies the faces in the image and create a characteristic vector for each face recognized
            face_encoding = face_recognition.face_encodings(face)
            # Create the key that will be associated to the image in the dict image_dict created
            key = person_folder + "/" + image

            # Just the images with at least a face recognized will be processed
            if len(face_encoding) != 0:
                # The value associated to the image will be the characteristic vector of the first face recognized in the IMAGE
                new_face_encoding = tuple(face_encoding[0])
                image_dict[key] = str(new_face_encoding)
                counter += 1
                # In RAM we are able just to manage a list of BLOCK_SIZE characteristics vectors, so we need to move those to memory
                # and continue processing the remaining images
                # Is not better to load all the characteristic vectors in the hash and the just move those to memory once?
                if counter % BLOCK_SIZE == 0:
                    load_to_memory(image_dict)
            else:
                print("\nNo face was found in: " + str(image_path))
    # Moving characteristic vectors to memory
    # WARNING: If the image_dict is empty, is still necessary to run this code?            
    load_to_memory(image_dict)


def load_to_memory(image_dict):
    # Create the path where the characteristic vectors of image dict will be allocated
    processed_path = os.path.join(cwd, "feature_vectors.json")
    try:
        # Open the path of the file to store the characteristict vectors and append the new ones
        with open(processed_path, 'a', encoding="utf-8") as file:
            for keyword in image_dict:
                file.write(json.dumps({keyword: image_dict[keyword]}, ensure_ascii=False))
                file.write("\n")
            file.close()
            print("\nBlock uploaded")
        image_dict.clear()
        return 1
    except IOError:
        print("\nProblem reading: " + str(processed_path))
        return 0