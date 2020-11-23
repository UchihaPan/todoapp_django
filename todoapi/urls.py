from django.urls import path, include
from .views import TodoListCompletedView, TodoListCreateView, TodoListUpdateView, TodoCompleteView,signup,login

urlpatterns = [
    path('apicompleted/', TodoListCompletedView.as_view(), name='completedapiview'),
    path('apicreate/', TodoListCreateView.as_view(), name='createapiview'),
    path('update/<int:pk>/', TodoListUpdateView.as_view(), name='updateapiview'),
    path('<int:pk>/complete', TodoCompleteView.as_view(), name='completetodoapiapiview'),
    path('apisignup/', signup, name='apisignup'),
    path('apilogin/', login, name='apilogin'),

]
