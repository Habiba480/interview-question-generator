import time
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from prompt_template import build_prompt

llm = ChatOpenAI(
    base_url="http://0.0.0.0:1234/v1",
    model="meta-llama-3.1-8b-instruct",
    api_key="lm-studio"
)

def get_questions_from_llm(topic, placeholder):
    prompt = build_prompt(topic)
    full_response = ""
    response = llm([HumanMessage(content=prompt)]).content

    for char in response:
        full_response += char
        placeholder.code(full_response, language="markdown")
        time.sleep(0.005)

    placeholder.markdown(full_response, unsafe_allow_html=True)
    return full_response
