from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import DatabaseError
from django.conf import settings
import pandas as pd
import numpy as np
import requests
import urllib
import os
import datetime
import os
import joblib
import uuid

from .models import StockData, BacktestResults
from .serializer import StockDataSerializer, BacktestResultsSerializer
from .models import StockData
from .util.backtest import backtest
from .util.visualizeHelper import plot_25th_preds, plot_only_forecast, plot_forecast_with_groundtruth, plot_returns
from .util.modelHelper import forecast_30days, predict_for_many_rows, parse_records_to_open_price_numpy
from .util.pdfHelper import pdf_for_model_performance, pdf_for_backtest, pdf_for_forecast


API_BASEURL = "https://www.alphavantage.co/"


## TODO: implement rate limiting
@api_view(['GET'])
def update_db(request):

    
    try: 
        symbol = request.GET.get('symbol')
    except Exception as e:
        print(e)
        return Response("request needs to include symbol field", status=status.HTTP_400_BAD_REQUEST)
        
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
        

    with open("gg.json", "w") as f:
        import json
        f.write(json.dumps(records))


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
    
    plot1_filepath = os.path.join(os.path.dirname(__file__), f'static/tmp/{str(uuid.uuid4())}.png')
    plot_returns(pd.DataFrame(data={
        "date": results["dates"],
        "return": results["returns"]
    }), file_path=plot1_filepath)
    
    data = {
        "issue_date": datetime.datetime.today().date(),
        "start_date": start_date,
        "end_date": end_date,
        "investment": investment,
        "buy_range": buy_range,
        "sell_range": sell_range,
        "sharpe": results["metrics"]["sharpe"],
        "sortino": results["metrics"]["sortino"],
        "VaR": results["metrics"]["VaR"],
        "max_drawdown": results["metrics"]["max_drawdown"],
        "total_return": results["total_return"],
        "trade_count": results["trade_count"],
        "returns_plot_filepath": plot1_filepath
    }
    
    pdf_filename = f"backtest_result_{str(uuid.uuid4())}.pdf"
    pdf_for_backtest(data, os.path.join(os.path.dirname(__file__), f'static/pdf/{pdf_filename}'))
    data["report_filepath"] = settings.MEDIA_BASEURL+"pdf/"+pdf_filename
    
    os.remove(plot1_filepath)
    
    serializer = BacktestResultsSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)
    
    return Response( settings.MEDIA_BASEURL+"pdf/"+pdf_filename, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_previous_backtests(request):
    previous_backtests = BacktestResults.objects.all()
    if len(previous_backtests) == 0:
        return Response("No previous backtest results", status=status.HTTP_200_OK)
        
    serializer = BacktestResultsSerializer(data=previous_backtests, many=True)
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response("Couldn't fetch previous backtests", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def forecast(request):

    ##### input validation

    symbol = request.GET.get('symbol')
    try:
        date = datetime.datetime.strptime(request.GET.get('date'), '%Y-%m-%d').date()
    except:
        return Response("Invalid date value", status=status.HTTP_400_BAD_REQUEST)

    if date > datetime.datetime.today().date():
        return Response("Please choose a date of today or earlier", status=status.HTTP_400_BAD_REQUEST)
    
    
    # check if there is groundtruth data available in the database for comparison
    groundtruth_available = False
    if StockData.objects.order_by("-date").first().date >= date + datetime.timedelta(days=30):
        groundtruth_available = True
        
            
    dates = []
    groundtruth = []
    if groundtruth_available:
        records = list(reversed(StockData.objects.filter(symbol=symbol).filter(date__lt=date).order_by('-date')[:100]))  # get previous 100 days of data
        records += list(StockData.objects.filter(symbol=symbol).filter(date__gte=date).order_by('date'))[:30]  # get next 30 days of data for groundtruth
        groundtruth = parse_records_to_open_price_numpy(records[100:])

        for record in records[100:]:
            dates.append(record.date)
    
    else:
        try:
            records = list(reversed(StockData.objects.filter(symbol=symbol).filter(date__lte=date).order_by('-date')[:100]))
        except DatabaseError:
            return Response("Choose an earlier date", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        dates = [ date + datetime.timedelta(days=i) for i in range(0, 30) ]
        
        
    
    ##### make predictions
    
    predictions = forecast_30days(records[:100])[1]
    
    
    ##### plot comparison graphs
    
    plot_filepath = os.path.join(os.path.dirname(__file__), 'static/'+str(uuid.uuid4())+".png" )
    if groundtruth_available:
        data_df = pd.DataFrame({
            "date": dates,
            "pred": predictions,
            "groundtruth": groundtruth,
        })
        plot_forecast_with_groundtruth(data_df, plot_filepath)
        
    else:
        data_df = pd.DataFrame({
            "date": dates,
            "pred": predictions,
            "filename": plot_filepath
        }) 
        plot_only_forecast(data_df, plot_filepath)
    
    
    # generate pdf
    pdf_filename = f'forecast_{str(uuid.uuid4())}.pdf'
    pdf_filepath = os.path.join(os.path.dirname(__file__), 'static/tmp/'+pdf_filename )
    pdf_for_forecast({
        "start_date": date,
        "forecast_plot_filepath": plot_filepath
    }, pdf_filepath)
    
    
    return Response({"pdf": settings.MEDIA_BASEURL+"tmp/"+pdf_filename}, status=status.HTTP_200_OK)
    # return Response({
    #     "predictions": predictions
    # })
    
    
    
@api_view(['GET'])
def generate_model_performance(request):
    
    symbol = request.GET.get('symbol')
    records = list(StockData.objects.filter(symbol=symbol).order_by('date'))  # get previous 100 days of data
    
    [Xs, predictions] = predict_for_many_rows(records)
    
    plot1_filepath = os.path.join(os.path.dirname(__file__), 'static/'+str(uuid.uuid4())+".png" )
    plot_25th_preds(predictions, Xs, [ record.date for record in records[99:] ], plot1_filepath)
    
    
    plot2_filepath = os.path.join(os.path.dirname(__file__), 'static/'+str(uuid.uuid4())+".png" )
    predictions = forecast_30days(records[-130:][:100])[1]
    groundtruth = parse_records_to_open_price_numpy(records[-30:])
    data_df = pd.DataFrame({
        "date": [ record.date for record in records[-30:] ],
        "pred": predictions,
        "groundtruth": groundtruth,
    })
    plot_forecast_with_groundtruth(data_df, plot2_filepath)
    
    pdf_filename = f'model_performance_{symbol}_{datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')}.pdf'
    pdf_filepath = os.path.join(os.path.dirname(__file__), 'static/pdf/'+pdf_filename )
    pdf_for_model_performance({
        "historical_data_plot_path": plot1_filepath,
        "forecast_data_plot_path": plot2_filepath
    }, filepath=pdf_filepath)
    
    os.remove(plot1_filepath)
    os.remove(plot2_filepath)
    
    return Response({"pdf": settings.MEDIA_BASEURL+"pdf/"+pdf_filename}, status=status.HTTP_200_OK)
        
    # Xs = np.array(Xs).astype(float) 
    
    
    
    