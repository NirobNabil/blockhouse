from rest_framework import serializers
from .models import StockData, BacktestResults

class StockDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockData
        fields = '__all__'
        
class BacktestResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BacktestResults
        fields = '__all__'