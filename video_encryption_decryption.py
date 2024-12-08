
# Video Encryption Decryption

# imported necessary library
import tkinter
from tkinter import *
import tkinter as tk
import tkinter.messagebox as mbox
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2
import numpy as np
import random
import os
import ast
from cv2 import *
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from formating import frame_to_text, btext_to_frame, save_pretty, playVideo
from encryption import RSA_Hybrid_Encryptor

rsa_encryptor = RSA_Hybrid_Encryptor()
private_key_file = "rsa_private_key.pem"
public_key_file = "rsa_public_key.pem"

# Generate and write keys if not already created
if not (os.path.exists(private_key_file) and os.path.exists(public_key_file)):
    private_key, public_key = rsa_encryptor.key_create()
    rsa_encryptor.key_write(private_key, private_key_file)
    rsa_encryptor.key_write(public_key, public_key_file)
else:
    private_key = rsa_encryptor.key_load(private_key_file)
    public_key = rsa_encryptor.key_load(public_key_file)
# key = b"1234567812345678"
nonce = b"1234"

def show_popup(aesKeyEncrypted):
    # Create a Toplevel window
    popup = tk.Toplevel()
    popup.title("Key Encrypted")
    popup.geometry("300x150")  # Set window size

    # Add instructions label
    # label = tk.Label(popup, text="Click the message below to copy it:")
    # label.pack(pady=10)

    # Add a text widget for the message
    message = tk.Text(popup, height=3, wrap="word")
    message.insert("1.0", aesKeyEncrypted)
    message.configure(state="disabled")  # Make it read-only
    message.pack(pady=5, padx=10)

    # Add a button to close the popup
    close_button = tk.Button(popup, text="Close", command=popup.destroy)
    close_button.pack(pady=5)

    # Bind the click event to copy the text
    def copy_to_clipboard(event):
        popup.clipboard_clear()
        popup.clipboard_append(message.get("1.0", "end-1c"))
        popup.update()  # Required to update clipboard
        tk.Label(popup, text="Message copied!", fg="green").pack(pady=5)

    message.bind("<Button-1>", copy_to_clipboard)

def get_user_input():
    def on_submit():
        nonlocal user_input
        user_input = entry.get()  # Get the input from the entry widget
        popup.destroy()  # Close the popup

    user_input = None  # Placeholder for the user input

    # Create a popup window
    popup = tk.Toplevel()
    popup.title("Input Dialog")
    popup.geometry("300x150")

    # Add a label to instruct the user
    label = tk.Label(popup, text="Please enter your input:")
    label.pack(pady=10)

    # Add an entry widget for input
    entry = tk.Entry(popup, width=30)
    entry.pack(pady=10)
    entry.focus()  # Focus on the entry box

    # Add a submit button
    submit_button = tk.Button(popup, text="Submit", command=on_submit)
    submit_button.pack(pady=10)

    # Wait for the popup to close before returning
    popup.grab_set()  # Make the popup modal (block interaction with other windows)
    popup.wait_window()  # Pause execution until the popup is closed

    return user_input    
# Main Window & Configuration
window = tk.Tk() # created a tkinter gui window frame
window.title("Video Encryption Decryption") # title given is "DICTIONARY"
window.geometry('1000x700')

# top label
start1 = tk.Label(text = "VIDEO  ENCRYPTION\nDECRYPTION", font=("Arial", 55,"underline"), fg="magenta") # same way bg
start1.place(x = 120, y = 10)

def start_fun():
    window.destroy()

# start button created
startb = Button(window, text="START",command=start_fun,font=("Arial", 25), bg = "orange", fg = "blue", borderwidth=3, relief="raised")
startb.place(x =150 , y =580 )

# image on the main window
path = "Images/front.jpg"
# Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
img1 = ImageTk.PhotoImage(Image.open(path))
# The Label widget is a standard Tkinter widget used to display a text or image on the screen.
panel = tk.Label(window, image = img1)
panel.place(x = 130, y = 230)

# function created for exiting
def exit_win():
    if mbox.askokcancel("Exit", "Do you want to exit?"):
        window.destroy()

# exit button created
exitb = Button(window, text="EXIT",command=exit_win,font=("Arial", 25), bg = "red", fg = "blue", borderwidth=3, relief="raised")
exitb.place(x =730 , y = 580 )
window.protocol("WM_DELETE_WINDOW", exit_win)
window.mainloop()

# Main Window & Configuration
window1 = tk.Tk() # created a tkinter gui window frame
window1.title("Video Encryption Decryption") # title given is "DICTIONARY"
window1.geometry('1000x700')

# function to select file
def open_file():
    global filename
    filename = filedialog.askopenfilename(title="Select file")
    # print(filename)
    path_text.delete("1.0", "end")
    path_text.insert(END, filename)

# function to encrypt video and show encrypted video
def encrypt_fun():
    global filename
    cipherFrames = []
    originalFrames = []
    encryptedKey, key = rsa_encryptor.aes_key_generate(public_key)
    cam = cv2.VideoCapture(filename)
    frame_count = 0
    fps = cam.get(cv2.CAP_PROP_FPS)

    width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    while True:
        # Read the next frame
        ret, frame = cam.read()
        
        # If no frame is returned (end of video), break the loop
        if not ret:
            break
        if frame_count < 90:
            # Encrypting the frame
            # print(f"initited {frame_count}")
            frame_text = frame_to_text(frame)
            cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
            ciphertext, tag = cipher.encrypt_and_digest(frame_text)
            encryptedframe = btext_to_frame(width, height, ciphertext)
            cipherFrames.append(encryptedframe)
            # cipherFrames.append(btext_to_frame(width, height, frame_text))
            # cv2.imshow('Encrypted Video Play', encryptedframe)    
        else:    
            originalFrames.append(frame)
            # cv2.imshow('Video Player', frame)    
        frame_count += 1

    print("encrypting frames done in memory \nrendering encrpyted video")     

    cam.release()
    cv2.destroyAllWindows()
    output_video_path = "output/encrypted_video.avi"

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')   # Codec (use 'XVID', 'mp4v', 'MJPG', etc.)
    frame_size = (width, height)  # Frame size (width, height) - should match frame size of RGB frames
    # print(frame_size)
    out = cv2.VideoWriter(output_video_path, fourcc, fps, frame_size)

    # Loop through each frame in the array and write it to the video
    # print(cipherFrames[0])
    for frame in np.array(cipherFrames):
        out.write(frame)  # Write each frame

    for frame in np.array(originalFrames):
        out.write(frame)    

    # Release the VideoWriter object
    out.release()
    print("Done encrypting")
    # exit()
    show_popup(encryptedKey)
    playVideo("output/encrypted_video.avi")

    
# function to decrypt video and show decrypted video
def decrypt_fun():
    global filename
    frame_count = 0
    cam = cv2.VideoCapture(filename)
    frame_count = 0
    fps = cam.get(cv2.CAP_PROP_FPS)
    encryptedKey = get_user_input()
    key = rsa_encryptor.Decrypt_aes_key(private_key, encryptedKey)
    videoFrames = []
    print("frames saved")
    width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    while True:
        # print(f"initited {frame_count}")
        ret, frame = cam.read()
        
        if not ret:
            break
        if frame_count < 90:
            # Decrypting the frame
            cipherr = AES.new(key, AES.MODE_EAX, nonce=nonce)
            frame_text = frame_to_text(frame)
            plaintext = cipherr.decrypt(frame_text)
            decryptedframe = btext_to_frame(width, height, plaintext)
            videoFrames.append(decryptedframe)
            # cv2.imshow('Decrypted Video', decryptedframe)    
        else:    
            videoFrames.append(frame)
            # cv2.imshow('Decrypted Video', frame)    

        frame_count += 1

    print("decrypting frames done in memory \nrendering decrpyted video")     

    cam.release()
    cv2.destroyAllWindows()
    output_video_path = "output/decrypted_output_video.avi"

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')   # Codec (use 'XVID', 'mp4v', 'MJPG', etc.)
    frame_size = (width, height)  # Frame size (width, height) - should match frame size of RGB frames
    # print(frame_size)
    out = cv2.VideoWriter(output_video_path, fourcc, fps, frame_size)

    # Loop through each frame in the array and write it to the video
    # print(cipherFrames[0])
    for frame in np.array(videoFrames):
        out.write(frame)  # Write each frame


    # Release the VideoWriter object
    out.release()
    print("Done Decrypting")
    playVideo("output/decrypted_output_video.avi")
    # exit()

# function to reset the video to original video and show preview of that
def reset_fun():
    global filename

    source3 = cv2.VideoCapture(filename)
    # running the loop
    while True:
        # extracting the frames
        ret3, img3 = source3.read()
        # displaying the video
        cv2.imshow("Original Video", img3)
        # exiting the loop
        key = cv2.waitKey(1)
        if key == ord("q"):
            break



# top label
start1 = tk.Label(text = "VIDEO  ENCRYPTION\nDECRYPTION", font=("Arial", 55, "underline"), fg="magenta") # same way bg
start1.place(x = 120, y = 10)

# lbl1 = tk.Label(text="Select any video, dimension & crop it...", font=("Arial", 40),fg="green")  # same way bg
# lbl1.place(x=50, y=100)

lbl2 = tk.Label(text="Selected Video", font=("Arial", 30),fg="brown")  # same way bg
lbl2.place(x=80, y=220)

path_text = tk.Text(window1, height=3, width=37, font=("Arial", 30), bg="light yellow", fg="orange",borderwidth=2, relief="solid")
path_text.place(x=80, y = 270)

# Select Button
selectb=Button(window1, text="ENCRYPT VIDEO",command=encrypt_fun,  font=("Arial", 25), bg = "orange", fg = "blue")
selectb.place(x = 120, y = 450)

# Select Button
selectb=Button(window1, text="DECRYPT VIDEO",command=decrypt_fun,  font=("Arial", 25), bg = "orange", fg = "blue")
selectb.place(x = 550, y = 450)

# Select Button
selectb=Button(window1, text="SELECT",command=open_file,  font=("Arial", 25), bg = "light green", fg = "blue")
selectb.place(x = 80, y = 580)

# Get Images Button
getb=Button(window1, text="RESET",command=reset_fun,  font=("Arial", 25), bg = "yellow", fg = "blue")
getb.place(x = 420, y = 580)


def exit_win1():
    if mbox.askokcancel("Exit", "Do you want to exit?"):
        window1.destroy()

# Get Images Button
getb=Button(window1, text="EXIT",command=exit_win1,  font=("Arial", 25), bg = "red", fg = "blue")
getb.place(x = 780, y = 580)

window1.protocol("WM_DELETE_WINDOW", exit_win1)
window1.mainloop()

