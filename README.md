# Azure AI Inference with Serverless Models and RAG Sample

This sample demonstrates how to use **serverless models** in **Azure AI Foundry** with the **Azure AI Inference SDK**, specifically showcasing the **Grok-3-Mini** and **DeepSeek-R1** models. The **Azure AI Inference SDK** acts as a unified wrapper over generative AI models provisioned in Azure AI Foundry, enabling **zero code changes** when switching between different models. The sample also implements **Retrieval-Augmented Generation (RAG)** using **Azure AI Search** to provide contextual information to the AI models.

## Overview

This application shows how to:
- Use serverless AI models (Grok-3-Mini and DeepSeek-R1) deployed in Azure AI Foundry
- Leverage the Azure AI Inference SDK as a unified wrapper for generative AI models
- Switch between different models seamlessly with **zero code changes** - only the model parameter needs to be updated
- Implement RAG (Retrieval-Augmented Generation) using Azure AI Search
- Authenticate using Azure credentials (DefaultAzureCredential)
- Process search results and present them as context to AI models

## Architecture

```
User Query → Azure AI Search → Search Results → AI Model → Enhanced Response
```

1. **User Query**: The application receives a user question
2. **Azure AI Search**: Performs semantic search to find relevant documents
3. **Context Assembly**: Combines search results into a structured context
4. **AI Model Processing**: Sends the context and query to the selected serverless model
5. **Enhanced Response**: Returns an AI-generated answer based on the retrieved context

## Key Features

### Azure AI Inference SDK Wrapper
- **Unified Interface**: The Azure AI Inference SDK provides a consistent API across all generative AI models in Azure AI Foundry
- **Zero Code Changes**: Switch between any supported models (Grok-3-Mini, DeepSeek-R1, GPT, Claude, etc.) by only changing the model parameter
- **Model Abstraction**: No need to learn different APIs or SDKs for different model providers
- **Future-Proof**: New models added to Azure AI Foundry automatically work with existing code

### Serverless Models Support
- **Grok-3-Mini**: Fast and efficient model for general-purpose tasks
- **DeepSeek-R1**: Advanced reasoning model for complex queries
- **Easy Model Switching**: Change models by simply updating the `model` parameter - no other code modifications needed

### RAG Implementation
- **Semantic Search**: Uses Azure AI Search with semantic configuration
- **Document Chunking**: Processes multiple search results as context
- **Context Limitation**: Retrieves top 3 most relevant documents to optimize token usage

### Authentication
- **Azure Identity**: Uses `DefaultAzureCredential` for secure, passwordless authentication
- **RBAC Support**: Works with role-based access control for both AI services and search

## Prerequisites

1. **Azure AI Foundry** with deployed serverless models:
   - Grok-3-Mini model endpoint
   - DeepSeek-R1 model endpoint

2. **Azure AI Search** service with:
   - Search index containing your data
   - Semantic search configuration enabled
   - RBAC enabled (recommended)

3. **Azure Identity** setup:
   - Your account should have appropriate RBAC roles:
     - `Cognitive Services User` for AI models
     - `Search Index Data Reader` for Azure AI Search

## Setup Instructions

### 1. Clone and Install Dependencies

```bash
git clone <repository-url>
cd ai-on-own-data-sample1
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Azure AI Foundry Endpoint
endpoint=https://your-ai-foundry-endpoint.inference.ai.azure.com

# Model Names (deployed in Azure AI Foundry)
grok_model=grok-3-mini
deep_seek_model=DeepSeek-R1

# Azure AI Search Configuration
ai_search_url=https://your-search-service.search.windows.net
ai_index_name=your-index-name
ai_semantic_config=default

# Optional: API Keys (if not using DefaultAzureCredential)
# api_key=your-api-key
# ai_search_key=your-search-key
```

### 3. Azure RBAC Configuration

Ensure your Azure identity has the following role assignments:

**For Azure AI Services:**
```bash
az role assignment create \
  --assignee <your-user-principal-id> \
  --role "Cognitive Services User" \
  --scope "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<ai-service-name>"
```

**For Azure AI Search:**
```bash
az role assignment create \
  --assignee <your-user-principal-id> \
  --role "Search Index Data Reader" \
  --scope "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.Search/searchServices/<search-service-name>"
```

## Usage

### Running the Sample

```bash
python client.py
```

### Switching Models

To switch between models, simply change the `model` variable in `client.py`:

```python
# Use Grok-3-Mini
model = grok_model

# Or use DeepSeek-R1
model = deep_seek_model
```

The Azure AI Inference SDK handles the rest automatically - **no code changes required**! This is the power of the Azure AI Inference SDK - it abstracts away the complexities of different model APIs and provides a unified interface for all generative AI models provisioned in Azure AI Foundry.

### Customizing the Query

Modify the `user_prompt` variable to test with different questions:

```python
user_prompt = "What are things to do when the games slow down my computer or crash it?"
```

## Code Structure

### Main Components

1. **Environment Setup**: Loads configuration from `.env` file
2. **Search Function**: `perform_search_based_qna()` handles Azure AI Search integration
3. **AI Client**: `ChatCompletionsClient` manages communication with serverless models
4. **RAG Pipeline**: Combines search results with user query for enhanced responses

### Key Code Sections

**Model Selection:**
```python
# Easy model switching
model = grok_model  # or deep_seek_model
```

**Azure AI Search Integration:**
```python
def perform_search_based_qna(query):
    # Perform semantic search
    results = search_client.search(
        search_text=query, 
        query_type="semantic",
        semantic_configuration_name=ai_semantic_config
    )
    
    # Combine top 3 results
    for index, result in enumerate(results):
        if index == 2:
            break
    
    return search_response
```

**AI Model Interaction:**
```python
response = client.complete(
    messages=[
        SystemMessage(content=sys_prompt),
        UserMessage(content=f"Content: {search_response} \n User Query: {user_prompt}")
    ],
    model=model,
    max_tokens=1000
)
```

## Sample Output

The application will:
1. Display the search query being processed
2. Show search results with document indices
3. Present the AI model's response based on retrieved context

Example:
```
Calling Azure Search for query: What are things to do when the games slow down my computer or crash it?
Index: 0, Result: {...}
Index: 1, Result: {...}
Index: 2, Result: {...}

[AI Response based on retrieved gaming troubleshooting documentation]
```

## Benefits of This Approach

### Azure AI Inference SDK Advantages
- **Unified API**: Single SDK works with all generative AI models in Azure AI Foundry
- **No Vendor Lock-in**: Easy to switch between different model providers without code changes
- **Consistent Experience**: Same authentication, error handling, and response format across all models
- **Simplified Development**: Focus on your application logic, not on learning different model APIs

### Serverless Models
- **Cost Effective**: Pay only for what you use
- **Scalable**: Automatic scaling based on demand
- **Model Variety**: Access to latest models without infrastructure management
- **Zero Code Migration**: Switch to new models as they become available without any code changes

### RAG Implementation
- **Accurate Responses**: Answers based on your specific data
- **Source Attribution**: Clear connection between responses and source documents
- **Reduced Hallucination**: Grounds responses in actual retrieved content

### Azure Integration
- **Secure**: Uses Azure identity and RBAC
- **Reliable**: Enterprise-grade security and availability
- **Integrated**: Seamless integration between Azure services

## Troubleshooting

### Common Issues

1. **Authentication Errors**: Ensure your Azure identity has proper RBAC roles
2. **Model Not Found**: Verify model names match your Azure AI Foundry deployments
3. **Search Errors**: Check that your search service has RBAC enabled and index exists
4. **Missing Dependencies**: Run `pip install -r requirements.txt`

### Environment Variables

Double-check that all required environment variables are set in your `.env` file and that the endpoints are correct.

## Next Steps

- Experiment with different search queries and model combinations
- Customize the system prompt for your specific use case
- Implement additional search filters or ranking
- Add error handling and logging for production use
- Explore other serverless models available in Azure AI Foundry

## Dependencies

- `azure-ai-inference`: Azure AI Inference SDK
- `azure-search-documents`: Azure AI Search SDK
- `azure-identity`: Azure authentication
- `python-dotenv`: Environment variable management
- `aiohttp`: HTTP client library

---

This sample demonstrates the power of the **Azure AI Inference SDK** as a unified wrapper for generative AI models, combined with Azure's intelligent search capabilities to create sophisticated AI applications. The SDK's abstraction layer means you can experiment with different models (Grok-3-Mini, DeepSeek-R1, and any future models) with **zero code complexity** - just change the model parameter and you're ready to go!
