from django.urls import path
from .views import ActivityListView, CalculateTheLove, AchievementResultsView, FetchCalculation

urlpatterns = [
    path('', ActivityListView.as_view()),
    path('<int:activity_id>', CalculateTheLove.as_view()),
    path('results/<int:calculation_id>', AchievementResultsView.as_view()),
    path('calculation/<int:calculation_id>', FetchCalculation.as_view()),
]