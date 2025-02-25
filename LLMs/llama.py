import requests
import base64

# API configuration
API_KEY = "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"
INVOKE_URL = "https://ai.api.nvidia.com/v1/gr/meta/llama-3.2-11b-vision-instruct/chat/completions"
IMAGE_PATH = r"E:\Project\DocuBrain\Invoice_samples\invoice4.webp"
STREAM = False

# Encode the image as base64
with open(IMAGE_PATH, "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode()

# # Assert image size for API limitations
# assert len(image_b64) < 180_000, \
#     "To upload larger images, use the assets API (see docs)"

# Define headers
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "text/event-stream" if STREAM else "application/json",
    "Content-Type": "application/json"
}

# Define the payload
payload = {
    "model": "meta/llama-3.2-11b-vision-instruct",
    "messages": [
        {
            "role": "user",
            "content": f'''
                "Extract all the text from this image.

                "

                Here is the image content: <img src="data:image/png;base64,{image_b64}" />
            '''
        }
    ],
    "max_tokens": 512,
    "temperature": 0.0,
    "top_p": 1.0,
    "stream": STREAM
}

# Make the API request
response = requests.post(INVOKE_URL, headers=headers, json=payload)

# Handle response
if STREAM:
    print("Streaming response:")
    for line in response.iter_lines():
        if line:
            print(line.decode("utf-8"))
else:
    if response.status_code == 200:
        with open("output.txt", "w") as file:
            file.write(response.text)
        print("Extraction successful. Check output.txt for results.")
    else:
        with open("output.txt", "w") as file:
            file.write(f"Error: {response.status_code}, {response.text}")
        print("An error occurred. Check output.txt for details.")