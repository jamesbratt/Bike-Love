from django.urls import path
from .views import SendFeedback

urlpatterns = [
    path('', SendFeedback.as_view()),
]