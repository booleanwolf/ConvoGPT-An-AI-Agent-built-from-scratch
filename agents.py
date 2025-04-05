from openai import OpenAI
from prompt import Prompt

client_llm = OpenAI()


class MemoryAgent():
    def __init__(self):
        self.model = "gpt-4o-mini"
        self.max_completion_length = 1000
        self.system_prompt =  Prompt.MEMORY_AGENT
    
    def generate_memory_plan(self, text):
        self.messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"{text}\n\n."}
            ]
        
        response = client_llm.chat.completions.create(
            model="gpt-4o",
            messages=self.messages,
            temperature=0.3,
            max_tokens=self.max_completion_length,
            top_p=0.4,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            response_format={ "type": "json_object" }
        )

        return response.choices[0].message.content


class WifeyAgent():
    def __init__(self):
        self.model = "gpt-4o-mini"
        self.max_completion_length = 1000
        self.system_prompts = Prompt.WIFEY_AGENT
        
        chat_history.add_dq("system", Prompt.WIFEY_AGENT)
    
    def run(self, text):
        chat_history.add_dq("user", text) 

        self.messages = chat_history.as_prompt_message() 
        # print(self.messages)

        # self.messages = [
        #         {"role": "system", "content": self.system_prompts},
        #         {"role": "user", "content": f"{text}\n\n."}
        #     ]

        response = client_llm.chat.completions.create(
            model="gpt-4o",
            messages=self.messages,
            temperature=0.3,
            max_tokens=self.max_completion_length,
            top_p=0.4,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            response_format={ "type": "json_object" }
        )

        return response.choices[0].message.content
