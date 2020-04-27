# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 13:23:51 2020

@author: metalcorebear
"""

# Import relevant functions
import stock_functions


# Class to pull historic or intraday stock data using the World Trading Data API.

class stock_API():
    
    def __init__(self, API_KEY):
        
        self.key = API_KEY

    def daily(self, TKR, time_delta, beta=True, EX='^IXIC'):
        
        if beta == False:
            date_from, date_to = stock_functions.get_date_range(time_delta)
            daily_url = stock_functions.build_url_stock(self.key, TKR, date_to, date_from)
            output = stock_functions.get_json(daily_url)
            try:
                out_data = stock_functions.get_closing_prices_and_volumes(output)
            except:
                out_data = {'error':'Requested stock could not be found.'}
        
        else:
            date_from, date_to = stock_functions.get_date_range(time_delta)
            daily_url = stock_functions.build_url_stock(self.key, TKR, date_to, date_from)
            ex_url = stock_functions.build_url_stock(self.key, EX, date_to, date_from)
            output = stock_functions.get_json(daily_url)
            ex_output = stock_functions.get_json(ex_url)
            try:
                out_data = stock_functions.get_closing_prices_and_volumes(output)
                out_data_ex = stock_functions.get_closing_prices_and_volumes(ex_output)
                b = stock_functions.beta(out_data['closing_prices'], out_data_ex['closing_prices'])
                b_dict = {'beta':b}
                out_data.update(b_dict)
            except:
                out_data = {'error':'Requested stock could not be found.'}

        return out_data
    
    def intraday(self, TKR, range_=1, interval=60, beta=True, EX='^IXIC'):
        
        if beta == False:
            intraday_url = stock_functions.build_url_stock_intraday(self.key, TKR, range_, interval)
            output = stock_functions.get_json(intraday_url)
            out_data = stock_functions.get_closing_prices_and_volumes_intraday(output)
            
        else:
            intraday_url = stock_functions.build_url_stock_intraday(self.key, TKR, range_, interval)
            ex_url = stock_functions.build_url_stock_intraday(self.key, EX, range_, interval)
            output = stock_functions.get_json(intraday_url)
            ex_output = stock_functions.get_json(ex_url)
            out_data = stock_functions.get_closing_prices_and_volumes(output)
            out_data_ex = stock_functions.get_closing_prices_and_volumes(ex_output)
            b = stock_functions.beta(out_data['closing_prices'], out_data_ex['closing_prices'])
            b_dict = {'beta':b}
            out_data.update(b_dict)
            
        return out_data
        
    
# Class to generate synthetic stock data (bullish or oscillating random price)

class syn_stock():
    
    def __init__(self):
        
        self.help = '"Oscillator" method generates an oscillating random price from Gaussian random noise added to a sine function.  "bullish_random" method is a bullish Gaussian random variable.  Note that these generators may on occasion generate negative prices.'
        
    def oscillator(self, n, scale=1):
        output = stock_functions.oscillating_random_price(n, scale)
        return output
    
    def bullish_random(self, n, scale=1):
        output = stock_functions.bullish_random_price(n, scale)
        return output
        

# Class to calculate momentum indicators
        
class analyze():
    
    def __init__(self, input_, closing_prices='closing_prices'):
        
        if type(input_) == list:
            self.price_list = input_
        elif type(input_) == dict:
            try:
                self.price_list = input_[closing_prices]
            except:
                self.price_list = []
        else:
            print('Error: input_ must be list or dict type.  Object not properly instantiated.')
            self.price_list = []
    
    def stochastic_oscillator(self, n, c=3):
        
        K_list, D_list, new_price_list = stock_functions.stochastic_oscillator(self.price_list, n, c)
        output = stock_functions.KD_Analysis(K_list, D_list)
        output_list = [K_list, D_list, output]
        output_label_list = ['K', 'D', 'Assessment']
        json_out = stock_functions.gen_json(output_list, new_price_list, output_label_list)
        self.stochastic_output = json_out
        assessment = json_out['Assessment'][-1]
        if assessment == -1:
            self.stochastic_assessment = 'Buy Signal'
        elif assessment == 1:
            self.stochastic_assessment = 'Sell Signal'
        else:
            self.stochastic_assessment = 'Hold Signal'
            
        
    def RSI(self, n):
        
        RSI_out, new_price_list = stock_functions.RSI_chart(self.price_list, n)
        output = stock_functions.RSI_generator(RSI_out)
        output_list = [RSI_out, output]
        output_label_list = ['RSI_out', 'Assessment']
        json_out = stock_functions.gen_json(output_list, new_price_list, output_label_list)
        self.RSI_output = json_out
        assessment = json_out['Assessment'][-1]
        if assessment == -1:
            self.RSI_assessment = 'Buy Signal'
        elif assessment == 1:
            self.RSI_assessment = 'Sell Signal'
        else:
            self.RSI_assessment = 'Hold Signal'