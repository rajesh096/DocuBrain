import openai
import base64

# Initialize OpenAI client
client = openai.OpenAI(api_key="YOUR_API_KEY")

# Function to encode image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Image path
image_path = r"E:\Project\DocuBrain\Employee_Entry\Employee_proof_samples\resume for retail supervisor.png"
base64_image = encode_image(image_path)

# OpenAI API request
response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": "You are an OCR and image processing assistant."},
        {"role": "user", "content": [
            {"type": "text", "text": "Extract the text from this image."},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
        ]}
    ],
    max_tokens=500
)

# Print the extracted text
print(response.choices[0].message.content)
