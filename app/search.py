from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from .config import OPENAI_API_KEY
import os


def count_pages():
    # 現在のファイル（search.py）のディレクトリを基準に絶対パスを構築
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "..", "example_data", "nke-10k-2023.pdf")

    loader = PyPDFLoader(file_path)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, add_start_index=True
    )
    all_splits = text_splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-large", openai_api_key=OPENAI_API_KEY
    )

    vector_store = InMemoryVectorStore(embeddings)
    ids = vector_store.add_documents(documents=all_splits)

    results = vector_store.similarity_search(
        "How many distribution centers does Nike have in the US?"
    )

    print(results[0])

    return results
