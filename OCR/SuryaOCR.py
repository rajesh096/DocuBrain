from PIL import Image
from surya.ocr import run_ocr
from surya.model.detection import segformer
from surya.model.recognition import model as rec_model, processor as rec_processor

def extract_text(image_path, languages=["en"]):
    # Open the image file
    image = Image.open(image_path)

    # Load the detection model and processor
    det_processor, det_model = segformer.load_processor(), segformer.load_model()

    # Load the recognition model and processor
    rec_model_instance, rec_processor_instance = rec_model.load_model(), rec_processor.load_processor()

    # Run the OCR process on the image
    predictions = run_ocr(
        [image], [languages], det_model, det_processor, rec_model_instance, rec_processor_instance
    )[0]

    # Extract text from the OCR predictions
    extracted_text = [line.text for line in list(predictions)[0][1]]

    return extracted_text

# Example usage
image_path = r"E:\Project\DocuBrain\Invoice_samples\invoice2.png"
text = extract_text(image_path, languages=["en"])
print("\n".join(text))
