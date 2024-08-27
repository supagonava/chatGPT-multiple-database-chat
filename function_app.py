import json
import azure.functions as func
import logging

from agent_executor import execute_user_message
from dotenv import load_dotenv

load_dotenv()

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="query_chat_api", methods=["POST"])
def query_chat_api(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body: dict = req.get_json()
        input_question = req_body.get("input_question")
        result_message = execute_user_message(input_question)
        return func.HttpResponse(body=json.dumps({"status": True, "message": result_message}), headers={"content-type": "application/json"})

    except Exception as e:
        return func.HttpResponse(status_code=500, body=json.dumps({"status": False, "message": str(e)}), headers={"content-type": "application/json"})
