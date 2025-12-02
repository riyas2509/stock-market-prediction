# Imports libraries to handle data (pandas, numpy) and dates (datetime and timedelta).
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# For plotting
from dash import Dash, dcc, html, Output, Input
import plotly.graph_objects as go

# Step 1: GENERATE SAMPLE DATA FILE
np.random.seed(42)
STOCKS = [
    'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFC.NS', 'ICICIBANK.NS',
    'LT.NS', 'SBIN.NS', 'KOTAKBANK.NS', 'ITC.NS', 'BHARTIARTL.NS',
    'GOLDBEES.NS', 'SILVERBEES.NS'
]

DAYS = 100
base = datetime.today()
date_list = [base - timedelta(days=x) for x in range(DAYS)][::-1]

all_data = []
for ticker in STOCKS:
    price = 1000 + np.random.randint(-10, 10)
    for dt in date_list:
        open_price = price + np.random.randint(-20, 20)
        high_price = open_price + np.random.randint(0, 20)
        low_price = open_price - np.random.randint(0, 20)
        actual_close = open_price + np.random.randint(-15, 15)
        predicted_close = actual_close + np.random.normal(0, 10)  

        all_data.append({
        'Date': dt,
        'Ticker': ticker,
        'Open': open_price,
        'High': high_price,
        'Low': low_price,
        'Actual_Close': actual_close,
        'Predicted_Close': predicted_close,
        })
        price = actual_close

df = pd.DataFrame(all_data)
df.sort_values(['Ticker', 'Date'], inplace=True)
df.to_excel('Stock_And_Commodities_Analysis.xlsx', index=False)

print("Sample Excel file created: Stock_And_Commodities_Analysis.xlsx\n")

# Step 2: DASH APP CODE
app = Dash(__name__)
df['Date'] = pd.to_datetime(df['Date'])
stock_options = [{'label': t, 'value': t} for t in df['Ticker'].unique()]

app.layout = html.Div(style={'backgroundColor': '#111111', 'color': 'white', 'padding': '20px'}, children=[
    html.H1("Indian Stocks & Commodities - Actual vs Predicted Price Viewer", style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='stock-dropdown',
        options=stock_options,
        placeholder="Select a stock or commodity",
        searchable=True,
        style={'width': '50%', 'margin': 'auto', 'color': 'black', }
    ),
    dcc.Graph(id='price-chart', config={'displayModeBar': False})
])

@app.callback(
    Output('price-chart', 'figure'),
    Input('stock-dropdown', 'value')
)
def update_chart(selected_ticker):
    if not selected_ticker:
        return go.Figure(layout=dict(plot_bgcolor='#111111', paper_bgcolor='#111111', font_color='white'))

    df_filtered = df[df['Ticker'] == selected_ticker].copy()
    df_filtered.sort_values('Date', inplace=True)

    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df_filtered['Date'],
        open=df_filtered['Open'],
        high=df_filtered['High'],
        low=df_filtered['Low'],
        close=df_filtered['Actual_Close'],
        increasing_line_color='green',
        decreasing_line_color='red',
        name='Actual Price'
    ))

    fig.add_trace(go.Scatter(
        x=df_filtered['Date'],
        y=df_filtered['Predicted_Close'],
        mode='lines',
        line=dict(color='blue', dash='dash'),
        name='Predicted Price'
    ))

    fig.update_layout(
        title=f"{selected_ticker} Price: Actual & Predicted",
        xaxis_title="Date",
        yaxis_title="Price",
        template='plotly_dark',
        hovermode="x unified",
        font=dict(family="Arial", size=12),
        legend=dict(x=0, y=1, bgcolor='rgba(0,0,0,0)')
    )
    return fig

# Starts the Dash development server
if __name__ == '__main__':
    app.run(debug=True)
