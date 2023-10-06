# EmbedPDF

EmbedPDF is for those who don't have access to a GPU and can't perform fine-tuning but want to utilize the power of the OpenAI API to chat with their PDFs. With this tool, users can generate and save embeddings for their PDFs using OpenAI's `text-embedding-ada-002` model and then use the `GPT-4` API to query these embeddings. 

## Note

Once you create embeddings with the create_embeds.py script, you won't have to repeat this unless you change the PDFs in your collection. This helps save on API costs. When starting the Streamlit chat, just point to the directory of the embedding directory you want. You can also change the embedding directory in the middle of the chat.

## Chat Functionality

When chatting with EmbedPDF, the chat will first attempt to find relevant content from the embedded PDFs based on your query. If a match is found within the embeddings, the chat will provide a response based on that content. If the content isn't found within the embedded PDFs, the chat will revert to a standard ChatGPT response, ensuring that you always get a relevant answer.

## Prerequisites

- OpenAI API key.

## Getting Started

1. Clone the EmbedPDF repository to your local machine.
   
   ```
   git clone <repository-url>
   cd EmbedPDF
   ```

2. Create and activate a virtual environment:

   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the necessary dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Store your OpenAI API key in a `config.txt` file in the format: `OPENAI_API_KEY=your_openai_api_key_here`. 

5. Put your desired PDFs in a targeted folder.

6. Generate embeddings for your PDFs:

   ```
   python3 create_embeds.py [path_to_pdfs] [path_to_embeddings]
   ```

7. To chat with your embedded PDFs, run:

   ```
   streamlit run app.py
   ```

