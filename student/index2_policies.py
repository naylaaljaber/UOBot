from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Document
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import os

print("LlamaIndex imported successfully!")

# Load all documents from the policies folder
documents = SimpleDirectoryReader(
    "/data/datasets/202105450/ollama/test/student/temp/policies", recursive=True
).load_data()

# === Function to split documents by '*' and prepend filename as context ===
def split_documents_with_context(documents):
    split_docs = []
    for doc in documents:
        # Use file name as a human-readable label (e.g., "General Policies")
        source_name = doc.metadata.get('file_name', 'Unknown').replace('_', ' ').replace('.txt', '').title()

        # Split based on '*'
        chunks = doc.text.split('*')

        for chunk in chunks:
            chunk = chunk.strip()
            if chunk:
                # Prepend label to text
                new_chunk_text = f"Policy Type: {source_name}\n{chunk}"

                # ✅ Add structured metadata for filtering
                doc_chunk = Document(
                    text=new_chunk_text,
                    metadata={"policy_type": source_name}
                )

                split_docs.append(doc_chunk)
    return split_docs

# Do the chunking
chunked_documents = split_documents_with_context(documents)

# Set the embedding model
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

# Build and save the index
index = VectorStoreIndex.from_documents(chunked_documents, embed_model=embed_model)
index.storage_context.persist(persist_dir="/scratch-beegfs/datasets/202105450/ollama/test/student/index2_policies")

print("✅ Indexing for policies with metadata completed successfully!")

