import os
import numpy as np
import joblib

model = joblib.load(os.path.join(os.path.dirname(__file__), '../data/lin_model.pkl') ) 

def parse_records_to_open_price_numpy(records):
    arr = []
    for record in records:
        arr.append(record.open)
    arr = np.array(arr).astype(float)
    return arr

def forecast_30days(records):
    Xs = parse_records_to_open_price_numpy(records)
    y = model.predict([Xs])
    return [Xs, y[0]]

def predict_for_many_rows(records):
    Xs = np.array([ record.open for record in records[:100] ]).reshape(1,100).astype(float)
    
    # this is to allocate memory at initialization so that continuous reallocation doesnt take up long in the following for loop
    Xs = np.concatenate( ( Xs, np.zeros( (len(records) - 100, 100) ) ), axis=0 )
    for i in range(100, len(records)):
        Xs[i-99] = np.append(Xs[i-100][1:], records[i].open).reshape(1,100).astype(float)
    
    
    y = model.predict(Xs)

    return [Xs, y]