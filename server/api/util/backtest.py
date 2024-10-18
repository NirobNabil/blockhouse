from datetime import datetime, timedelta
import sys

def mean(records):
    count = len(records)
    result = 0
    for r in records:
        result += ( float(r.open) + float(r.close) + float(r.high) + float(r.low) ) / 4
    return result / count


def backtest(records, start_date, end_date, buy_range, sell_range, initial_investment):
    
    balance = float(initial_investment)
    stocks = 0
    
    record_count = len(records)
    start_idx = None
    trade_count = 0
    min_price = sys.float_info.max
    max_price = sys.float_info.min
    
    try:        
        # this logic works because the records are sorted
        start_idx = list(map(lambda x:(x.date - start_date).days >= 0 and (x.date - start_date).days <= 2, records)).index(True)
        end_idx = record_count - list(reversed(list(map(lambda x:(x.date - end_date).days <= 0 and (x.date - end_date).days >= -2, records)))).index(True)
    except ValueError:
        pass # TODO
    
    for cur_idx in range(start_idx, end_idx+1):
        buy_mean = mean(records[cur_idx-buy_range-1:cur_idx])
        sell_mean = mean(records[cur_idx-sell_range-1:cur_idx])
        cur_price = float(records[cur_idx].open)
        
        min_price = min(min_price, cur_price)
        max_price = max(max_price, cur_price)
        
        if cur_price > sell_mean and stocks != 0:
            stocks -= 1
            balance += cur_price
            trade_count += 1
            continue   # prevent buying if already sold in this round
        
        if cur_price < buy_mean and balance >= cur_price:
            stocks += 1
            balance -= cur_price
            trade_count += 1
        
    if stocks > 0:
        trade_count += stocks
        balance += float(records[record_count-1].high) * stocks
        stocks = 0
        
    max_drawdown = ( ( min_price - max_price ) / max_price ) * 100.0
        
    return {
        "total_return": balance - initial_investment,
        "trade_count": trade_count,
        "max_drawdown": max_drawdown
    }