from django.urls import path
from user.views import HelloView

urlpatterns = [
    path('hello/', HelloView.as_view()),


]