from langchain_community.document_loaders import PyPDFLoader
import os


def count_pages():
    # 現在のファイル（search.py）のディレクトリを基準に絶対パスを構築
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "..", "example_data", "nke-10k-2023.pdf")

    loader = PyPDFLoader(file_path)
    docs = loader.load()
    return len(docs)
