# chatbot/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from edu_hub.settings import AZURE_OPENAI_KEY
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage


# Create the ChatOpenAI model
model = ChatOpenAI(model="gpt-4o", openai_api_key=AZURE_OPENAI_KEY)

# Initialize chat history
chat_history = [
    SystemMessage(content=(
    "You are a knowledgeable and friendly career and university courses advisor. "
    "You help students explore different career paths based on their interests and competencies. "
    "You also suggest suitable university courses and programs that align with their skills and aspirations."
))
]

@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')

        if not user_message:
            return JsonResponse({'error': 'No message provided'}, status=400)

        # Add user's message to chat history
        chat_history.append(HumanMessage(content=user_message))

        # Get AI response
        result = model.invoke(chat_history)
        response = result.content

        # Add AI message to chat history
        chat_history.append(AIMessage(content=response))

        return JsonResponse({'response': response})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
