# DocuBrain - Invoice and Employee Data Extraction

## Overview
This project is designed to extract and process structured data from invoices and employee documents using **GPT-4 Turbo**. It integrates **OCR**, **AI-based entity extraction**, and **PostgreSQL** for structured storage.

## Features
- **Invoice Processing:** Extracts vendor name, invoice date, total items, amount, and tax from invoices.
- **Employee Data Extraction:** Retrieves employee name, email, phone number, qualification, and address.
- **AI-powered Chatbot:** Provides support on enterprise-related queries, including rules and regulations.
- **Secure API Handling:** Uses a `.env` file to protect sensitive API keys.

## Setup Instructions
### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- PostgreSQL
- Required Python libraries (install via `requirements.txt`)

### Installation Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/rajesh096/DocuBrain.git
   cd DocuBrain
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the application:
   ```sh
   python main.py
   ```

## API Key Handling
- **Environment Variables:** The application reads API keys from a `.env` file, ensuring security.
- **Error Handling:** If no API key is provided, the user is prompted to enter one manually.

## Enterprise Support Chatbot
- This project includes a chatbot that can answer enterprise-related queries such as:
  - Company policies
  - Rules and regulations
  - Work environment-related doubts
- The chatbot uses OpenAI's API to process user queries and provide relevant responses.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License
MIT License. Feel free to modify and use it as needed.

## Contact
For any issues or feature requests, open an issue on GitHub or contact us at **srajeshrajesh607@gmail.com**.

