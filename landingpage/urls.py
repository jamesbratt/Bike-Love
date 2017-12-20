from django.urls import path
from django.views.generic import TemplateView
from .views import Logout

urlpatterns = [
    path('', TemplateView.as_view(template_name="landingpage/landing-page.html")),
    path('logout', Logout.as_view()),
]