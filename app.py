import streamlit as st
from llama_index import load_index_from_storage, ServiceContext, StorageContext
from llama_index.llms import OpenAI
import openai
import os
from llama_index.embeddings import OpenAIEmbedding
from config_utils import get_api_key_from_config
from llama_index.memory import ChatMemoryBuffer

# Setting up the API key
api_key = get_api_key_from_config()
if not api_key:
    raise ValueError("API key not found in configuration file.")
os.environ["OPENAI_API_KEY"] = api_key
openai.api_key = os.environ["OPENAI_API_KEY"]

embed_model = OpenAIEmbedding(embed_batch_size=10)
llm = OpenAI(model="gpt-4", temperature=0.01)


# Load data function with caching
@st.cache(show_spinner=False, allow_output_mutation=True)
def load_data(persist_dir):
    with st.spinner(text="Loading saved embeddings"):
        service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)
        essay_index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=persist_dir),
            service_context=service_context,
        )
        return essay_index


# Get directory input from user
persist_dir = st.text_input("Enter the directory for embeddings:", "./embeddings/")

# Load data if the persist_dir is different from the stored one or if it doesn't exist in session_state yet
if "persist_dir" not in st.session_state or st.session_state.persist_dir != persist_dir:
    index = load_data(persist_dir)
    st.session_state.persist_dir = persist_dir
else:
    index = load_data(st.session_state.persist_dir)


if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
    memory = ChatMemoryBuffer.from_defaults(token_limit=2000)
    st.session_state.chat_engine = index.as_chat_engine(
        chat_mode="react",
        verbose=True,
        memory=memory,
        system_prompt=(
            "You are a chatbot with access to specific embedded documents. "
            "Use these documents, in combination with your expansive knowledge, to answer the user's questions. "
            "If the embedded documents don't contain relevant information for a particular query, state that explicitly "
            "and then provide an answer based on your own knowledge.\n"
            "Relevant documentation content from embedded documents: [Retrieved Document Snippet]\n"
            "User's question: [User's Current Question]"
        ),  # system_prompt is not used if the chat_mode is "react"
    )


if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me a question of your saved embeded pdfs",
        }
    ]
if prompt := st.chat_input(
    "Your question"
):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:  # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])


def clear_convo():
    st.session_state["past"] = []
    st.session_state["generated"] = []


# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)  # Add response to message history


def init():
    st.set_page_config(
        page_title="Chat embeded PDFs",
        page_icon="🧸",
        layout="centered",
        initial_sidebar_state="auto",
        menu_items=None,
    )


def reset_conversation():
    st.session_state.chat_engine.reset()


st.button("Reset Chat", on_click=reset_conversation)
