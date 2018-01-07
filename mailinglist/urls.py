from django.urls import path
from .views import Subscribe

urlpatterns = [
    path('', Subscribe.as_view()),
]