from django.urls import path,include
from .views import TodoListCompletedView,TodoListCreateView,TodoListUpdateView

urlpatterns = [
    path('completed/', TodoListCompletedView.as_view(),name='completedapiview'),
path('create/', TodoListCreateView.as_view(),name='createapiview'),
path('update/<int:pk>/', TodoListUpdateView.as_view(),name='updateapiview'),


]
