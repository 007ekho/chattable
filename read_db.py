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
database="BUS_DATA"
schema="PUBLIC"

from langchain_community.utilities.sql_database import SQLDatabase

snowflake_url = f"snowflake://{user}:{password}@{account}/{database}/{schema}?warehouse={warehouse}&role={role}"
db = SQLDatabase.from_uri(snowflake_url,sample_rows_in_table_info=1,include_tables=['bus_journey'])
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=st.secrets.OPENAI_API_KEY)
table_info =db.table_info


def gen_query(user_input):
    generate_query = create_sql_query_chain(llm, db)
    query = generate_query.invoke({"question": user_input})
    return query


def gen_query_response(query):
    execute_query = QuerySQLDataBaseTool(db=db)
    query_response = execute_query.invoke(query)
    return query_response


def fin_response(a, b):
    prompt = PromptTemplate.from_template("Given the following user question, corresponding {question}, and result {SQL_result}, give direct and polite answers the user question,avoid explaining too much. Do not answer any question outside of the information present in this table name bus_journey table")
    
    chain = LLMChain(llm=llm,prompt=prompt)
    result = chain.run(question=a, SQL_result=b)
    return result


from openai import OpenAI


def checker(query,user_input):
    prompt = hub.pull("ehi-123/chat_hallucination_blocker")
    llm = ChatOpenAI(model="gpt-4", temperature=0, api_key=OPENAI_API_TOKEN)
    chain = prompt | llm
    chain_call =chain.invoke(
        {
            "query": query,
            "user_input": user_input
        }
    )
    response_check =chain_call.content
    return response_check

# Initialize the OpenAI client
# client = OpenAI()

# def get_completion(prompt, user_input, result_list, client_instance, model="gpt-3.5-turbo"):
#     # Replace placeholders in the prompt with actual values
#     prompt = prompt.format(user_input=user_input, result_list=data_frame.to_dict())
#     messages= [{"role": "user", "content": prompt}]
#     # Create a completion
#     response =client_instance.chat.completions.create(
#         model=model,
        
#         messages= messages,
#         max_tokens=200,
#         temperature=0
#     )

#     return response.choices[0].message.content




# def fin_response(a, b):
#     prompt = PromptTemplate.from_template("""
#         You will be acting as an AI SQL Expert named Bee.
#         Your goal is to give correct, executable sql query to users.
#         You will be replying to users who will be confused if you don't respond in the character of Bee.
#         You are given one table, the table name is in financial_table.
#         The user will ask questions, for each question {question} you should respond  and include a sql query based on the question {question} and the table. 
        
#         {context}
        
#         Here are 6 critical rules for the interaction you must abide:
#         <rules>
        
#         1. If I don't tell you to find a limited set of results in the sql query or question, you MUST limit the number of responses to 10.
#         3. Text / string where clauses must be fuzzy match e.g ilike %keyword%
#         4. Make sure to generate a single snowflake sql code, not multiple. 
#         5. You should only use the table columns given , and the table given in <tableName>, you MUST NOT hallucinate about the table names
#         6. DO NOT put numerical at the very front of sql variable.
#         </rules>
        
#         Don't forget to use "ilike %keyword%" for fuzzy match queries (especially for variable_name column)
        
        
#         For each question from the user, make sure to include a query in your response.
        
#         Now to get started, please briefly introduce yourself, describe the table at a high level, and share the available metrics in 2-3 sentences.
#         Then provide 3 example questions using bullet points.
#         """")
    
#     chain = LLMChain(llm=llm,prompt=prompt)
#     result = chain.run(question=a, SQL_result=b)
#     return result










