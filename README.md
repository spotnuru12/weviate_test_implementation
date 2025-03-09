# weviate_test_implementation

steps to run 

1) Create & Activate a Virtual Environment (mac)
   
python3 -m venv venv
source venv/bin/activate

2) Install Dependencies
   
pip install -r requirements.txt

3) Insert Data into Weaviate
   
python3 manual_weaviate.py

4) Simple Query (Direct Retrieval)

python3

import weaviate
from weaviate.embedded import EmbeddedOptions

client = weaviate.Client(
    embedded_options=EmbeddedOptions(
        additional_env_vars={"ENABLE_MODULES": "ref2vec-centroid"}
    )
)

results = client.data_object.get(class_name="PDFInsights")
print(results)

5) Semantic Search with nearVector

import weaviate
from weaviate.embedded import EmbeddedOptions
from sentence_transformers import SentenceTransformer

# Re-initialize the client with minimal modules
client = weaviate.Client(
    embedded_options=EmbeddedOptions(
        additional_env_vars={"ENABLE_MODULES": "ref2vec-centroid"}
    )
)

# Suppose we search for the concept "contraceptives"
query_text = "contraceptives"

# Use the same embedding model as in manual_weaviate.py
model = SentenceTransformer("all-MiniLM-L6-v2")

# Encode our query into a vector
query_vector = model.encode(query_text).tolist()

# Perform a nearVector query on the PDFInsights class
search_results = (
    client.query
    .get("PDFInsights", ["text", "metadata"])
    .with_near_vector({"vector": query_vector})
    .with_limit(5)  # return the top 5 hits
    .do()
)

print(search_results)




