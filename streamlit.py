
import streamlit as st
from read_db import gen_query
from read_db import fin_response
from read_db import gen_query_response
from read_db import checker
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain_community.utilities.sql_database import SQLDatabase

app_active = True

if app_active:

        from langchain_community.utilities.sql_database import SQLDatabase
        
        # snowflake_url = f"snowflake://{user}:{password}@{account}/{database}/{schema}?warehouse={warehouse}&role={role}"
        # db = SQLDatabase.from_uri(snowflake_url,sample_rows_in_table_info=1,include_tables=['financial_table'])
        # llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=st.secrets.OPENAI_API_KEY)
        
        
        import streamlit as st
        st.title("Snowflake Bot")
        
        description = "The table contains information about bus journeys, including the bus number, journey ID, start time, end time, card type used for payment, weekday of the journey, and revenue generated."
        
        st.write(description)
        
        st.write("<span style='color:blue'>BUS_NUMBER</span>: The 'BUS_NUMBER' column includes bus numbers 1-10 for different journeys.", unsafe_allow_html=True)
        st.write("<span style='color:blue'>JOURNEY_ID</span>: The 'JOURNEY_ID' column contains unique IDs for each journey.", unsafe_allow_html=True)
        st.write("<span style='color:blue'>START_TIME</span>: The 'START_TIME' column shows the time when the journey started.", unsafe_allow_html=True)
        st.write("<span style='color:blue'>END_TIME</span>: The 'END_TIME' column displays the time when the journey ended.", unsafe_allow_html=True)
        st.write("<span style='color:blue'>CARD_TYPE</span>: The 'CARD_TYPE' column indicates the type of card used for payment (Debit, Credit, or Prepaid).", unsafe_allow_html=True)
        st.write("<span style='color:blue'>WEEKDAY</span>: The 'WEEKDAY' column specifies the day of the week when the journey took place.", unsafe_allow_html=True)
        st.write("<span style='color:blue'>REVENUE</span>: The 'REVENUE' column shows the revenue generated from each journey in decimal format.", unsafe_allow_html=True)
        
        
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # React to user input
        if prompt := st.chat_input("go Bee..."):
            # Display user message in chat message container
            st.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
        
            # response = f"Echo: {prompt}"
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                query_response = gen_query(prompt)
                llm_response = gen_query_response(query_response)
                check =checker(prompt,query_response)
                response =fin_response(prompt,llm_response)
                    # st.write(query_response)
                st.markdown(response)
                # st.write(query_response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                # if check == "Yes":
                #     response =fin_response(prompt,llm_response)
                #     # st.write(query_response)
                #     st.markdown(response)
                #     # st.write(query_response)
                #     st.session_state.messages.append({"role": "assistant", "content": response})
                # else:
                #     st.write(check)
                # st.write(llm_res)
                # message["results"] =  gen_query_response(query_response)
                # st.dataframe(message["results"])
               
            # Add assistant response to chat history
            # st.session_state.messages.append({"role": "assistant", "content": response})

else:
    # Display an upgrade notice when the app is inactive
    st.error('🛠️ This chatbot is currently undergoing an upgrade and may be temporarily unavailable. Thank you for your patience.')




