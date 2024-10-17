from django.urls import path
from .views import update_db

urlpatterns = [
    path('update_db/', update_db, name="update_db"),
]