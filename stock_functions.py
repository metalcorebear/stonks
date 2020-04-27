# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 13:27:48 2020

@author: metalcorebear
"""

# Functions list


import requests
import numpy as np
import pandas as pd
from datetime import date as datemethod
from datetime import timedelta


# Stock functions
def get_date_range(time_delta):
    t = datemethod.today()
    dt = timedelta(days = time_delta)
    t0 = t - dt
    date_from = datemethod.strftime(t0, '%Y-%m-%d')
    date_to = datemethod.strftime(t, '%Y-%m-%d')
    return date_from, date_to

def build_url_stock(API_KEY, TKR, date_to, date_from):
    base_url = 'https://api.worldtradingdata.com/api/v1/history?symbol='
    symbol = TKR
    url = base_url + symbol + '&date_from=' + date_from + '&date_to=' + date_to + '&sort=asc&api_token=' + API_KEY
    return url

def build_url_stock_intraday(API_KEY, TKR, range_, interval):
    base_url = 'https://intraday.worldtradingdata.com/api/v1/intraday?symbol='
    symbol = TKR
    url = base_url + symbol + '&interval=' + str(interval) + '&range=' + str(range_) + '&sort=asc&api_token=' + API_KEY
    return url
    
def get_json(url):
    page = requests.request('GET', url)
    output = page.json()
    return output

def get_closing_prices_and_volumes(output):
    data = output['history']
    dates_0 = data.keys()
    dates_0.sort()
    dates = []
    for i in dates_0:
        dates.append(i.replace('-',''))
    closing_prices = []
    volumes = []
    for date in dates_0:
        closing_prices.append(float(data[date]['close']))
        volumes.append(float(data[date]['volume']))
    out_dict = {'dates':dates, 'closing_prices':closing_prices, 'volumes':volumes}
    return out_dict

def get_closing_prices_and_volumes_intraday(output):
    data = output['intraday']
    dates_0 = list(data.keys())
    dates_0.sort()
    dates = []
    for i in dates_0:
        dates.append(i.replace('-',''))
    closing_prices = []
    volumes = []
    for date in dates_0:
        closing_prices.append(float(data[date]['close']))
        volumes.append(float(data[date]['volume']))
    out_dict = {'dates':dates, 'closing_prices':closing_prices, 'volumes':volumes}
    return out_dict

def beta(s,e):
    b = np.cov(s,e)[0][1] / np.var(e)
    return b


# Support functions
def threshold(high, low, metric):
    status = []
    for i in metric:
        if i >= high:
            status.append('OVERBOUGHT')
        elif i <= low:
            status.append('OVERSOLD')
        else:
            status.append('')
    return status

def moving_average(x, c):
    a = np.convolve(x, np.ones(c), 'valid') / c
    return a

def segment_list(price_list, i, n=5):
    if (len(price_list) < n) or (i < n):
        out_list = []
    else:
        range_list = [i-j for j in range(n)]
        out_list = [price_list[j] for j in range_list]
    return out_list


# Stochastic oscillator functions
def oscillator_K(price_list, price):
    L = float(min(price_list))
    H = float(max(price_list))
    if H != L:
        K = 100.0*(price-L)/(H-L)
    else:
        K = 0.5
    return K

def stochastic_oscillator(price_list, n=5, c=3):
    new_price_list = price_list[n:]
    K_list = []
    for i in range(n, len(price_list)):
        price_segment = segment_list(price_list, i, n)
        price = float(price_segment[-1])
        K = oscillator_K(price_segment, price)
        K_list.append(K)
    D_array = moving_average(K_list, c)
    D_list = [0.0 for j in range(n-c)]
    D_list_1 = list(D_array)
    D_list.extend(D_list_1)
    return K_list, D_list, new_price_list

def KD_Analysis(K_list, D_list):
    status = threshold(80, 20, K_list)
    differences = []
    deltas = ['N']
    for i in range(len(K_list)):
        d = K_list[i] - D_list[i]
        if d < 0:
            differences.append(-1)
        if d >= 0:
            differences.append(1)
    for j in range(1, len(differences)):
        delta = differences[i]*differences[j-1]
        if (delta == -1) and (differences[j] > 0):
            deltas.append('P_OVERBOUGHT')
        elif (delta == -1) and (differences[j] <= 0):
            deltas.append('P_OVERSOLD')
        else:
            deltas.append('N')
    comparisons = zip(deltas, status)
    output = []
    for c in comparisons:
        if c[0] == 'P_OVERBOUGHT':
            if c[1] == 'OVERBOUGHT':
                output.append(-1)
        if c[0] == 'P_OVERSOLD':
            if c[1] == 'OVERSOLD':
                output.append(1)
        else:
            output.append(0)
    return output


# Relative strength index functions
def RSI_calc(price_segment):
    up_list = []
    down_list = []
    for i in range(1, len(price_segment)):
        a = price_segment[i] - price_segment[i-1]
        if a <= 0:
            down_list.append(-1*a)
        if a > 0:
            up_list.append(a)
    period = len(price_segment)
    average_up = sum(up_list)/float(period)
    average_down = sum(down_list)/float(period)
    RS = average_up/average_down
    RSI = 100.0 - 100.0/(1.0 + RS)
    return RSI

def RSI_chart(price_list, n=14):
    new_price_list = price_list[n:]
    RSI_out = []
    for i in range(n, len(price_list)):
        price_segment = segment_list(price_list, i, n)
        RSI = RSI_calc(price_segment)
        RSI_out.append(RSI)
    return RSI_out, new_price_list
        
def RSI_generator(RSI_out):
    status = threshold(80, 20, RSI_out)
    output = []
    for i in status:
        if i == 'OVERBOUGHT':
            output.append(-1)
        if i == 'OVERSOLD':
            output.append(1)
        else:
            output.append(0)
    return output
    

# Synthetic price list functions
def bullish_random_price(n, scale=1):
    x = range(n)
    y = 0.0
    result = []
    for _ in x:
        result.append(y)
        a = np.random.normal(loc=10, scale=scale)
        y += round(a,2)
    return result

def oscillating_random_price(n, scale=1):
    x = range(n)
    y = 0.0
    result = []
    for i in x:
        result.append(y)
        a = 10*np.sin(i) + np.random.normal(loc=0, scale=scale)
        y += round(a,2)
    return result

# Output functions
def gen_json(output_list, new_price_list, output_label_list):
    p = {'price':new_price_list}
    for i in range(len(output_list)):
        a = {output_label_list[i]:output_list[i]}
        p.update(a)
    return p
    