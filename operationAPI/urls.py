from django.urls import path
from .views import OperationsView

urlpatterns = [
    path('operation', OperationsView.as_view())
]