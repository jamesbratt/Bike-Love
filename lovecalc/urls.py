from django.urls import path
from .views import ActivityListView, CalculateTheLove

urlpatterns = [
    path('', ActivityListView.as_view()),
    path('/<int:activity_id>', CalculateTheLove.as_view()),
]