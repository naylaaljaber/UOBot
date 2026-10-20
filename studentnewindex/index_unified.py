from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Document
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import os

print("✅ LlamaIndex imported successfully!")

# === Load all documents from the main folder (including subfolders) ===
documents = SimpleDirectoryReader(
    "/data/datasets/202105450/ollama/test/studentnewindex/documents", recursive=True
).load_data()

# === Function to split documents by '*' and prepend appropriate context ===
def split_documents_with_context(documents):
    split_docs = []
    for doc in documents:
        file_path = doc.metadata.get('file_path', '')
        file_name = doc.metadata.get('file_name', 'Unknown')
        base_name = file_name.replace('_', ' ').replace('.txt', '').title()

        # Determine category: program or policy
        if 'program_plans' in file_path:
            label = "Program"
            meta_key = "program"
        elif 'policies' in file_path:
            label = "Policy"
            meta_key = "policy"
        else:
            label = "Document"
            meta_key = "category"

        # Split by '*' and process chunks
        chunks = doc.text.split('*')
        for chunk in chunks:
            chunk = chunk.strip()
            if chunk:
                new_chunk_text = f"{label}: {base_name}\n{chunk}"
                doc_chunk = Document(
                    text=new_chunk_text,
                    metadata={meta_key: base_name}
                )
                split_docs.append(doc_chunk)
    return split_docs

# === Split and enrich documents ===
chunked_documents = split_documents_with_context(documents)
print(f"✅ Total chunks created: {len(chunked_documents)}")

# === Set the embedding model ===
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
print("✅ Embedding model loaded!")

# === Build and persist the index ===
index = VectorStoreIndex.from_documents(chunked_documents, embed_model=embed_model)
index.storage_context.persist(persist_dir="/scratch-beegfs/datasets/202105450/ollama/test/studentnewindex/index_unified")

print("🎉 Unified index built and saved successfully!")

