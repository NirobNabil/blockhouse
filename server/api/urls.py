from django.urls import path
from .views import update_db, backtest_endpoint, forecast

urlpatterns = [
    path('update_db/', update_db, name="update_db"),
    path('backtest/', backtest_endpoint, name="backtest"),
    path('forecast/', forecast, name="forecast"),
]