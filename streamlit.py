
import streamlit as st
from read_db import gen_query
from read_db import fin_response
from read_db import gen_query_response
from langchain_openai import ChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase

user = "EHI007"
password = "Worker/123"
warehouse = "COMPUTE_WH"
role = "ACCOUNTADMIN"
account = "vwwhgvg-aw51783"
database="FROSTY_SAMPLE"
schema="CYBERSYN_FINANCIAL"

from langchain_community.utilities.sql_database import SQLDatabase

snowflake_url = f"snowflake://{user}:{password}@{account}/{database}/{schema}?warehouse={warehouse}&role={role}"
db = SQLDatabase.from_uri(snowflake_url,sample_rows_in_table_info=1,include_tables=['financial_table'])
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=st.secrets.OPENAI_API_KEY)

st.title("Welcome to your chatbot")


# snowflake_url = f"snowflake://{user}:{password}@{account}/{database}/{schema}?warehouse={warehouse}&role={role}"
# db = SQLDatabase.from_uri(snowflake_url,sample_rows_in_table_info=1,include_tables=['financial_table'])
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=st.secrets.OPENAI_API_KEY)

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
        llm_response = gen_query_response(query_response)
        llm_res =fin_response(user_prompt,llm_response)
        
        st.write(llm_res)

    st.session_state.messages.append({"role": "assistant", "content": llm_response})

