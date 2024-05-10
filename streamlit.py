
import streamlit as st
from read_db import gen_query
from read_db import gen_response
st.title("Welcome to your chatbot")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello there, how can I help you today?"}]

# Display messages
for message in st.session_state.messages:
    with st.container():
        st.write(f"{message['role'].capitalize()}: {message['content']}")

# User input
user_prompt = st.text_input("You:", "")

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Generate response if user input is not empty
    with st.spinner("Assistant is thinking..."):
        query_response = gen_query(user_prompt)
        llm_response = gen_response(query_response)
        
        st.write(llm_response)

    st.session_state.messages.append({"role": "assistant", "content": llm_response})

