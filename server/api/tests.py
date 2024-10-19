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
        results = backtest(
            records=records, 
            start_date=datetime.strptime('2024-01-01', '%Y-%m-%d').date(),
            end_date=datetime.strptime('2024-02-01', '%Y-%m-%d').date(),
            buy_range=3,
            sell_range=2,
            initial_investment=5000
        )
        
        total_return = results["total_return"]
        trade_count = results["trade_count"]
        max_drawdown = results["max_drawdown"]
        self.assertAlmostEqual(302.5, total_return, 0, "Backtest result total return does not match")
        self.assertEqual(26, trade_count, "Backtest result trade count does not match")
        self.assertAlmostEqual(-7.96, max_drawdown, 0, "Backtest result max drawdown does not match")
    
    def test_backtestApiCase1(self):
        response = self.client.post('/api/backtest/', {
            'startDate': '2024-01-01',
            'endDate': '2024-02-01',
            'buyRange': '3',
            'sellRange': '2',
            'investment': '5000',
        }, format='json')
        
        self.assertEqual(response.status_code, 200)

        results = json.loads(response.content)
        total_return = results["total_return"]
        trade_count = results["trade_count"]
        max_drawdown = results["max_drawdown"]
        self.assertAlmostEqual(302.5, total_return, 0, "Backtest result total return does not match")
        self.assertEqual(26, trade_count, "Backtest result trade count does not match")
        self.assertAlmostEqual(-7.96, max_drawdown, 0, "Backtest result max drawdown does not match")
        
    
    def test_backtestApiCase2(self):
        response = self.client.post('/api/backtest/', {
            'startDate': '2012-01-01',
            'endDate': '2024-10-01',
            'buyRange': '200',
            'sellRange': '50',
            'investment': '5000',
        }, format='json')
        
        self.assertEqual(response.status_code, 200)

        results = json.loads(response.content)
        total_return = results["total_return"]
        trade_count = results["trade_count"]
        max_drawdown = results["max_drawdown"]
        self.assertAlmostEqual(6361.7, total_return, 0, "Backtest result total return does not match")
        self.assertEqual(1256, trade_count, "Backtest result trade count does not match")
        self.assertAlmostEqual(-87.1, max_drawdown, 0, "Backtest result max drawdown does not match")
        
    