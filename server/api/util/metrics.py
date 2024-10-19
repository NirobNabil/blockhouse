
import numpy as np
import pandas as pd

def sharpe(stats, risk_free_rate=0.0999):
    account_values = np.array(list(map(lambda x:x["value"], stats)))
    annualized_coefficient = len(account_values)
    diff = np.diff( account_values, 1 ) / account_values[1:]
    annualized_std = diff.std() * np.sqrt(annualized_coefficient)
    return ( diff.mean() * annualized_coefficient - risk_free_rate ) / annualized_std

def sortino(stats, risk_free_rate=0.0999):
    account_values = np.array(list(map(lambda x:x["value"], stats)))
    annualized_coefficient = len(account_values)
    diff = np.diff( account_values, 1 ) / account_values[1:]
    neg_returns = diff[diff < 0]
    annualized_std = neg_returns.std() * np.sqrt(annualized_coefficient)
    return ( diff.mean() * annualized_coefficient - risk_free_rate ) / annualized_std

def max_drawdown(stats):
    account_values = pd.Series(list(map(lambda x:x["value"], stats)))
    returns = account_values.diff(1) / account_values[1:]
    cumulative = (returns + 1).cumprod()
    peak = cumulative.expanding(min_periods=1).max()
    dd = (cumulative / peak) - 1
    return dd.min()

def VaR(stats, alpha=0.95):
    account_values = np.array(list(map(lambda x:x["value"], stats)))
    initial_value = account_values[0]
    returns = np.diff( account_values, 1 ) / account_values[1:]
    returns_sorted = np.sort(returns)
    index = int(alpha * len(returns_sorted))
    return initial_value * abs(returns_sorted[index])