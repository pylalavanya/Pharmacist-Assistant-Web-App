import cv2
import pytesseract

# Set Tesseract OCR Path (Modify if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from textblob import TextBlob
import pytesseract
import cv2

def extract_text(image_path):
    """Extracts and corrects text from a prescription image."""
    image = cv2.imread(image_path)
    text = pytesseract.image_to_string(image)

    # Correct spelling errors
    corrected_text = str(TextBlob(text).correct())
    return corrected_text


# Test OCR (Optional)
if __name__ == "__main__":
    text = extract_text("sample_prescription.jpg")
    print("Extracted Text:\n", text)
