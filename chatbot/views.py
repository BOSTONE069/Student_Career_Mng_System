# chatbot/views.py

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from edu_hub.settings import AZURE_OPENAI_KEY
# from langchain_openai import ChatOpenAI
# from langchain.schema import AIMessage, HumanMessage, SystemMessage

# # Initialize the ChatOpenAI model using GPT-4o and the Azure API key
# model = ChatOpenAI(model="gpt-4o", openai_api_key=AZURE_OPENAI_KEY)

# # Global chat history to maintain conversation context across API calls
# chat_history = [
#     SystemMessage(content=(
#         "You are a knowledgeable and friendly career and university courses advisor. "
#         "You help students explore different career paths based on their interests and competencies. "
#         "You also suggest suitable university courses and programs that align with their skills and aspirations."
#     ))
# ]

# @csrf_exempt  # Disable CSRF protection for this API endpoint (since it's called via POST from other apps like Flutter)
# def chat_api(request):
#     """
#     API endpoint to handle chat messages from the frontend.
#     Accepts POST requests with a 'message' in the JSON body.
#     Returns the AI-generated response as JSON.
#     """
#     if request.method == 'POST':
#         # Parse the JSON body from the request
#         data = json.loads(request.body)
#         user_message = data.get('message')

#         if not user_message:
#             # If no message was provided, return an error response
#             return JsonResponse({'error': 'No message provided'}, status=400)

#         # Add the user's message to the chat history
#         chat_history.append(HumanMessage(content=user_message))

#         # Use the ChatOpenAI model to generate an AI response
#         result = model.invoke(chat_history)
#         response = result.content

#         # Add the AI's response to the chat history
#         chat_history.append(AIMessage(content=response))

#         # Return the response to the client as JSON
#         return JsonResponse({'response': response})

#     # If the request method is not POST, return an error response
#     return JsonResponse({'error': 'Invalid request method'}, status=405)

## Uncomment the above if you want to use the LangChain OpenAI model directly.


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from openai import AzureOpenAI
from edu_hub.settings import AZURE_OPENAI_KEY, AZURE_OPENAI_ENDPOINT

# Initialize the AzureOpenAI client with API key and endpoint
# This client will handle all the communication with the Azure-hosted GPT model
client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT, 
    api_version="2024-02-01"
)

# Global chat history to maintain context across multiple API calls
# Starts with a system message to set the AI's behavior and purpose
chat_history = [
    {
        "role": "system",
        "content": (
            "You are a knowledgeable and friendly career and university courses advisor. "
            "You help students explore different career paths based on their interests and competencies. "
            "You also suggest suitable university courses and programs that align with their skills and aspirations."
        )
    }
]

@csrf_exempt  # Disable CSRF protection (since this endpoint is typically used by external clients like mobile apps)
def chat_api(request):
    """
    Django view to handle chat-based interactions.
    Accepts POST requests with a JSON body containing a 'message' key.
    Uses the Azure OpenAI API to generate a response and maintains the chat context.
    """
    if request.method == 'POST':
        # Parse the incoming JSON request body
        data = json.loads(request.body)
        user_message = data.get('message')

        # If no message is provided, return an error response
        if not user_message:
            return JsonResponse({'error': 'No message provided'}, status=400)

        # Add the user's message to the ongoing chat history
        chat_history.append({"role": "user", "content": user_message})

        # Send the full chat history to the Azure OpenAI API to generate a response
        response = client.chat.completions.create(
            model="gpt-4o",  # Specify the model deployed in Azure
            messages=chat_history
        )

        # Extract the AI's response text from the API response
        ai_response = response.choices[0].message.content

        # Add the AI's response to the chat history for future context
        chat_history.append({"role": "assistant", "content": ai_response})

        # Return the AI's response to the client as JSON
        return JsonResponse({'response': ai_response})

    # If the request is not POST, return a 405 Method Not Allowed error
    return JsonResponse({'error': 'Invalid request method'}, status=405)

