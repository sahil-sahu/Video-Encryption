# Video Encryption and Decryption with RSA and AES

**Description**

This project implements a video encryption and decryption system using the RSA and AES algorithms. It encrypts videos frame-by-frame, ensuring strong security for your video content.

**Features**

* Securely encrypts videos using a combination of RSA and AES for key exchange and data encryption.
* Decrypts encrypted videos with the corresponding private key.
* Provides user-friendly controls for selecting videos, performing encryption/decryption, and viewing the original/encrypted video.


**Installation**

1. Clone this repository and download the code files.
2. Install the required libraries using `pip install -r requirements.txt`.

**Usage**

1. Run the script `video_encryption_decryption.py`.
2. The graphical user interface (GUI) will display options for selecting a video, choosing encryption or decryption, and viewing the original/encrypted video.
3. Select the desired video file and click the appropriate button ("ENCRYPT VIDEO" or "DECRYPT VIDEO").
4. If decrypting, you might be prompted to enter the encrypted key (obtained during encryption).
5. The encrypted/decrypted video will be saved in the `output` directory.

**Notes**

* This project uses RSA key pairs (`rsa_private_key.pem` and `rsa_public_key.pem`) for encryption and decryption. These keys are automatically generated if they don't exist and are stored securely.
* The encrypted video will be larger than the original video due to the additional encryption overhead.

**Code Structure**

The code is organized into the following modules:

* `video_encryption_decryption.py`: The main script that launches the GUI and handles user interactions.
* `encryption.py`: Contains functions for RSA key generation, key encryption/decryption, and AES key generation.
* `formating.py`: Provides functions for converting video frames to text and vice versa.

**Future Enhancements**

* Implement progress bars during encryption and decryption for better user feedback.
* Allow users to specify custom output filenames.
* Consider adding support for video formats beyond AVI.
