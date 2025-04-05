# ConvoGPT - An AI Agent Built from Scratch with Memory Planner and Action Planner

ConvoGPT is an AI agent built from scratch, capable of handling custom tasks and responding to user prompts in an intelligent way. The agent is designed to be highly modular, allowing for easy addition of new tools and features.
The implementation is really simple. More things could have been done. 

Agent has 3 types of memories:

1. Semantic Memory: facts about the user. Like username, address, personal preference like favourite color, food etc. Personal information like the institution user is studying, company he is doing job etc.
2. Episodic Memory: User's preference of your response, for example: You elaborate much about a topic but user wants it brief. Then you store this preference of user in episodic memory
3. Procedural Memory: Procedure of any action or work explained by the user.


## Setup Instructions

Follow the instructions below to set up and run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ConvoGPT-An-AI-Agent-built-from-scratch.git
cd ConvoGPT-An-AI-Agent-built-from-scratch
```

### 2. Install Dependencies 

```bash
pip install -r requirements.txt
```
### 3.  Generating the Prompt Template

```bash
python generate_template.py
```
### 4. Adding a Tool
To add a new tool to the AI agent:

Modify the WifeyTool() class in main.py by adding your new tool logic.

After modifying the tool, re-run the template generation process to update prompt.py with the new tool variables.

```bash
python generate_template.py
```
Copy the updated variables and paste them into prompt.py again.

### 5. Running the Agent
Once everything is set up, you can run the agent using:

```bash
python main.py
```

Thank you! 
