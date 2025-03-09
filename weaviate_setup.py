import os
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "API KEY HERE"
import weaviate
from weaviate.embedded import EmbeddedOptions
import pdfplumber

# Set your OpenAI API key if using auto-vectorization with text2vec-openai
# os.environ["OPENAI_APIKEY"] = "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"

# Initialize Embedded Weaviate (auto-vectorization enabled)
client = weaviate.Client(
    embedded_options=EmbeddedOptions(
        additional_env_vars={
            # Remove modules that require extra config if not needed.
            "ENABLE_MODULES": "text2vec-huggingface"
        }
    )
)

# Define the schema for storing PDF text and metadata
schema = {
    "classes": [
        {
            "class": "PDFInsights",
            "description": "Store PDF text and metadata",
            "vectorizer": "text2vec-huggingface",  # Auto-vectorization using OpenAI embeddings
            "properties": [
                {"name": "text", "dataType": ["text"]},
                {"name": "metadata", "dataType": ["string"]}
            ]
        }
    ]
}

# Create the schema in Weaviate
client.schema.delete_class("PDFInsights")
client.schema.create(schema)
# Function to extract text from a PDF using pdfplumber
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# Set the folder where your PDFs are stored (adjust the path as needed)
pdf_folder = "/Users/spotnuru/Desktop/school/spectical_health/UHC IFP Documentation"

# Loop over all PDF files in the folder, extract text, and insert into Weaviate
for filename in os.listdir(pdf_folder):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, filename)
        print(f"Processing {filename} ...")
        pdf_text = extract_text_from_pdf(pdf_path)
        data_object = {
            "text": pdf_text,
            "metadata": filename
        }
        client.data_object.create(data_object, "PDFInsights")

print("All PDFs have been processed and inserted into Weaviate.")
input("Press Enter to exit and shut down Weaviate...")

