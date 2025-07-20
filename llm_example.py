import argparse
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler

def request_llm(message):
    llm = ChatOllama(
      model="gemma:7b",
      callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])                 
    )
    prompt = ChatPromptTemplate.from_template(
        """당신은 질문자의 친절한 안내자 뮤직이야.
        {message}에 대해서 간결하게 답변해줘.
        """
    )
    chain = prompt | llm
    return chain.invoke({"message": message})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", type=str, default="너의 이름은?")
    args = parser.parse_args()
    request_llm(args.m)
    # print(request_llm("안녕"))
