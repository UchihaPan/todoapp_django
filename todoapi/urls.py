from django.urls import path,include
from .views import TodoListCompletedView

urlpatterns = [
    path('completed/', TodoListCompletedView.as_view(),name='completedapiview'),

]
