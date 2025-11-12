from django.urls import path
from .views import MenuTreeView

urlpatterns = [
    path('',MenuTreeView.as_view(),name='menu-list'),
]