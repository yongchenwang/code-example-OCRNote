# OCRNote - OCR Screen Capture and Text Recognition Tool

**OCRNote** is a graphical user interface (GUI) application for capturing screen regions and recognizing text within those regions using Optical Character Recognition (OCR). This tool can be useful for online learning, allowing you to convert screenshots into text for notes and further processing.

## Usage

Follow these steps to use OCRNote:

- Create the virtual environment and install the dependencies from requirements.txt.
- Run the script to open the OCR tool.
- Click the "Recognize Text" button to activate the screenshot capture mode.
- Drag your mouse to select a region on the screen that contains the text you want to recognize.
- Release the mouse button to capture the selected region.
- The recognized text will be displayed in the main window's text box.
- You can copy the recognized text to the clipboard by clicking the "Copy Text" button.
- To clear the text box, click the "Clear" button.
- To exit the application, click the "Exit" button.

## Dependencies

OCRNote relies on the following Python libraries:

- **tkinter**: For creating the graphical user interface.
- **pytesseract**: For Optical Character Recognition (OCR) text recognition.
- **numpy**: For array manipulation.
- **cv2 (OpenCV)**: For image processing.
- **PIL (Pillow)**: For capturing and processing screenshots.

## Author

- **Author**: Yongchen Wang
- **Date**: August 24, 2023
