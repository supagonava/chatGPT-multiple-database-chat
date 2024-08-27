import json
import os
from typing import Literal
import json5
import openai
from openai import OpenAI, AzureOpenAI
import requests


class ChatGPTConnection:

    def __init__(
        self,
        api_key: str = os.environ.get("AZURE_OPENAI_ENDPOINT"),
        api_endpoint: str = os.environ.get("AZURE_OPENAI_KEY"),
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
        system_role: str = "You are a helpful assistant.",
        output_structure: dict = None,
        model: Literal["gpt-4o", "gpt-4o-mini"] = "gpt-4o-mini",
    ):
        """Initialize the ChatGPT service with the API key, system role, and output structure."""
        self.api_key = api_key
        self.api_version = api_version
        self.api_endoint = api_endpoint
        self.model = model
        self.system_role = system_role
        self.output_structure = output_structure or {}
        if self.output_structure:
            self.system_role += "\nYou will response only below json schema.\n{}".format(
                json5.dumps(output_structure, ensure_ascii=False, indent=2),
            )
        self.open_ai_client: AzureOpenAI = AzureOpenAI(api_key=api_key, base_url=api_endpoint, api_version=api_version)

    def query_chat(self, prompt: str) -> dict:
        """Send a query to ChatGPT and return the response."""
        try:
            response = self.open_ai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_role},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=4096 if self.model == "gpt-4o" else 16384,
                temperature=0,
            )
            response_message = response.choices[0].message.content
            response_message_json_first = response_message.find("{")
            response_message_json_last = response_message.rfind("}")
            json_message = response_message[response_message_json_first : response_message_json_last + 1]
            return json.loads(json_message)
        except openai.OpenAIError as e:
            print(f"Error querying ChatGPT: {e}")
            raise

    def parse_to_json(self, response: dict) -> dict:
        """Parse the ChatGPT response to a JSON format, verifying against the expected output structure."""
        try:
            content = response["choices"][0]["message"]["content"]
            parsed_data = json5.loads(content)

            # Validate the parsed JSON against the expected output structure
            if not self._validate_structure(parsed_data):
                raise ValueError("Parsed JSON does not match the expected output structure.")

            return parsed_data
        except (json.JSONDecodeError, KeyError, IndexError, ValueError) as e:
            print(f"Error parsing response to JSON: {e}")
            raise

    def _validate_structure(self, data: dict) -> bool:
        """Validate the parsed JSON data against the expected output structure."""
        for key, expected_type in self.output_structure.items():
            if key not in data or not isinstance(data[key], expected_type):
                print(f"Validation error: Key '{key}' is missing or not of type '{expected_type.__name__}'")
                return False
        return True
