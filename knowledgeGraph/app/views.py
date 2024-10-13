from rest_framework.decorators import api_view
from rest_framework.response import Response

def process(question):
    return "Output test: " + question

@api_view(['POST'])
def chatbot(request):
    question = request.data.get('question')
    if not question:
        return Response({"status": "failure", "error": "Missing 'question' in request"}, status=400)
    
    answer = process(question)
    return Response({"status": "success", "answer": answer})
