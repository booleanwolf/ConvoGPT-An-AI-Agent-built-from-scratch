import json 

class MemoryToolExecutor():
    def __init__(self, database):
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

    
class WifeyToolExecutor():
    def __init__(self, tools):
        self.instance = tools
    
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
            