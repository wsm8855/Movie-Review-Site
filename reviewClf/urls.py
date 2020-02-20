from django.urls import path

from . import views

urlpatterns = [
    path('', views.enter_review, name='enter_review')
]