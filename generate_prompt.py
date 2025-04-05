from main import WifeyTool 
import inspect

MEMORY_AGENT = """You are a memory agent. Your job is to provide a proper plan to store the information. Only output the json of planned tools.
        1. Actively use memory tools [save_semantic_memory(text), save_episodic_memory(text), save_procedural_memory(text), search_semantic_memory(text), search_episodic_memory(text), search_procedural_memory(text)]

        {your_prompt_here}
        }"""

def extract_methods_in_format(cls):
    formatted_methods = []
    
    for name, obj in inspect.getmembers(cls):
        if inspect.isfunction(obj):
            # Get the signature of the function (method)
            signature = inspect.signature(obj)
            # Extract the arguments (excluding 'self')
            args = [param for param in signature.parameters.values() if param.name != 'self']
            # Create the formatted string "MethodName(arg1, arg2)"
            formatted_method = f"{name}({', '.join(arg.name for arg in args)})"
            formatted_methods.append(formatted_method)
    
    return formatted_methods



formatted_methods = extract_methods_in_format(WifeyTool)


WIFEY_AGENT = f"_your_prompt_here__. Tools: {formatted_methods} You will output a json format of tools. Your message will be passed as argument to given tools. "

print(f"Copy and paste the following into prompt.py...")
print("MEMORY AGENT: ")
print("----------------------------------------------------------")
print(MEMORY_AGENT)
print("----------------------------------------------------------")
print("WIFEY AGENT: ")
print("----------------------------------------------------------")
print(WIFEY_AGENT)
print("----------------------------------------------------------")