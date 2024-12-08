import json
import numpy as np
import cv2
from time import sleep
def frame_to_text(frame):
    # Convert the NumPy array directly into a flat 1D array of pixel values (RGB values)
    # arr = []  # Flatten the 2D frame (height, width, 3) to (num_pixels, 3)
    # for row in frame:
    #     arr.append(row.flatten())
    # # Convert the array into a 1D array of pixel values (flattened) and then to text
    # arr_flat = np.array(arr).flatten()  # Flatten to a single 1D array
    
    # # Convert the integers to characters and then join them to a string
    # load = ''.join(chr(num) for num in arr_flat)
    
    # return load.encode('utf-8')
    return frame.tobytes()

def btext_to_frame(width, height, btext):
    # Convert the byte text to a NumPy array of integers
    arr = np.frombuffer(btext, dtype=np.uint8)
    frame = arr.reshape(height, width, 3)
    # frame = []
    # row = []
    # # Ensure the array has the correct length
    # for i in range(0, height):
    #     for j in range(0, width):
    #         # Extract the RGB values from the integer
    #         r,g,b = 255,255,255
    #         try:
    #             # Access the R, G, B values, with bounds checking
    #             r = arr[i * width * 3 + j * 3]
    #             g = arr[i * width * 3 + j * 3 + 1]
    #             b = arr[i * width * 3 + j * 3 + 2]
    #         except IndexError:
    #             pass
    #             # If index is out of bounds, default to 255
    #             # r, g, b = 255, 255, 255
    #         row.append([r, g, b])    
    #     frame.append(row)
    #     row = []    


    
    # return arr
    return frame


def save_pretty(array, file_name):
    """
    Save a Python array to a text file in a pretty-printed format.

    :param array: List or array to save
    :param file_name: Name of the text file to save
    """
    try:
        # Prettify the array using JSON formatting
        pretty_array = json.dumps(array, indent=4)

        # Write the prettified array to a file
        with open(file_name, 'w') as file:
            file.write(pretty_array)
        
        print(f"Array successfully saved to '{file_name}' in a pretty format!")
    except Exception as e:
        print(f"An error occurred: {e}")

def playVideo(file)        :
    # Read the video file
    cap = cv2.VideoCapture(file)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
        # exit()
    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = int(1000 / fps)  # Delay in milliseconds

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Video Player', frame)
        cv2.waitKey(delay)
    cv2.destroyAllWindows()
    return    
