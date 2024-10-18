from rest_framework.test import APIClient, APITestCase
import json
import os
from datetime import datetime, timedelta

from .serializer import StockDataSerializer
from .models import StockData
from .util.backtest import backtest

class BacktestTestCase(APITestCase):
    
    def setUp(self):
        
        with open(os.path.join(os.path.dirname(__file__), 'data/test_db.json'), "r") as f:
            data = json.loads(f.read())
            serializer = StockDataSerializer(data=data, many=True)
            if serializer.is_valid():
                serializer.save()
            
        self.client = APIClient()
        return super().setUp()
    
    def test_backtestCase1(self):
        records = StockData.objects.all().order_by('date')
        balance = backtest(
            records=records, 
            start_date=datetime.strptime('2024-01-01', '%Y-%m-%d').date(),
            end_date=datetime.strptime('2024-02-01', '%Y-%m-%d').date(),
            buy_range=3,
            sell_range=2,
            initial_investment=5000
        )
        self.assertAlmostEqual(5332.8, balance, 1, "Backtest result balance does not match")
    
    def test_backtestApiCase1(self):
        response = self.client.post('/api/backtest/', {
            'startDate': '2024-01-01',
            'endDate': '2024-02-01',
            'buyRange': '3',
            'sellRange': '2',
            'investment': '5000',
        }, format='json')
        
        self.assertEqual(response.status_code, 200)

        response = json.loads(response.content)
        self.assertAlmostEqual(5332.8, response["balance"], 1, "Response balance does not match")
        
    
    def test_backtestApiCase2(self):
        response = self.client.post('/api/backtest/', {
            'startDate': '2012-01-01',
            'endDate': '2024-10-01',
            'buyRange': '200',
            'sellRange': '50',
            'investment': '5000',
        }, format='json')
        
        self.assertEqual(response.status_code, 200)

        response = json.loads(response.content)
        self.assertAlmostEqual(11361.8, response["balance"], 1, "Response balance does not match")
        
    