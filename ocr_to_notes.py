'''
OCRNote - OCR Screen Capture and Text Recognition Tool

This script creates a graphical user interface (GUI) application
for capturing screen regions and recognizing text within those
regions using Optical Character Recognition (OCR).
This tool can be useful for online learning to convert screenshots
to texts for notes.

Usage:
    - Run this script to open the OCR tool.
    - Click "Recognize Text" and drag the mouse to select a region
     on the screen.
    - Release the mouse button to capture the selected region.
    - Recognized text is displayed in the main window's text box.
    - You can copy the recognized text to the clipboard and clear
    the text box.

Dependencies:
    - tkinter: For creating the GUI.
    - pytesseract: For OCR text recognition.
    - numpy: For array manipulation.
    - cv2 (OpenCV): For image processing.
    - PIL (Pillow): For capturing and processing screenshots.

Author: Yongchen Wang
Date: August 24, 2023
'''

# Import libraries
import tkinter as tk
import pytesseract as pt
import numpy as np
import cv2
from PIL import ImageGrab, Image


class OCRNote:

    def __init__(self):
        # Initialize the screenshot dimensions and region to None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.rectangle = None

        # Create the main window
        self.root = tk.Tk()
        self.root.title("OCR Screen")
        self.root.geometry("500x600")

        # Create the screenshot button
        self.screenshot_btn = tk.Button(
            self.root, text="Recognize Text", command=self.recognize_text)
        self.screenshot_btn.pack(pady=10)

        # Create a button to copy the text
        self.copy_btn = tk.Button(
            self.root, text="Copy Text", command=self.copy_text)
        self.copy_btn.pack(pady=10)

        # Create a text box to display the text
        self.text_box = tk.Text(self.root, height=50, width=50)

        # Create the clear button
        self.clear_btn = tk.Button(
            self.root, text="Clear", command=self.clear_text)
        self.clear_btn.pack(pady=10)

        # Create the exit button
        self.exit_btn = tk.Button(
            self.root, text="Exit", command=self.root.destroy)
        self.exit_btn.pack(pady=10)

        self.text_box.pack(pady=10)

        self.root.mainloop()

    # Initialize the gray layer and start the selection of the region
    def recognize_text(self):
        self.create_gray_layer()

    # Start selection of the region, and mouse click event updates
    # the starting coordinates
    def start_selection(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rectangle = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='red', fill='', width=2
        )

    # Dragging the mouse updates the rectangle coordinates
    def dragging(self, event):
        self.canvas.coords(self.rectangle, self.start_x,
                           self.start_y, event.x, event.y)

    # End selection of the region, and mouse release event updates
    # the ending coordinates
    def end_selection(self, event):
        self.root.deiconify()

        self.end_x = event.x
        self.end_y = event.y

        x1 = min(self.start_x, self.end_x)
        y1 = min(self.start_y, self.end_y)
        x2 = max(self.start_x, self.end_x)
        y2 = max(self.start_y, self.end_y)

        # Capture the selected region
        screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        image = np.array(screenshot)

        # Pre-process the image to improve recognition accuracy
        image = cv2.resize(image, None, fx=1.2, fy=1.2,
                           interpolation=cv2.INTER_CUBIC)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((1, 1), np.uint8)
        image = cv2.dilate(image, kernel, iterations=1)
        image = cv2.erode(image, kernel, iterations=1)
        cv2.threshold(cv2.medianBlur(image, 3), 0, 255,
                      cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Configure the additional parameters
        custom_config = r'chi_sim -c preserve_interword_spaces=1'

        text = pt.image_to_string(
            image, lang='eng+chi_sim', config=custom_config)

        # Destroy the gray layer
        self.gray_layer.destroy()

        # Append the text into the text box
        self.text_box.insert(tk.END, text)

    # Create a gray layer to cover the screen to inform the user
    # to select a region
    def create_gray_layer(self):
        self.root.withdraw()

        # Create a new window that covers the entire screen
        self.gray_layer = tk.Toplevel()
        self.gray_layer.attributes('-fullscreen', True)

        # Create a gray canvas that fills the window
        self.canvas = tk.Canvas(self.gray_layer, bg='gray')
        self.canvas.pack(fill='both', expand=True)

        # Set the window to be transparent with 80% opacity
        self.gray_layer.attributes('-alpha', 0.5)

        # Set the focus on the gray layer's canvas
        self.canvas.focus_set()

        # Bind mouse events for rectangle selection
        self.canvas.bind('<Button-1>', self.start_selection)
        self.canvas.bind('<B1-Motion>', self.dragging)
        self.canvas.bind('<ButtonRelease-1>', self.end_selection)
        self.gray_layer.bind('<Escape>', self.remove_gray_layer)

    # Remove the gray layer
    def remove_gray_layer(self, event):
        print("remove_gray_layer")
        self.gray_layer.destroy()

    # Copy the text to the clipboard
    def copy_text(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.text_box.get('1.0', 'end'))

    # Clear the text box
    def clear_text(self):
        self.text_box.delete('1.0', 'end')


# Run the script
OCRNote()
