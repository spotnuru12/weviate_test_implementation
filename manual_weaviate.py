import os
import pdfplumber
import weaviate
from weaviate.embedded import EmbeddedOptions
from sentence_transformers import SentenceTransformer

# 1) Load a local embedding model (no API key needed)
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2) Initialize an embedded Weaviate instance
client = weaviate.Client(
    embedded_options=EmbeddedOptions(
        additional_env_vars={
            # We only load modules required for local / manual vector insertion.
            # If you don't need text2vec modules for auto-vectorizing, you can omit them entirely.
            "ENABLE_MODULES": "ref2vec-centroid"  
        }
    )
)

# 3) Define the schema with NO auto-vectorizer
schema = {
    "classes": [
        {
            "class": "PDFInsights",  # The class name for your PDF documents
            "description": "Storing PDF text, metadata, and manual vectors",
            # No 'vectorizer': ... here, because we do manual vector insertion
            "properties": [
                {"name": "text", "dataType": ["text"]},
                {"name": "metadata", "dataType": ["string"]}
            ]
        }
    ]
}

# (Optional) If you want a fresh start each run, delete the class first (removes all data).
try:
    client.schema.delete_class("PDFInsights")
except:
    pass

# 4) Create the schema
client.schema.create(schema)

# 5) PDF extraction function
def extract_text_from_pdf(pdf_path):
    all_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            if page_text:
                all_text.append((i, page_text))
    return all_text

# 6) Path to your PDFs
pdf_folder = "/Users/spotnuru/Desktop/school/spectical_health/UHC IFP Documentation"  # Replace with your actual folder

# 7) Loop through PDFs, extract text, embed, and insert into Weaviate
for filename in os.listdir(pdf_folder):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, filename)
        print(f"Processing {filename} ...")

        # Extract text by page
        pages = extract_text_from_pdf(pdf_path)

        for page_num, page_text in pages:
            # Manual embedding with sentence-transformers
            embedding = model.encode(page_text).tolist()

            # Create data object
            data_object = {
                "text": page_text,
                "metadata": f"{filename} - page {page_num}"
            }

            # Insert with manual vector
            client.data_object.create(
                data_object=data_object,
                class_name="PDFInsights",
                vector=embedding
            )

print("All PDFs have been processed. Press Enter to shutdown Weaviate.")
input()