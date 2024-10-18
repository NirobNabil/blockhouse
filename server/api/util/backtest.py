from datetime import datetime, timedelta

def mean(records):
    count = len(records)
    result = 0
    for r in records:
        result += ( r.open + r.close + r.high + r.low ) / 4
    return result / count


def backtest(records, start_date, end_date, buy_range, sell_range, initial_investment):
    
    balance = float(initial_investment)
    stocks = 0
    
    record_count = len(records)
    start_idx = None
    
    try:        
        # this logic works because the records are sorted
        start_idx = list(map(lambda x:(x.date - start_date).days >= 0 and (x.date - start_date).days <= 2, records)).index(True)
    except ValueError:
        pass # TODO
        
    for cur_idx in range(start_idx, record_count):
        buy_mean = mean(records[cur_idx-buy_range-1:cur_idx])
        sell_mean = mean(records[cur_idx-sell_range-1:cur_idx])
        cur_price = float(records[cur_idx].open)
        
        if cur_price > sell_mean and stocks != 0:
            stocks -= 1
            balance += cur_price
            continue   # prevent buying if already sold in this round
        
        if cur_price < buy_mean and balance >= cur_price:
            stocks += 1
            balance -= cur_price
        
    if stocks > 0:
        balance += records[-1].high * stocks
        stocks = 0
        
    return balance