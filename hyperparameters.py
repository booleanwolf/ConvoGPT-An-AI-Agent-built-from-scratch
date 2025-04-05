class Param:
    embedding_model = "text-embedding-3-small"
    embedding_size = 1536 
    memory_model = "gpt-4o"
    memory_MAX_COMPLETION_LENGTH = 1000
    wife_model = "gpt-4o"
    wife_MAX_COMPLETION_LENGTH = 1000 
    memory_TEMPERATURE = 0.3 
    wife_TEMPERATURE = 0.3 
    memory_topP = 0.4 
    wife_topP = 0.4 
    frequency_penalty = 0.0
    presence_penalty = 0.0 