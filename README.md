# weviate_test_implementation

steps to run 

1.) create ve:

python3 -m venv venv
source venv/bin/activate

2.)

pip install -r requirements.txt

3.)

python3 manual_weaviate.py

4.) test query:

python3

5.) 

import weaviate
from weaviate.embedded import EmbeddedOptions

client = weaviate.Client(
    embedded_options=EmbeddedOptions(
        additional_env_vars={"ENABLE_MODULES": "ref2vec-centroid"}
    )
)

results = client.data_object.get(class_name="PDFInsights")
print(results)




