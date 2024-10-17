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
    