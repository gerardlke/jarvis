import json
from .llm import LLM

from .schemas.logger import Logger
from .schemas.action import Action
from .schemas.tools import TOOLS


class Controller:
    def __init__(self):
        self.llm = LLM()
        Logger.info("Pipeline", "Controller initialised.")

    def send_llm_request(self, prompt="", input={}):
        return self.llm.generate(
            system_prompt=prompt,
            user_input=input
        )
    
    def generate_action(self, input):
        return self.send_llm_request(
            prompt="""
You are a control agent.

Return ONLY valid JSON:
{
  "action": "<action_name>",
  "parameters": { ... }
}

If no tool is required, return:
{
  "action": "respond",
  "parameters": {}
}""",
            input=input
        )
    
    def generate_response(self, input):
        return self.send_llm_request(
            prompt="You are a helpful assistant. Converse.",
            input=input
        )
    
    def fallback_response(self, input):
        return self.send_llm_request(
            prompt="You are a helpful assistant but the user's requested action is not available.",
            input=input
        )
    
    def validate_action(self, action):
        try:
            parsed_json = json.loads(action)
            action = Action(**parsed_json)

            if action.action not in TOOLS:
                Logger.error("Controller", f"Action not allowed: {action.action}")
                return
            
            return action
            
        except Exception as e:
            Logger.error("Controller", f"Failed to validate {action} due to {e}")
        
    def execute_action(self, action):
        tool = TOOLS.get(action.action)
        if not tool:
            Logger.error("Controller", f"Tool not found for {action.action}")
            return
        
        try:
            Logger.info("Controller", f"Executing tool: {tool}")
            tool.execute()
        except Exception as e:
            Logger.error("Controller", f"Error executing {tool} tool: {e}")
    
    def run(self, input):
        Logger.info("Controller", f"Received user input: {input}")

        action = self.generate_action(input)
        action = self.validate_action(action)
        if not action:
            return self.fallback_response(input)
        
        Logger.info("Controller", f"Requested action: {action.action}")

        if action.action == "respond":
            return self.generate_response(input)

        return self.execute_action(action)