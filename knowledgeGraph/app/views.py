# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# # from .Module_Final.class_QA_Neo4j import QAUsingNeo4j

# # qa_neo4j = QAUsingNeo4j()

# # def process(query):
# #     answer = qa_neo4j.full_question_answer(query)
# #     return answer

# # @api_view(['POST'])
# # def chatbot(request):
# #     question = request.data.get('question')
# #     if not question:
# #         return Response({"status": "failure", "error": "Missing 'question' in request"}, status=400)
    
# #     try:
# #         answer = process(question)
# #     except Exception as e:
# #         return Response({"status": "failure", "error": str(e)}, status=500)
        
# #     return Response({"status": "success", "answer": answer})

# # def process_cypher(query):
# #     cypher = qa_neo4j.query_to_cypher(query)
# #     return cypher

# # @api_view(['POST'])
# # def cypher(request):
# #     question = request.data.get('question')
# #     if not question:
# #         return Response({"status": "failure", "error": "Missing 'question' in request"}, status=400)
    
# #     try:
# #         answer = process_cypher(question)
# #     except Exception as e:
# #         return Response({"status": "failure", "error": str(e)}, status=500)
        
# #     return Response({"status": "success", "answer": answer})


# from django.shortcuts import render
# from django.contrib.auth.models import User
# from .models import Chat
# from .serializer import ChatSerialier, UserRegistrationSerializer
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework.response import Response

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

# class CustomTokenObitanPairView(TokenObtainPairView):
#     def post(self, request, *args, **kwargs):
#         try:
#             response = super().post(request, *args, **kwargs)
#             tokens = response.data

#             access_token = tokens['access']
#             refresh_token = tokens['refresh']

#             res = Response()
#             res.data = {'success':True}    

#             res.set_cookie(
#                 key = "access_token",
#                 value = access_token,
#                 httponly= True,
#                 secure = True,
#                 samesite = None,
#                 path='/'
#             )
#             res.set_cookie(
#                 key = "refresh_token",
#                 value = refresh_token,
#                 httponly= True,
#                 secure = True,
#                 samesite = None,
#                 path='/'
#             )
#             return res
#         except:
#             return Response({'success':False})

# class CustomRefreshTokenView(TokenRefreshView):
#     def post(self, request, *args, **kwargs):
#         try:
#             refresh_token = request.COOKIES.get('refresh_token')
#             request.data['refresh'] = refresh_token

#             response = super().post(request, *args, **kwargs)
            
#             tokens = response.data
#             access_token = tokens['access']
            
#             res = Response()
#             res.data = {'refreshed':True}
            
#             res.set_cookie(
#                 key='access_token',
#                 value = access_token,
#                 httponly = True,
#                 secure = True,
#                 samesite = None,
#                 path = '/'
#             )
            
#             return res
#         except:
#             return Response({'refreshed':False}) 

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_chats(request):
#     user =  request.user
#     chats = Chat.objects.filter(owner=user).order_by('time')
#     serializer = ChatSerialier(chats, many=True)
#     return Response(serializer.data)

# @api_view(['POST'])
# def logout(request):
#     try:
#         res = Response()
#         res.data = {'success': True}
#         res.delete_cookie('access_token', path='/', samesite='None')
#         res.delete_cookie('refresh_token', path='/', samesite='None')
#         return res
#     except:
#         return Response({'success': False})
    
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def is_authenticated(request):
#     return Response({'authenticated':True})

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register(request):
#     serializer = UserRegistrationSerializer(data= request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.error)

# from rest_framework import viewsets
# class ChatViewSet(viewsets.ModelViewSet):
#     queryset = Chat.objects.all()
#     serializer_class = ChatSerialier
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         # Thiết lập `owner` là người dùng hiện tại khi tạo mới
#         serializer.save(owner=self.request.user)
        

#     def get_queryset(self):
#         # Lọc các tin nhắn theo người dùng hiện tại
#         return Chat.objects.filter(owner=self.request.user)

