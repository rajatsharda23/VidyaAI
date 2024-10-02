from nemoguardrails import LLMRails, RailsConfig
from nemoguardrails.server.api import register_datastore
from nemoguardrails.server.datastore.memory_store import MemoryStore

register_datastore(MemoryStore())
    # This is the datastore to support threads for storing the conversation threads to retain context. Sends only the latest user messages(s) rather than entire history
    # We can register our own datastore and fine tune the code for our particular use case
    #To support this just add the "thread_id" in the body for the API call as a parameter like this->
    # {
    # "config_id": "config_1",
    # "thread_id": "1234567890123456",  
    # "messages": [{
    #   "role":"user",
    #   "content":"What is 7*9?"
    # }]
    # }


def init(app: LLMRails):
    # This module is loaded before initializing LLMRails
    # For time being nothing is needed to be done here
    print ("Config - module is loaded before initializing LLMRails")
    

