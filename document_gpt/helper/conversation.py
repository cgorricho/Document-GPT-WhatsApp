from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts.prompt import PromptTemplate

from config import config

def create_conversation() -> ConversationalRetrievalChain:

    persist_directory = config.DB_DIR

    embeddings = OpenAIEmbeddings(
        openai_api_key=config.OPENAI_API_KEY
    )

    db = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )

    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=False
    )

    _template = """
    Given the following conversation and a follow up question, \
    rephrase the follow up question to be a standalone question, \
    in its original language.

    If the chat history is empty, assume that you are starting \
    a brand new conversation with a new user.

    Chat History:
    {chat_history}

    Follow Up Input: {question}
    
    Standalone question:"""

    CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

    qa = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo"),
        chain_type='stuff',
        retriever=db.as_retriever(),
        memory=memory,
        get_chat_history=lambda h: h,
        condense_question_prompt=CONDENSE_QUESTION_PROMPT,
        condense_question_llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo'),
        verbose=False
    )

    return qa