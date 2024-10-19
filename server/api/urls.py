from django.urls import path
from .views import update_db, backtest_endpoint, get_previous_backtests, forecast, generate_model_performance

urlpatterns = [
    path('update_db/', update_db, name="update_db"),
    path('backtest/', backtest_endpoint, name="backtest"),
    path('previous_backtests/', get_previous_backtests, name="previous_backtests"),
    path('forecast/', forecast, name="forecast"),
    path('generate_model_performance/', generate_model_performance, name="generate_model_performance"),
]