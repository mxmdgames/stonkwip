import yfinance as yf
import pandas as pd
import ta
from functools import lru_cache

@lru_cache(maxsize=None)
def load_data(ticker, period, interval):
    data = yf.download(ticker, period=period, interval=interval)
    if data.empty:
        raise ValueError("No data found for the given ticker and time frame.")
    data.reset_index(inplace=True)
    return data

def calculate_technical_indicators(data):
    data['SMA'] = ta.trend.SMAIndicator(data['Close'], window=20).sma_indicator()
    data['EMA'] = ta.trend.EMAIndicator(data['Close'], window=20).ema_indicator()
    data['RSI'] = ta.momentum.RSIIndicator(data['Close'], window=14).rsi()
    macd = ta.trend.MACD(data['Close'])
    data['MACD'], data['MACD_Signal'], data['MACD_Hist'] = macd.macd(), macd.macd_signal(), macd.macd_diff()
    so = ta.momentum.StochasticOscillator(data['High'], data['Low'], data['Close'])
    data['Stoch'], data['Stoch_Signal'] = so.stoch(), so.stoch_signal()
    bbands = ta.volatility.BollingerBands(data['Close'])
    data['BB_High'], data['BB_Low'] = bbands.bollinger_hband(), bbands.bollinger_lband()
    ichimoku = ta.trend.IchimokuIndicator(data['High'], data['Low'])
    data['Ichimoku_A'], data['Ichimoku_B'], data['Ichimoku_Base'], data['Ichimoku_Conv'] = ichimoku.ichimoku_a(), ichimoku.ichimoku_b(), ichimoku.ichimoku_base_line(), ichimoku.ichimoku_conversion_line()
    data['Parabolic_SAR'] = ta.trend.PSARIndicator(data['High'], data['Low'], data['Close']).psar()
    data['OBV'] = ta.volume.OnBalanceVolumeIndicator(data['Close'], data['Volume']).on_balance_volume()
    data['FearGreedIndex'] = calculate_fear_greed_index(data)
    return data

def calculate_fear_greed_index(data):
    rsi_normalized = (data['RSI'] - data['RSI'].min()) / (data['RSI'].max() - data['RSI'].min()) * 100
    sma_distance = data['Close'] / data['SMA'] - 1
    sma_normalized = (sma_distance - sma_distance.min()) / (sma_distance.max() - sma_distance.min()) * 100
    volume_normalized = (data['Volume'] - data['Volume'].min()) / (data['Volume'].max() - data['Volume'].min()) * 100
    fear_greed_index = (rsi_normalized + sma_normalized + volume_normalized) / 3
    return fear_greed_index
 
