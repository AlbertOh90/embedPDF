import os
import openai
import argparse
from llama_index.embeddings import OpenAIEmbedding
from llama_index import (
    ServiceContext,
    SimpleDirectoryReader,
    VectorStoreIndex,
)
from config_utils import get_api_key_from_config

CONFIG_FILE = "config.txt"
EMBED_BATCH_SIZE = 10


def setup_openai_api():
    """
    Set up the OpenAI API using the key from configuration or environment variable.
    """
    api_key = get_api_key_from_config() or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "API key not found in configuration file or environment variables."
        )
    openai.api_key = api_key


def pdf_to_index(pdf_repo, persist_dir):
    """
    Index PDFs from a given directory and save the embeddings to another directory.

    :param pdf_repo: Directory containing the PDFs.
    :param persist_dir: Directory to save the embeddings.
    """
    documents = SimpleDirectoryReader(pdf_repo).load_data()
    setup_openai_api()
    embed_model = OpenAIEmbedding(embed_batch_size=EMBED_BATCH_SIZE)
    service_context = ServiceContext.from_defaults(embed_model=embed_model)
    index = VectorStoreIndex.from_documents(documents, service_context=service_context)
    index.storage_context.persist(persist_dir=persist_dir)
    print(f"Embeddings saved to disk at {persist_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Embed PDFs into an index and save to disk."
    )
    parser.add_argument("pdf_repo", type=str, help="Directory containing the PDFs.")
    parser.add_argument("save_dir", type=str, help="Directory to save the embeddings.")
    args = parser.parse_args()

    pdf_to_index(args.pdf_repo, args.save_dir)


if __name__ == "__main__":
    main()
