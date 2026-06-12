# Save this inside: init_search.py
import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
)

# 1. Paste your exact Azure credentials here
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
INDEX_NAME = "unhinged-advice-index"

index_client = SearchIndexClient(endpoint=AZURE_SEARCH_ENDPOINT, credential=AzureKeyCredential(AZURE_SEARCH_KEY))

# 2. Create the Index Schema if it doesn't exist
if INDEX_NAME not in [index.name for index in index_client.list_indexes()]:
    index = SearchIndex(
        name=INDEX_NAME,
        fields=[
            SimpleField(name="id", type="Edm.String", key=True),
            SearchableField(name="mood", type="Edm.String", analyzer_name="en.microsoft"),
            SearchableField(name="advice", type="Edm.String", analyzer_name="en.microsoft"),
        ]
    )
    index_client.create_index(index)
    print(f"📦 Index '{INDEX_NAME}' created successfully on Azure!")

# 3. Add your actual knowledge base data here!
unhinged_knowledge_base = [
    {"id": "1", "mood": "Angry", "advice": "Go scream into a pillow, or better yet, reply to that email with pure corporate aggression. Let them feel the heat."},
    {"id": "2", "mood": "Sad", "advice": "Cry it out, then eat some ice cream for breakfast. Rules are social constructs anyway."},
    {"id": "3", "mood": "Anxious", "advice": "Overthinking is just a sign your brain is working at 400% capacity. Channel that chaos into cleaning your room at 2 AM."},
]

search_client = SearchClient(endpoint=AZURE_SEARCH_ENDPOINT, index_name=INDEX_NAME, credential=AzureKeyCredential(AZURE_SEARCH_KEY))
search_client.upload_documents(documents=unhinged_knowledge_base)
print("✅ All your chaotic advice has been uploaded to Microsoft Foundry IQ backend!")