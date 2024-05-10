# %pip install snowflake-sqlalchemy
# %pip install snowflake
# %pip install --upgrade --quiet  snowflake-connector-python
# %pip install langchain_community
# %pip install langchain
# %pip install langchain_openai
# %pip install langsmith

OPENAI_API_TOKEN="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"

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


def gen_response():
    from langchain.chains import create_sql_query_chain
    from langchain_openai import ChatOpenAI
    from langsmith import traceable

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature = 1, openai_api_key=OPENAI_API_TOKEN)
    generate_query = create_sql_query_chain(llm,db)
    query = generate_query.invoke({"question":"which entity has the largest total deposit based on current year?"})

    return query