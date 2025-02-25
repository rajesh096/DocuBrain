import os
import base64
from together import Together

# Set your Together AI API key
os.environ["TOGETHER_API_KEY"] = "8ad1b8d740903edbce799f8f41a36ea1d36d856c010fd9824ad75d403978bd62"

# Convert local image to Base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Path to your local image
image_path = r"E:\Project\DocuBrain\Invoice_samples\invoice5.jpg"
base64_image = encode_image(image_path)

client = Together()

response = client.chat.completions.create(
    model="meta-llama/Llama-Vision-Free",
    messages=[
        {"role": "system", "content": "You are an AI assistant that can analyze images."},
        {"role": "user", "content": "Describe the image."}
    ],
    file={"image": "https://www.swipez.in/images/invoice-formats/brooklyn.png"}
,  # Correct way to send image
    max_tokens=500,
    temperature=0.7,
    top_p=0.7,
    top_k=50,
    repetition_penalty=1,
    stop=["<|eot_id|>", "<|eom_id|>"],
    stream=True
)

for token in response:
    if hasattr(token, "choices"):
        print(token.choices[0].delta.content, end="", flush=True)
