from django.shortcuts import render
from rest_framework.views import APIView
from .search import RagSearch
from documents.vectorStore import VectorStore
from documents.embeddings import Embeddings
from .models import QueryLog , ChatRoom
from django.contrib.auth import get_user_model
from companies.models import Company
from django.http import JsonResponse
from .serializers import ChatRoomSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes , api_view


from django.shortcuts import get_object_or_404

class ChatRoomView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        title = request.data.get("title")
        user = request.user
        company = user.company
        
        try:
            obj = ChatRoom.objects.create(
            user = user,
            company=company,
            title = title
            
               )
            print(f"created chat room {obj.id}")
            return JsonResponse({"id":obj.id,"title":obj.title,"created_at":obj.created_at,
                                 "status":True})
        except:
            return JsonResponse({"Error at creating chatroom"})
    
    def get(self,request):
        user  = request.user
        
        chatRooms = ChatRoom.objects.filter(user=user).order_by("-created_at")
        
        serializer  = ChatRoomSerializer(chatRooms,many=True)
        
        return Response({
            "chat_rooms":serializer.data
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chatRoom_history(request):
    
    user = request.user
    chat_room_id = request.GET.get('chat_room_id')

    chats = QueryLog.objects.filter(
        chatRoom_id=chat_room_id,
        user=user
    ).order_by("created_at")

    messages = []

    for chat in chats:
        messages.append({
            "sender": "question",
            "text": chat.question
        })
        messages.append({
            "sender": "response",
            "text": chat.response
        })

    return JsonResponse({"messages": messages})
       
        
        
        


class SearchLLM(APIView):
   
    def post(self, request):
        query = request.data.get("query")
        chat_room_id = request.data.get("chat_room_id")
        

        if not query:
            return JsonResponse({
                "status": False,
                "error": "Query is required"
            }, status=400)

        #  Secure user handling
        user = request.user
        company = user.company   # make sure this relation exists
        
        chatRoom = get_object_or_404(ChatRoom,id=chat_room_id,user=user,company=company)

        vector_store = VectorStore()
        embed = Embeddings()

        retrieved_docs = vector_store.Search(
            query,
            3,
            embed,
            str(company.id)
        )
        
        if not retrieved_docs:
            return JsonResponse({
                "response":"Your query doesn't related to your company documents!",
                "status":False,
            })

        answer = RagSearch(retrieved_docs, query)

        if not answer:
            answer = "No relevant answer found."

        #  Save log
        QueryLog.objects.create(
            chatRoom=chatRoom,
            user=user,
            company=company,
            question=query,
            response=answer
        )

        return JsonResponse({
            "response": answer,
            "status": True,
        })
