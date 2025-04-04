from qdrant_client import QdrantClient, models
from dotenv import load_dotenv 
import os 
from openai import OpenAI
from prompt import Prompt
import json 
from datetime import datetime 
from collections import deque
import time 

load_dotenv()
import sys

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

RESET = '\033[0m'
BLACK = "\u001b[30m"
RED = "\u001b[31m"
GREEN = "\u001b[32m"
BRIGHT_GREEN = "\u001b[92m"
YELLOW = "\u001b[33m"
BLUE = "\u001b[34m"
MAGENTA = "\u001b[35m"
CYAN = "\u001b[36m"
WHITE = "\u001b[37m"

def debug_print(text):
    print(f"DEBUG LOG: {text}")

def log_print(text):
    print(f"{BLUE}\033[3m{text}\033[0m") 



URL = os.getenv("QUADRANT_URL")
API = os.getenv("QUADRANT_API")

client_db = QdrantClient(
    url=URL, 
    api_key=API,
)

client_llm = OpenAI()

class VectorDatabase:
    def __init__(self):
        self.embedding_model= "text-embedding-3-small"

        if not client_db.collection_exists(collection_name="semantic_collection"):
            semantic_collection = client_db.create_collection(
                collection_name="semantic_collection",
                vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
            )

        if not client_db.collection_exists(collection_name="episodic_collection"):
            episodic_collection = client_db.create_collection(
                collection_name="episodic_collection",
                vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
            )

        if not client_db.collection_exists(collection_name="procedural_collection"):
            procedural_collection = client_db.create_collection(
                collection_name="procedural_collection",
                vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
            )

    def embed(self, text):
        embed = client_llm.embeddings.create(
            input=text,
            model=self.embedding_model
        ) 

        return embed.data[0].embedding
    
    def save_semantic_memory(self, text):
        vector = self.embed(text)
        now_time = datetime.now()
        now_time = int(now_time.strftime('%Y%m%d%H%M%S'))

        client_db.upsert(
        collection_name="semantic_collection",
        points=[
            models.PointStruct(
                id=now_time,
                payload={
                        "message": text, 
                        },
                        vector=vector,  
                ),
            ],
        )
        log_print(f"Semantic Memory Saved: {text}")
        # debug_print("Semantic Memory Saved!")

    def save_procedural_memory(self, text):
        vector = self.embed(text)

        client_db.upsert(
        collection_name="procedural_collection",
        points=[
            models.PointStruct(
                id=1,
                payload={
                        "message": text, 
                        },
                        vector=vector,  
                ),
            ],
        )
        log_print(f"Procedural Memory Saved: {text}")
        # debug_print("Procedural Memory Saved!")

    def save_episodic_memory(self, text):
        vector = self.embed(text)

        client_db.upsert(
        collection_name="episodic_collection",
        points=[
            models.PointStruct(
                id=1,
                payload={
                        "message": text, 
                        },
                        vector=vector,  
                ),
            ],
        )
        log_print(f"Episodic Memory Saved: {text}")
        # debug_print("Episodic Memory Saved!")
    
    def search_semantic_memory(self, query):
        emb = self.embed(query)

        info = client_db.search(
            collection_name="semantic_collection",
            # query_filter=models.Filter(
            #     must=[
            #         models.FieldCondition(
            #             key="message",
            #             match=models.MatchValue(
            #                 value=query,
            #             ),
            #         )
            #     ]
            # ),
            query_vector=emb,
            limit=1,
        ) 

        # debug_print(info[0].payload['message'])

        if info:
            return info[0].payload['message']

    
    def search_episodic_memory(self, query):
        emb = self.embed(query)

        info = client_db.search(
            collection_name="episodic_collection",
            # query_filter=models.Filter(
            #     must=[
            #         models.FieldCondition(
            #             key="message",
            #             match=models.MatchValue(
            #                 value=query,
            #             ),
            #         )
            #     ]
            # ),
            query_vector=emb,
            limit=1,
        ) 

        # debug_print(info[0].payload['message'])

        if info:
            return info[0].payload['message'] 

    def search_procedural_memory(self, query):
        emb = self.embed(query)

        info = client_db.search(
            collection_name="procedural_collection",
            # query_filter=models.Filter(
            #     must=[
            #         models.FieldCondition(
            #             key="message",
            #             match=models.MatchValue(
            #                 value=query,
            #             ),
            #         )
            #     ]
            # ),
            query_vector=emb,
            limit=1,
        ) 

        # debug_print(info[0].payload['message'])

        if info:
            return info[0].payload['message']



class MemoryToolExecutor():
    def __init__(self):
        self.instance = database

    def execute_method(self, method_name, *args, **kwargs):
        # Get the method from the instance using getattr()
        method = getattr(self.instance, method_name, None)

        # Check if the method exists and is callable
        if method and callable(method):
            return method(*args, **kwargs)
        else:
            raise ValueError(f"Method '{method_name}' not found or is not callable on the instance.")
    
    def execute_memory_plan(self, tools_response):
        if "tools" in tools_response:
            data_json = json.loads(tools_response)

            searched_info = ""

            for tool in data_json["tools"]:
                # Parse the function name and arguments
                function_name = tool.split('(')[0]
                arguments = tool.split('(')[1].split(')')[0].strip("'")

                # debug_print(f"Executing {function_name} with {arguments}")
                
                # Call execute_method
                if "search" in function_name:
                    info = self.execute_method(function_name, arguments)
                    # print("SEARCG INFO")    # print(info)
                    if info:
                        if type(info) == str:
                            searched_info += f"{info} "
                        else:
                            for i in info:
                                searched_info += i
                                searched_info += " "
                else:
                    self.execute_method(function_name, [arguments])
            
            return searched_info

class ChatQueue():
    def __init__(self):
        self.dq = deque(maxlen=50)
    
    def add_dq(self, user, text):
        if len(self.dq) == self.dq.maxlen: 
            self.dq.remove(self.dq[1]) 
        self.dq.append({"role" : user, "content": text}) 
    
    def stringify(self):
        return " ".join(self.dq)
    
    def as_prompt_message(self):
        msg = []
        for elem in self.dq:
            msg.append(elem) 
        return msg 

      
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

class WifeyTool():
    def __init__(self):
        pass 

    def Speak(self, text):
        chat_history.add_dq("assistant", text[0])
        print(f"{GREEN}Wifey: {text[0]}{WHITE}")
         

    def Think(self, t):
        time.sleep(float(t[0])/1000)
        print(f"{CYAN}Wifey Thinking...{WHITE}")

    def BJ(self, t):
        time.sleep(0.5)
        chat_history.add_dq("assistant", "Gave BJ")
        print(f"{GREEN}Wifey Giving BJ...{WHITE}")
        time.sleep(1.5)
         

    def ShowBoobs(self, t):
        time.sleep(0.5)
        chat_history.add_dq("assistant", "Showed Boobs")
        print(f"{BRIGHT_GREEN}Wifey showing boobos...{WHITE}")
        time.sleep(1.5)
         

    def Wait(self, t):
        # print(f"{CYAN}Waiting...{WHITE}") 
        # debug_print(int(t[0]))
        time.sleep(float(t[0])/1000)

    
class WifeyToolExecutor():
    def __init__(self):
        self.instance = WifeyTool()
    
    def execute_method(self, method_name, *args, **kwargs):
        # Get the method from the instance using getattr()
        method = getattr(self.instance, method_name, None)

        # Check if the method exists and is callable
        if method and callable(method):
            return method(*args, **kwargs)
        else:
            raise ValueError(f"Method '{method_name}' not found or is not callable on the instance.")
    
    def execute_wifey_plan(self, tools_response):
        if "tools" in tools_response:
            data_json = json.loads(tools_response)

            for tool in data_json["tools"]:
                # Parse the function name and arguments
                function_name = tool.split('(')[0]
                arguments = tool.split('(')[1].split(')')[0].strip("'")
                
                self.execute_method(function_name, [arguments])
            
         
        
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


        
if __name__ == "__main__":
    # print("\033[3mThis text is in italics\033[0m")
    # print(f"{GREEN}This is red text{WHITE}")

    # exit()
    chat_history = ChatQueue()
    database = VectorDatabase() 
    mem = MemoryAgent()
    executor = MemoryToolExecutor()
    wife = WifeyAgent()
    wife_executor = WifeyToolExecutor() 

    
    

    # print(client_db.get_collections())
    while True:
        
        chat = input("You: ")
        response = mem.generate_memory_plan(chat)
        memory_info = executor.execute_memory_plan(response)
        # debug_print(f"{memory_info}")
        wife_chat = f"Tamim: {chat}\n Previous Memory: {memory_info}"
        
        response = wife.run(wife_chat)
        # print(response) 
        wife_executor.execute_wifey_plan(response)


    # print(type(response)) 
    # print(response)
    # data_json = json.loads(response)
    
    


    # database.save_semantic_memory("I like chubby girls with big boobs")
    # database.search_semantic_memory("What kind of girl i like?")