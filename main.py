import chainlit as cl
from chainlit.playground.providers.openai import ChatOpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import Runnable, RunnablePassthrough
from langchain.schema.runnable.config import RunnableConfig
from langchain.utilities import SQLDatabase

# Set up database and openai client
path_biz = "sqlite:///./db/chinook"
path_music = "sqlite:///./db/chinookv2.db"

@cl.cache
def setup_database(path):
    return SQLDatabase.from_uri(path)

# Setup database
db = setup_database(path=path_music)

def get_schema(self):
    return db.get_table_info()

def run_query(query):
    return db.run(query)

@cl.on_chat_start
async def on_chat_start():
    model = ChatOpenAI(streaming=True)
    template_query = """Based on the table schema below, write a SQL query that would answer the user's question:
        {schema}

        Question: {question}
        SQL Query:"""
    
    template_response = """Based on the table schema below, question, sql query, and sql response, write a natural language response:
            {schema}
            
            Question: {question}
            SQL Query: {query}
            SQL Response: {response}"""
    
    prompt_query = ChatPromptTemplate.from_template(template_query)
    prompt_response = ChatPromptTemplate.from_template(template_response)
    
    sql_response = (
    RunnablePassthrough.assign(schema=get_schema)
    | prompt_query
    | model.bind(stop=["\nSQLResult:"])
    | StrOutputParser())
    
    full_chain = (
    RunnablePassthrough.assign(query=sql_response)
    | RunnablePassthrough.assign(
        schema=get_schema,
        response=lambda x: db.run(x["query"]),
    )| prompt_response| model| StrOutputParser())
    
    cl.user_session.set("runnable", full_chain)


@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")  # type: Runnable

    msg = cl.Message(content="")

    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler(stream_final_answer=True)]),
    ):
        await msg.stream_token(chunk)

    await msg.send()
