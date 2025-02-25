import openai
import base64
import psycopg2
import json
from datetime import datetime

# OpenAI API Key
OPENAI_API_KEY = "YOUR_API_KEY"

# PostgreSQL Database Connection Details
DB_NAME = "EmployeeDB"
DB_USER = "postgres"
DB_PASSWORD = "Raju"
DB_HOST = "localhost"  # Change if using a remote server
DB_PORT = "5432"

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Function to encode image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Function to extract text from image using GPT-4 Turbo
def extract_text_from_image(image_path):
    base64_image = encode_image(image_path)
    
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an OCR and document processing assistant."},
            {"role": "user", "content": [
                {"type": "text", "text": "Extract the text from this document image."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]}
        ],
        max_tokens=1000
    )
    
    return response.choices[0].message.content

# Function to analyze extracted text and extract required entities
def process_employee_text(extracted_text):
    prompt = f"""
    Extract the following details from this employee document:
    - Employee Name
    - Email ID
    - Phone Number
    - Qualification (Highest)
    - Address

    Here is the document text:
    {extracted_text}

    Provide the extracted data in JSON format.
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an employee data extraction assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    extracted_data = response.choices[0].message.content
    extracted_data = extracted_data.strip("```json").strip("```").strip()
    return json.loads(extracted_data)

# Function to store employee details in PostgreSQL
def store_employee_data(employee_data):
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        )
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            phone VARCHAR(20),
            qualification VARCHAR(255),
            address TEXT,
            entry_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # SQL query to insert data
        insert_query = """
        INSERT INTO employees (name, email, phone, qualification, address, entry_date)
        VALUES (%s, %s, %s, %s, %s, %s);
        """

        # Execute query
        cursor.execute(insert_query, (
            employee_data["Employee Name"],
            employee_data["Email ID"],
            employee_data["Phone Number"],
            employee_data["Qualification (Highest)"],
            employee_data["Address"],
            datetime.now()
        ))

        # Commit and close connection
        conn.commit()
        cursor.close()
        conn.close()

        print("Employee data successfully inserted into PostgreSQL!")

    except Exception as e:
        print(f"Error: {e}")

# Main Function
def main():
    image_path = r"E:\Project\DocuBrain\Employee_Entry\Employee_proof_samples\resume for retail supervisor.png"

    print("Extracting text from document...")
    extracted_text = extract_text_from_image(image_path)
    
    print("Processing extracted text...")
    employee_data = process_employee_text(extracted_text)
    
    print("Storing employee data in PostgreSQL...")
    store_employee_data(employee_data)

    print("Process completed successfully!")

# Run the script
if __name__ == "__main__":
    main()
