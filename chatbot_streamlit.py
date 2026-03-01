import streamlit as st

from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load env variable ==> API key
load_dotenv()

# streamlit page setup
st.set_page_config(
    page_title="Chatbot.",
    page_icon="🤖",
    layout="centered"
)

st.title("💬 Generative AI chatbot.")

# Initiate chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Show chat history
for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.markdown(message["content"])

# Initiate llm
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.0
)

# user input box
user_prompt = st.chat_input("Ask Chatbot...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append(
        {"role": "user", "content": user_prompt}
    )

    # Inoke llm with user query
    response = llm.invoke(
        input = [
            {"role": "system", "content": "You are a helpful chat assistant."},
            *st.session_state.chat_history
        ]
    )

    assistant_response = response.content
    # add this response back to chat history
    st.session_state.chat_history.append(
        {"role": "assistant", "content": assistant_response}
    )

    # display response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)