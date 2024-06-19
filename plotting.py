import plotly.graph_objects as go

def create_gauge(title, value):
    ranges = [0, 20, 40, 60, 80, 100]
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        gauge={
            'axis': {'range': [None, 100], 'tickvals': ranges, 'ticktext': ['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed']},
            'bar': {'color': "black"},
            'steps': [
                {'range': [0, 20], 'color': '#FF0000'},
                {'range': [20, 40], 'color': '#FF4500'},
                {'range': [40, 60], 'color': '#FFD700'},
                {'range': [60, 80], 'color': '#32CD32'},
                {'range': [80, 100], 'color': '#008000'}],
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': value}
        }
    ))
    return fig

def plot_candlestick(data, selected_indicators, show_volume, draw_trend_line):
    fig = go.Figure()

    datetime_col = 'Datetime' if 'Datetime' in data.columns else 'Date'

    fig.add_trace(go.Candlestick(x=data[datetime_col], open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='Candlesticks'))

    if 'SMA' in selected_indicators:
        fig.add_trace(go.Scatter(x=data[datetime_col], y=data['SMA'], mode='lines', name='SMA', line=dict(color='orange')))
    if 'EMA' in selected_indicators:
        fig.add_trace(go.Scatter(x=data[datetime_col], y=data['EMA'], mode='lines', name='EMA', line=dict(color='purple')))
    if 'BBands' in selected_indicators:
        fig.add_trace(go.Scatter(x=data[datetime_col], y=data['BB_High'], mode='lines', name='BB High', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=data[datetime_col], y=data['BB_Low'], mode='lines', name='BB Low', line=dict(color='red')))
    if 'Ichimoku Cloud' in selected_indicators:
        fig.add_trace(go.Scatter(x=data[datetime_col], y=data['Ichimoku_A'], mode='lines', name='Ichimoku A', line=dict(color='pink')))
        fig.add_trace(go.Scatter(x=data[datetime_col], y=data['Ichimoku_B'], mode='lines', name='Ichimoku B', line=dict(color='brown')))
        fig.add_trace(go.Scatter(x=data[datetime_col], y=data['Ichimoku_Base'], mode='lines', name='Ichimoku Base Line', line=dict(color='yellow')))
        fig.add_trace(go.Scatter(x=data[datetime_col], y=data['Ichimoku_Conv'], mode='lines', name='Ichimoku Conversion Line', line=dict(color='grey')))
    if 'Parabolic SAR' in selected_indicators:
        fig.add_trace(go.Scatter(x=data[datetime_col], y=data['Parabolic_SAR'], mode='markers', name='Parabolic SAR', marker=dict(color='green', symbol='circle', size=5)))

    if show_volume:
        fig.add_trace(go.Bar(x=data[datetime_col], y=data['Volume'], name='Volume', marker=dict(color='gray'), yaxis='y2'))

    fig.update_layout(
        title="Stock Data and Technical Indicators",
        yaxis_title='Stock Price',
        xaxis_title='Date',
        template='plotly_dark',
        yaxis2=dict(
            title='Volume',
            overlaying='y',
            side='right',
            showgrid=False,
        ),
        xaxis_rangeslider_visible=False,
        dragmode='drawline' if draw_trend_line else 'zoom'
    )

    return fig

def plot_indicators(data, selected_indicators):
    datetime_col = 'Datetime' if 'Datetime' in data.columns else 'Date'

    if 'RSI' in selected_indicators:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data[datetime_col], y=data['RSI'], mode='lines', name='RSI', line=dict(color='blue')))
        fig.update_layout(
            title="Relative Strength Index (RSI)",
            yaxis_title='RSI',
            xaxis_title='Date',
            template='plotly_dark',
            xaxis_rangeslider_visible=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    if 'MACD' in selected_indicators:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data[datetime_col], y=data['MACD'], mode='lines', name='MACD', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=data[datetime_col], y=data['MACD_Signal'], mode='lines', name='MACD Signal', line=dict(color='red')))
        fig.add_trace(go.Bar(x=data[datetime_col], y=data['MACD_Hist'], name='MACD Histogram'))
        fig.update_layout(
            title="MACD (Moving Average Convergence Divergence)",
            yaxis_title='MACD',
            xaxis_title='Date',
            template='plotly_dark',
            xaxis_rangeslider_visible=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    if 'Stochastic Oscillator' in selected_indicators:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data[datetime_col], y=data['Stoch'], mode='lines', name='Stochastic Oscillator', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=data[datetime_col], y=data['Stoch_Signal'], mode='lines', name='Stochastic Signal', line=dict(color='red')))
        fig.update_layout(
            title="Stochastic Oscillator",
            yaxis_title='Stochastic Oscillator',
            xaxis_title='Date',
            template='plotly_dark',
            xaxis_rangeslider_visible=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    if 'OBV' in selected_indicators:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data[datetime_col], y=data['OBV'], mode='lines', name='OBV', line=dict(color='blue')))
        fig.update_layout(
            title="On-Balance Volume (OBV)",
            yaxis_title='OBV',
            xaxis_title='Date',
            template='plotly_dark',
            xaxis_rangeslider_visible=False,
        )
        st.plotly_chart(fig, use_container_width=True)
