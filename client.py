import os
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential, TokenCredential
from azure.identity import DefaultAzureCredential
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.search.documents import SearchClient

# Load environment variables from .env file
load_dotenv()

# Get endpoint and API key from environment variables
endpoint = os.getenv("endpoint")
api_key = os.getenv("api_key")
grok_model = os.getenv("grok_model", "grok-3-mini")
deep_seek_model = os.getenv("deep_seek_model", "DeepSeek-R1")
ai_search_url = os.getenv("ai_search_url")
ai_index_name = os.getenv("ai_index_name")
ai_semantic_config = os.getenv("ai_semantic_config", "default")
ai_search_key = os.getenv("ai_search_key")

# model=grok_model
model=deep_seek_model


sys_prompt =  """
You are an AI Assistant tasked with helping the users of Contoso Gaming with their queries

Refer to the context provided before answering the question
If the provided context is insufficient to answer the question, state so
**DO NOT MAKE STUFF UP**
"""

def perform_search_based_qna(query):
    print("Calling Azure Search for query: ", query)
    search_response = None

    # The following code uses AzureKeyCredential to authenticate the SearchClient.
    # credential = AzureKeyCredential(ai_search_key)
    # search_client = SearchClient(endpoint=ai_search_url,
    #                   index_name=ai_index_name,
    #                   credential=credential)

    # results = search_client.search(
    #     search_text=query, 
    #     query_type="semantic",
    #     semantic_configuration_name=ai_semantic_config
    # )
    
    
    # Use DefaultAzureCredential to get the access token
    # When using DefaultAzureCredential, ensure that the environment is set up correctly. 
    # - the client should have RBAC role search-index-data reader assigned
    # - the search service should have role based access control (RBAC) enabled
    credential = DefaultAzureCredential()
    search_client = SearchClient(endpoint=ai_search_url,
                      index_name=ai_index_name,
                      credential=credential)

    results = search_client.search(
        search_text=query, 
        query_type="semantic",
        semantic_configuration_name=ai_semantic_config
    )
    
    for index, result in enumerate(results):
        print(f"Index: {index}, Result: {result}")
        if result['content']:
            if search_response is None:
                search_response = result['content']
            else:
                search_response += result['content'] + \
                " \n --- next document ---- \n"

        if index == 2:
            break

    return search_response

# client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))
client = ChatCompletionsClient(endpoint=endpoint, credential=DefaultAzureCredential(), credential_scopes=["https://cognitiveservices.azure.com/.default"])


user_prompt = "What are things to do when the games slow down my computer or crash it?"
search_response = perform_search_based_qna(user_prompt)
response = client.complete(
  messages=[
    SystemMessage(content=sys_prompt),
    UserMessage(content=f"(\n Content: \n {search_response} \n Refer to the context above to answer the user query below \n User Query: \n {user_prompt} \n )")
  ],
  model = model,
  max_tokens=1000
)

print(response)