from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import StockData
from .serializer import StockDataSerializer
from .models import StockData
from django.db import DatabaseError
import requests
import urllib
import os
import datetime

from .util.backtest import backtest

API_BASEURL = "https://www.alphavantage.co/"

@api_view(['POST'])
def update_db(request):

    if 'symbol' not in request.data:
        return Response("request needs to include symbol field", status=status.HTTP_400_BAD_REQUEST)


    symbol = request.data['symbol']
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": os.getenv('ALPHADVANTAGE_APIKEY'),
        "outputsize": "full",
        "datatype": "json"
    }
    
    req_url = API_BASEURL + "query?" + urllib.parse.urlencode(params)

    ## TODO: add logging    
    try:
        response = requests.get(req_url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return Response("alphadvantage api request timed out", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except requests.exceptions.Timeout as e:
        return Response("alphadvantage api request timed out", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    response = response.json()
    response = response["Time Series (Daily)"]
    
    records = []
    for date, values in response.items():
        entry = {
            "date": date,
            "open": float(values["1. open"]),
            "high": float(values["2. high"]),
            "low": float(values["3. low"]),
            "close": float(values["4. close"]),
            "volume": int(values["5. volume"]),
            "symbol": str(symbol)
        }
        records.append(entry)

    import json
    json_object = json.dumps(records, indent=4)
 
    # Writing to sample.json
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)

    ##### filter incoming records 
    
    latest_db_record = StockData.objects.order_by("-date").first()
    database_queue = []
    
    # At database init
    if latest_db_record is None:
        database_queue = records
    
    # only create new entries for dates that dont already exist in database
    else:
        latest_date = latest_db_record.date
        for entry in records:
            entry_date = datetime.datetime.strptime(entry["date"], "%Y-%m-%d").date()
            if entry_date > latest_date:
                database_queue.append(entry)
        
        
    
    ##### save into database
    
    updated_records = []
    try:
        serializer = StockDataSerializer(data=database_queue, many=True)
        if serializer.is_valid():
            serializer.save()
            updated_records = serializer.data
        else:
            return Response("Couldn't save data because data from alphadvantage api is invalid", status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
            
    except DatabaseError as db_e:
        ## TODO: log
        print(e)
        return Response("Database error occurred", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
         
    
    return Response(updated_records, status=status.HTTP_200_OK)


@api_view(['POST'])
def backtest_endpoint(request):
    
    ## TODO: do something about the mean average minimum start range
    try:
        start_date = datetime.datetime.strptime(request.data["startDate"], '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(request.data["endDate"], '%Y-%m-%d').date()
        investment = int(request.data["investment"])
        buy_range = int(request.data["buyRange"])
        sell_range = int(request.data["sellRange"])
        
        # TODO: do something about the 200 days thing
        # oldest = StockData.objects.order_by('date').first()
        # if oldest.date > start_date - datetime.timedelta(days=max(buy_range, sell_range)+1):
        #     raise ValueError("Database doesn't have enough data for given parameters. Please select range within 200 years from today")
        
    except ValueError as e:
        print(e)
        return Response("Invalid values", status=status.HTTP_400_BAD_REQUEST)
    
    records = StockData.objects.all().order_by('date')
    
    results = backtest(records, start_date, end_date, buy_range, sell_range, investment)
    
    return Response(results)
    
    