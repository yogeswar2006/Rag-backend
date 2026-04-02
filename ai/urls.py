from django.urls import path,include
from .views import SearchLLM , ChatRoomView,get_chatRoom_history

urlpatterns = [
    path("search/query/",SearchLLM.as_view(),name="querylog"),
    path("chatroom/create/fetch/",ChatRoomView.as_view(),name="chatroom_detail"),
    path("get/chatroom/history/",get_chatRoom_history,name="chatroom_history"),
    
]
