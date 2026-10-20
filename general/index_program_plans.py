from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Document
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import os

print("LlamaIndex imported successfully!")

# Load all documents from the program plans folder
documents = SimpleDirectoryReader("/data/datasets/202105450/ollama/test/general/documents/program_plans", recursive=True).load_data()

# === Function to split documents by '*' and prepend filename as context ===
def split_documents_with_context(documents):
    split_docs = []
    for doc in documents:
        # Use the file name (e.g., "network_engineering.txt") as a label
        source_name = doc.metadata.get('file_name', 'Unknown').replace('_', ' ').replace('.txt', '').title()

        # Split based on '*' as usual
        chunks = doc.text.split('*')

        for chunk in chunks:
            chunk = chunk.strip()
            if chunk:
                # Prepend context label to each chunk
                new_chunk_text = f"Program: {source_name}\n{chunk}"
                doc_chunk = Document(text=new_chunk_text)
                split_docs.append(doc_chunk)
    return split_docs

# Do the chunking
chunked_documents = split_documents_with_context(documents)

# Set the embedding model
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

# Build and save the index
index = VectorStoreIndex.from_documents(chunked_documents, embed_model=embed_model)
index.storage_context.persist(persist_dir="/scratch-beegfs/datasets/202105450/ollama/test/general/index_program_plans")

print("Indexing with context completed successfully!")

