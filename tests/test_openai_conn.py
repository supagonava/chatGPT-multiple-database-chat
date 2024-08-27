import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from services.chatgpt_connection import ChatGPTConnection
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    agent = ChatGPTConnection(
        api_key=os.environ.get("AZURE_OPENAI_KEY"),
        api_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
        model="gpt-4o-mini",
        output_structure={"result": "str", "reason": "str"},
        system_role="You are ai assistant to question user message.",
    )
    result_message = agent.query_chat(prompt="มือถือยี่ห้ออะไรที่มีแอป IMessage")
    print("Brand {}, Reason {}".format(result_message.get("result"), result_message.get("reason")))
