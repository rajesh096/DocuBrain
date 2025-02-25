import tkinter as tk
from tkinter import filedialog
from pdf_processing import extract_text_from_pdf, split_text_into_chunks
from embedding import generate_embeddings
from vector_store import VectorStore
from search import search_query
from llm import generate_response

EXISTING_PDF_PATH = r"C:\Users\sindh\OneDrive\Documents\pooja_excel\Chat-Bot-Project\data\hr_manual (1).pdf"

def choose_document_option():
    print("\nChoose an option:")
    print("1. Ask a question (use existing document)")
    print("2. Upload a new document")
    return input("Enter 1 or 2: ").strip()

def get_document_from_user():
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window
    root.attributes('-topmost', True)  # Force window to appear on top
    root.update()  # Ensure Tkinter initializes properly

    file_path = filedialog.askopenfilename(
        title="Select a PDF File",
        filetypes=[("PDF Files", "*.pdf")]
    )

    root.destroy()  # Close the Tkinter window after selection
    return file_path

# Ask the user to choose an option
choice = choose_document_option()

if choice == "1":
    PDF_PATH = EXISTING_PDF_PATH
    print(f"\nUsing existing document: {PDF_PATH}")
elif choice == "2":
    PDF_PATH = get_document_from_user()
    if not PDF_PATH:
        print("No file selected. Exiting...")
        exit()
    print(f"\nUsing uploaded document: {PDF_PATH}")
else:
    print("Invalid choice! Exiting...")
    exit()

# Processing the selected document
# print("\n⏳ Extracting text from PDF...")
text = extract_text_from_pdf(PDF_PATH)
# print("✅ Text extracted successfully!")

# print("\n⏳ Splitting text into chunks...")
chunks = split_text_into_chunks(text)
# print("✅ Text split successfully!")

# print("\n⏳ Generating embeddings...")
embeddings = generate_embeddings(chunks)
# print("✅ Embeddings generated successfully!")

# print("\n⏳ Initializing vector store...")
vector_store = VectorStore(dimension=len(embeddings[0]))
vector_store.add_documents(chunks, embeddings)
# print("✅ Document processed successfully! You can now ask questions.")

# Chatbot loop
while True:
    query = input("\nAsk a question (or type 'exit' to quit): ").strip()
    
    if query.lower() == "exit":
        print("Exiting chatbot. Goodbye!")
        break

    if query:
        # print("\n🔍 Searching for relevant text...")
        retrieved_text = search_query(query, vector_store)
        # print("✅ Search completed!")

        #print("\n🤖 Generating chatbot response...")
        answer = generate_response(query, retrieved_text)
        print("\nChatbot Answer:\n", answer)
    else:
        print("⚠ Please enter a valid question.")