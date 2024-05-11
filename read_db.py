import streamlit as st
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langsmith import traceable
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from operator import itemgetter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.chains import LLMChain



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



def gen_query(user_input):
    generate_query = create_sql_query_chain(llm, db)
    query = generate_query.invoke({"question": user_input})
    return query


def gen_query_response(query):
    execute_query = QuerySQLDataBaseTool(db=db)
    query_response = execute_query.invoke(query)
    
    # Assuming query_response is a list of tuples representing rows from the table
    if query_response:
        # Extract column names from the first row of the query response
        columns = [column[0] for column in query_response.description]
        
        # Initialize a dictionary with empty lists for each column
        table_dict = {column: [] for column in columns}
        
        # Populate the dictionary with values from the query response
        for row in query_response:
            for i, value in enumerate(row):
                table_dict[columns[i]].append(value)
        
        return table_dict
    else:
        return None


# def gen_query_response(query):
#     execute_query = QuerySQLDataBaseTool(db=db)
#     query_response = execute_query.invoke(query)
#     return query_response

def fin_response(a,b):
    prompt = (
    PromptTemplate.from_template("Given the following user question, corresponding {question}, and result  {SQL_result}, answer the user question.")
    
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    result =chain.run(question=a, SQL_result=b)
    return result

# template ="""Given the following user question, corresponding SQL query, and SQL result, answer the user question.
    
#         Question: {user_input}
#         SQL Query: {query}
#         SQL Result: {query_response}
#         Answer: """

# promt_template= PromptTemplate(
#     input_variable = ["user_input"],
#     template = template

# def gen_response(user_input):
#     query = gen_query(user_input)  # Generate query using user input
#     answer_prompt = PromptTemplate.from_template(
#         """Given the following user question, corresponding SQL query, and SQL result, answer the user question.
    
#         Question: {question}
#         SQL Query: {query}
#         SQL Result: {result}
#         Answer:"""
#     )
    
#     rephrase_answer = answer_prompt | llm | StrOutputParser()
    
#     chain = (
#         RunnablePassthrough.assign(query=query).assign(
#             result=itemgetter("query") | gen_query_response(query)
#         )
#         | rephrase_answer
#         )
    
#     response = chain.invoke({"question": user_input})  # Use user input here
#     return response







# def gen_query(input):
    
#     generate_query = create_sql_query_chain(llm, db)
#     query = generate_query.invoke({"question":input})
    
    
#     return query

# def gen_query_response(a):
#     execute_query = QuerySQLDataBaseTool(db=db)
#     query_response =execute_query.invoke(a)

#     return query_response

# def gen_response(query):
#     answer_prompt = PromptTemplate.from_template(
#         """Given the following user question, corresponding SQL query, and SQL result, answer the user question.
    
#         Question: {question}
#         SQL Query: {query}
#         SQL Result: {result}
#         Answer:"""
#     )
    
#     rephrase_answer = answer_prompt | llm | StrOutputParser()
    
#     chain = (
#         RunnablePassthrough.assign(query= gen_query(input)).assign(
#             result=itemgetter("query") | gen_query_response(query)
#         )
#         | rephrase_answer
#     )
    
#     response= chain.invoke({"question":userinput})
#     return  response
