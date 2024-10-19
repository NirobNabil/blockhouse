import matplotlib.pyplot as plt
import pandas as pd
import os

def plot_ml(plot_df, file_path):
    plt.rcParams["figure.figsize"] = (11,6)
    plt.plot(plot_df["date"], plot_df["pred"], label='Linear_Regression_Predictions')
    if "groundtruth" in plot_df:
        plt.plot(plot_df["date"], plot_df["groundtruth"], label='Actual Price')
    plt.legend(loc="upper left")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.savefig( file_path, bbox_inches='tight')
    plt.clf()
    

def plot_only_forecast(data_df, file_path):

    plot_pred = list(data_df["pred"])
    
    data = {
        "date":  list(data_df["date"]),
        "pred": plot_pred,
    }

    plot_df = pd.DataFrame(data)
    plot_ml(plot_df, file_path)
    
    
def plot_forecast_with_groundtruth(data_df, file_path):

    data = {
        "date":  list(data_df["date"]),
        "pred": list(data_df["pred"]),
        "groundtruth": list(data_df["groundtruth"]),
    }

    plot_df = pd.DataFrame(data)
    plot_ml(plot_df, file_path)


# Expects data_df to be sorted by date
# TODO: add docstrings
# made an exception by not taking data_df as param because converting this big array into DF and then converting back into array is not efficient
def plot_25th_preds(pred, groundtruth, dates, file_path):

    plot_pred = []
    plot_groundtruth = []
    lookforward_range = 25
    for pred_i in range(0, len(pred)):
        v_gt = groundtruth[pred_i][lookforward_range]
        v_p = pred[pred_i][lookforward_range]
        plot_pred.append(v_p)
        plot_groundtruth.append(v_gt)
    
    print(len(plot_groundtruth), len(plot_pred), len(dates))
    
    data = {
        "date": dates,
        "pred": plot_pred,
        "groundtruth": plot_groundtruth
    }

    plot_df = pd.DataFrame(data)
    plot_ml(plot_df, file_path)
    


def plot_returns(data_df, file_path):
    
    plt.rcParams["figure.figsize"] = (11,6)
    plt.plot(data_df["date"], data_df["return"], label='Backtest returns')
    plt.legend(loc="upper left")
    plt.xlabel("Date")
    plt.ylabel("Return")
    plt.savefig( file_path, bbox_inches='tight')
    plt.clf()