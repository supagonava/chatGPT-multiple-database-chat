# Sub Agent
import glob, os, json
from dotenv import load_dotenv

load_dotenv()

# Step convert human message to sql statement
import pandas as pd
from typing import Literal
from services.chatgpt_connection import ChatGPTConnection
from services.sqlite_connection import SQLiteConnection
from services.postgresql_connection import PostgreSQLConnection


def execute_user_message(input_question: str):

    DB_MAPPER: dict[str, SQLiteConnection, PostgreSQLConnection] = {
        "chinook-db-agent": SQLiteConnection(
            os.environ.get("SQLITE_DB_PATH", "database/chinook.db"),
        ),
        "northwind-db-agent": PostgreSQLConnection(
            db_name=os.environ.get("POSTGRES_DB_NAME", "northwind"),
            user=os.environ.get("POSTGRES_USER", "postgres"),
            password=os.environ.get("POSTGRES_PASSWORD", "postgres"),
            host=os.environ.get("POSTGRES_HOST", "localhost"),
            port=5432,
        ),
    }

    sub_agents: list[dict] = []
    for json_file in glob.glob("agents/*.json"):
        sub_agent_config: dict = json.loads(open(json_file, "r", encoding="utf-8").read())
        # set prompt from txt file
        if sub_agent_config.get("prompt_file_path") and sub_agent_config.get("sql_schema_path"):
            txt_structure_sql = open(sub_agent_config["sql_schema_path"], "r", encoding="utf-8").read()
            sub_agent_config["prompt"] = open(
                str(sub_agent_config.get("prompt_file_path")),
                "r",
                encoding="utf-8",
            ).read()

            sub_agent_config["prompt"] = str(sub_agent_config["prompt"]).format(db_structure_txt=txt_structure_sql)
            sub_agents.append(sub_agent_config)
    sub_agents

    def convert_query_result_to_human_message(user_question: str, sql_statement: str, query_records: list, excel_path: str):
        sql_to_human_client_agent: ChatGPTConnection = ChatGPTConnection(
            api_key=os.environ.get("AZURE_OPENAI_KEY"),
            api_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
            api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
            model="gpt-4o-mini",
            system_role=open("prompts/convert_query_records_to_human.txt", "r", encoding="utf-8").read(),
            output_structure={
                "human_message": "text",
            },
        )

        user_prompt = """
        User Question : {user_question}
        SQL Statment : {sql_statement}
        Query Result : {query_records}
        Excel Path : {excel_path}
        You : """

        # if len(query_records) > 10:
        #     query_records = str(query_records[0:10]) + ".. {} records left.".format(len(query_records) - 10)

        final_prompt = user_prompt.format(
            user_question=user_question,
            sql_statement=sql_statement,
            query_records=str(query_records),
            excel_path=excel_path,
        )
        # print(final_prompt)

        result_human = sql_to_human_client_agent.query_chat(prompt=final_prompt)
        return result_human["human_message"]

    def chat_with_agent(agent_name=sub_agents[0]["agent_name"], input_message: str = ""):

        use_agents: list[dict] = [s for s in sub_agents if s["agent_name"] == agent_name]
        use_agent: dict = None
        if use_agents:
            use_agent = use_agents[0]

        client_agent = ChatGPTConnection(
            api_key=os.environ.get("AZURE_OPENAI_KEY"),
            api_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
            api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
            model="gpt-4o-mini",
            system_role=use_agent.get("prompt"),
            output_structure={
                "sql_statement": "text (only query statement without comments)",
            },
        )
        generate_sql_result = client_agent.query_chat(input_message)

        db_executor = DB_MAPPER[agent_name]
        db_executor.connect()
        # print("## Step 1 Generate Statement >>", generate_sql_result["sql_statement"])

        query_records = db_executor.fetch_all(query=generate_sql_result["sql_statement"])

        # >>>> What if need export excel file
        # query_records_pd = pd.DataFrame(query_records)
        # excel_path = "assets/{}.xlsx".format(input_message)
        # query_records_pd.to_excel(excel_path)

        # print("## Step 2 Query result >>", query_records)

        # print("## Step 3 Human Pretty Message >>")
        return_human_message = convert_query_result_to_human_message(
            user_question=input_message,
            sql_statement=generate_sql_result["sql_statement"],
            query_records=query_records,
            excel_path=None,
        )
        return return_human_message

    core_prompt = open("prompts/core.txt", "r").read()
    interact_with_agents = ""
    for idx, s_agent in enumerate(sub_agents):
        interact_with_agents += "[{idx}] Agent Name : `{agent_name}`, JobDescription : `{description}`\n".format(
            idx=idx,
            agent_name=s_agent["agent_name"],
            description=s_agent["description"],
        )
    # print(core_prompt.format(interact_with_agents=interact_with_agents))

    user_question = input_question
    # === Step 1
    prompt_list_query_message_to_agent_task = core_prompt.format(interact_with_agents=interact_with_agents)
    create_list_todo_client_agent = ChatGPTConnection(
        api_key=os.environ.get("AZURE_OPENAI_KEY"),
        api_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
        model="gpt-4o-mini",
        system_role=prompt_list_query_message_to_agent_task,
        output_structure={
            "todo_tasks": "list[dict] \{'agent_name':'str', 'question_to_agent':'str'\}",
        },
    )
    todo_tasks = create_list_todo_client_agent.query_chat(user_question)
    todo_tasks["todo_tasks"]

    prev_row = None
    query_result = None
    for idx, item_task in enumerate(todo_tasks["todo_tasks"]):
        print(idx, "----")
        user_q = item_task["question_to_agent"]
        agent_name = item_task["agent_name"]
        if prev_row is None:
            query_result = chat_with_agent(agent_name=agent_name, input_message=user_q)
            prev_row = """
            Base Question: {input_question}.
            
            {agent_name}: {query_result}
            """.format(
                input_question=input_question,
                agent_name=agent_name,
                query_result=query_result,
            )

        else:
            query_result = chat_with_agent(
                agent_name=agent_name,
                input_message="{prev_row}\n{user_q}".format(
                    prev_row=prev_row,
                    user_q=user_q,
                ),
            )
            prev_row = "{prev_row}\n{agent_name}: {query_result}".format(prev_row=prev_row, agent_name=agent_name, query_result=query_result)

        print(prev_row)

    return query_result
