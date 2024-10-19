from django.db import models

# Create your models here.
class StockData(models.Model):
    open = models.DecimalField(max_digits=10, decimal_places=4)
    high = models.DecimalField(max_digits=10, decimal_places=4)
    low = models.DecimalField(max_digits=10, decimal_places=4)
    close = models.DecimalField(max_digits=10, decimal_places=4)
    volume = models.IntegerField()
    date = models.DateField(unique=True)
    symbol = models.CharField(max_length=11)
    
    def __str__(self):
        return self.date.strftime("%Y-%m-%d")
    
    
    
class BacktestResults(models.Model):
    issue_date = models.DateField(unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    investment = models.IntegerField()
    buy_range = models.IntegerField()
    sell_range = models.IntegerField()
    sharpe = models.FloatField()
    sortino = models.FloatField()
    VaR = models.FloatField()
    max_drawdown = models.FloatField()
    total_return = models.FloatField()
    trade_count = models.FloatField()
    report_filepath = models.CharField(max_length=200)
    
    def __str__(self):
        return self.issue_date.strftime("%Y-%m-%d")