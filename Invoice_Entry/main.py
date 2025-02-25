import openai
import base64
import psycopg2
import json
import re
from datetime import datetime

# OpenAI API Key
OPENAI_API_KEY = "YOUR_API_KEY"

# PostgreSQL Database Connection Details
DB_NAME = "Invoice"
DB_USER = "postgres"
DB_PASSWORD = "Raju"
DB_HOST = "localhost"
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
            {"role": "system", "content": "You are an OCR and invoice processing assistant."},
            {"role": "user", "content": [
                {"type": "text", "text": "Extract the text from this invoice image."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]}
        ],
        max_tokens=1000
    )
    
    return response.choices[0].message.content

# Function to analyze extracted text and extract required entities
def process_invoice_text(extracted_text):
    prompt = f"""
    Extract the following details from this invoice text:
    - Vendor Name
    - Invoice Date (Format: YYYY-MM-DD)
    - Total Items (Number of unique line items)
    - Total Amount (Numeric value without currency symbol)
    - Tax Percentage (Numeric value, no % sign)

    Here is the invoice text:
    {extracted_text}

    Provide the extracted data in valid JSON format (without Markdown or any explanations).
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an invoice analysis assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    extracted_data = response.choices[0].message.content.strip()

    # Ensure valid JSON parsing (removes ```json and ``` if present)
    extracted_data = re.sub(r"```json|```", "", extracted_data).strip()

    return json.loads(extracted_data)

# Function to store invoice details in PostgreSQL
def store_invoice_data(invoice_data):
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        )
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            id SERIAL PRIMARY KEY,
            vendor_name VARCHAR(255),
            invoice_date DATE,
            total_items INT,
            total_amount NUMERIC(10,2),
            tax NUMERIC(5,2),
            entry_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Ensure numeric values are correctly formatted
        total_amount = float(str(invoice_data["Total Amount"]).replace("$", "").replace(",", ""))
        tax_percentage = float(str(invoice_data["Tax Percentage"]).replace("%", ""))

        # Convert date format (assuming GPT returns YYYY-MM-DD)
        invoice_date = datetime.strptime(invoice_data["Invoice Date"], "%Y-%m-%d").date()

        # SQL query to insert data
        insert_query = """
        INSERT INTO invoices (vendor_name, invoice_date, total_items, total_amount, tax, entry_date)
        VALUES (%s, %s, %s, %s, %s, %s);
        """

        # Execute query
        cursor.execute(insert_query, (
            invoice_data["Vendor Name"],
            invoice_date,
            invoice_data["Total Items"],
            total_amount,
            tax_percentage,
            datetime.now()
        ))

        # Commit and close connection
        conn.commit()
        print("✅ Invoice data successfully inserted into PostgreSQL!")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Main Function
def main():
    image_path = r"E:\Project\DocuBrain\Invoice_samples\invoice5.jpg"

    print("🔍 Extracting text from invoice...")
    extracted_text = extract_text_from_image(image_path)
    
    print("📑 Processing extracted text...")
    invoice_data = process_invoice_text(extracted_text)
    
    print("💾 Storing invoice data in PostgreSQL...")
    store_invoice_data(invoice_data)

    print("✅ Process completed successfully!")

# Run the script
if __name__ == "__main__":
    main()
