# Imports libraries to handle data (pandas, numpy) and dates (datetime and timedelta).
# Used for creating sample stock data and handling date operations.

# NumPy generates random numbers for realistic stock price simulation.
# pandas structures that raw simulated data in a DataFrame (tabular format), making it easy to organize and query (for dropdowns, graphs).
# timedelta helps you build the timeline (100 days from today) over which your prices are generated.
# Your Dash app then allows users to pick a stock from the pandas DataFrame, and visualize the pandas time series using Plotly for interactive charts.
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# For plotting
# Imports Dash components (Dash, dcc for core components like dropdown and graph, html for HTML elements).
# Imports Plotly's graph objects to create charts.
# These are the building blocks of your interactive web app and the charts shown.
from dash import Dash, dcc, html, Output, Input
import plotly.graph_objects as go

# Step 1: GENERATE SAMPLE DATA FILE
# Sets seed for reproducible random data generation for sample stock prices.
np.random.seed(42)

# Defines a list of popular Indian stocks and ETFs for Gold and Silver.
# Creates a list of 100 sequential dates starting 100 days ago until today.
# These will be used to generate fake historical data.

# "RELIANCE.NS" means the Reliance Industries Ltd stock on the National Stock Exchange of India
# ".NS" suffix in stock names stands for National Stock Exchange (NSE) of India
# ".BO" for Bombay Stock Exchange stocks, ".L" for London Stock Exchange, ".NYSE" for New York Stock Exchange

# Ticker Symbol	    Full Company or ETF Name

# RELIANCE.NS	    Reliance Industries Limited
# TCS.NS	        Tata Consultancy Services Limited
# INFY.NS	        Infosys Limited
# HDFC.NS	        Housing Development Finance Corporation Ltd.
# ICICIBANK.NS	    ICICI Bank Limited
# LT.NS	            Larsen & Toubro Limited
# SBIN.NS	        State Bank of India
# KOTAKBANK.NS	    Kotak Mahindra Bank Limited
# ITC.NS	        ITC Limited
# BHARTIARTL.NS	    Bharti Airtel Limited
# GOLDBEES.NS	    Nippon India Gold BeES (Gold ETF)
# SILVERBEES.NS	    Nippon India Silver BeES (Silver ETF)
STOCKS = [
    'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFC.NS', 'ICICIBANK.NS',
    'LT.NS', 'SBIN.NS', 'KOTAKBANK.NS', 'ITC.NS', 'BHARTIARTL.NS',
    'GOLDBEES.NS', 'SILVERBEES.NS'
]

# Defines the number of days for which you want to simulate or generate date data.
# Here, 100 means you want 100 consecutive dates.
DAYS = 100  # 100 days of data
# Gets the current date and time at the moment the code runs.
# base is the reference point (usually "today") from which you will calculate past dates.
base = datetime.today()
# This is a list comprehension creating a list of dates.
# For each x in 0 to DAYS-1 (i.e., 0 to 99):
#   Subtracts x days from base using timedelta(days=x) to go backwards in time.
#   For example, when x=0 you get base (today), when x=1 you get yesterday, and so on.
# The resulting list is a sequence of dates counting backward from today.
# The [::-1] reverses the list so it becomes ascending dates from oldest (100 days ago) to newest (today).
# Effectively, date_list contains 100 consecutive dates from 100 days ago up to today, in chronological order.
date_list = [base - timedelta(days=x) for x in range(DAYS)][::-1]

# Loops through each stock and each date, generating random open, high, low, actual close, and predicted close prices.
# The price simulates real stock price movements with randomness.
# all_data collects one dictionary per day per stock representing one row of stock data.

# Initializes an empty list all_data that will store dictionaries representing each stock's price data for each date.
all_data = []
# Starts a loop over each stock ticker symbol in the list STOCKS.
# This loop will generate data for every stock separately.
for ticker in STOCKS:
    # Initializes a starting price for the current stock.
    # It sets the price around 1000 with a random offset from -10 to +9, to vary the initial starting point for each stock.
    price = 1000 + np.random.randint(-10, 10)
    # Starts an inner loop over each date in the date_list.
    # This loop generates simulated daily price data points for the current stock over all chosen dates.
    for dt in date_list:
        # Simulates the opening price on date dt by taking the previous day’s price and adding a daily fluctuation between -20 and +19.
        # Adds randomness to mimic real market opening price changes.
        open_price = price + np.random.randint(-20, 20)
        # Sets the high price on the date as the opening price plus a positive random amount (0 to 19).
        # Ensures that high price is at least the opening price, simulating intraday price peak.
        high_price = open_price + np.random.randint(0, 20)
        # Sets the low price as opening price minus a random amount (0 to 19).
        # Ensures low price is less or equal to opening price, simulating intraday price drop.
        low_price = open_price - np.random.randint(0, 20)
        # Calculates the actual closing price as opening price plus a random change from -15 to +14.
        # Simulates daily closing price movement relative to opening.
        actual_close = open_price + np.random.randint(-15, 15)
        # Generates a predicted closing price by adding a noise sampled from a normal (Gaussian) distribution centered at zero with std deviation of 10 to the actual close.
        # This simulates an imperfect forecast around the actual closing price.
        predicted_close = actual_close + np.random.normal(0, 10)  # Simulate predicted
        # Creates a dictionary holding all the simulated data fields for the current date and stock, storing date, stock ticker, open/high/low prices, the actual closing price, and the predicted closing price.
        # Appends this dictionary to the list all_data.

        # Adds a new item (dictionary) to the end of the list all_data. The list stores each simulated data point for stocks over time.
        # Dictionary inside append
        # Creates a dictionary representing a single record (one row) of stock price data for a specific date and ticker.
        all_data.append({
        # Sets the key 'Date' with the value dt (current date in the loop). This marks the date of the record.
        'Date': dt,
        # Adds the key 'Ticker' with the value ticker (current stock symbol in the outer loop). Identifies which stock this record belongs to.
        'Ticker': ticker,
        # Adds 'Open' price: the simulated opening price for the stock on dt.
        'Open': open_price,
        # Adds 'High' price: the simulated highest price during that trading day.
        'High': high_price,
        # Adds 'Low' price: the simulated lowest price during that day.
        'Low': low_price,
        # Adds the actual closing price simulated for the stock on that day.
        'Actual_Close': actual_close,
        # Adds predicted closing price generated by adding noise to actual close, simulating forecasted price.
        'Predicted_Close': predicted_close,
        })
        # Updates the "previous price" variable to the actual closing price of the current day.
        # This new price is used in the next iteration to calculate the next day’s open price, providing continuity.
        price = actual_close

# Converts all_data list to a pandas DataFrame.
# Sorts rows by ticker and date for organized display.
# Saves the data to Excel for external analysis or later use.
# Prints a confirmation message.
# This Excel file simulates your price dataset.
df = pd.DataFrame(all_data)
df.sort_values(['Ticker', 'Date'], inplace=True)
df.to_excel('Stock_And_Commodities_Analysis.xlsx', index=False)

print("Sample Excel file created: Stock_And_Commodities_Analysis.xlsx\n")

# Step 2: DASH APP CODE
# Creates the Dash app object.
# Converts the 'Date' column to datetime type (ensures proper time axis plotting).
# Extracts unique stock tickers to populate the dropdown menu (user input on the page).
app = Dash(__name__)
df['Date'] = pd.to_datetime(df['Date'])
stock_options = [{'label': t, 'value': t} for t in df['Ticker'].unique()]

# Defines the HTML structure and styles of the app interface:
#     Dark background with white text for contrast.
#     Title centered at the top.
#     Dropdown menu for stock selection, centered with 50% width and black text so options are visible.
#     Graph component for displaying the price chart (initially empty).
# The layout tells Dash what to render on the webpage.
app.layout = html.Div(style={'backgroundColor': '#111111', 'color': 'white', 'padding': '20px'}, children=[
    html.H1("Indian Stocks & Commodities - Actual vs Predicted Price Viewer", style={'textAlign': 'center'}),
    # This creates a dropdown menu component in the Dash app.
    dcc.Dropdown(
        # Assigns a unique identifier used to link this component with callbacks.
        id='stock-dropdown',
        # Populates the dropdown with a list of options; each option typically has a label (what user sees) and a value (actual data value).
        options=stock_options,
        # Displays this text inside the dropdown when no option is selected, guiding the user.
        placeholder="Select a stock or commodity",
        # Enables a search bar in the dropdown so users can quickly find options by typing.
        searchable=True,
        # CSS styles the dropdown to be 50% width of its container, centered horizontally (margin: auto), and text color black for readability.
        style={'width': '50%', 'margin': 'auto', 'color': 'black', }
    ),
    # dcc.Graph: Creates an area in the app for displaying interactive Plotly charts.
    # id='price-chart': Unique identifier for linking with Dash callbacks where the chart's content updates dynamically based on user input.
    # config={'displayModeBar': False}: Hides Plotly's floating toolbar above the graph for a cleaner look.
    dcc.Graph(id='price-chart', config={'displayModeBar': False})
])

# The callback decorator links the dropdown's selected value (Input) to the graph's figure (Output).
# The function update_chart runs every time user selects a stock from dropdown.
# If no stock is selected (first page load), returns an empty dark background figure.
# This makes the page interactive: user changes the dropdown, and the graph updates dynamically.
@app.callback(
    Output('price-chart', 'figure'),
    Input('stock-dropdown', 'value')
)
def update_chart(selected_ticker):
    if not selected_ticker:
        return go.Figure(layout=dict(plot_bgcolor='#111111', paper_bgcolor='#111111', font_color='white'))

    # Filters the DataFrame to only the chosen stock's data.
    # Sorts by date to ensure chronological order on the x-axis of the graph.
    # This subset drives all the plot data for the selected stock.
    df_filtered = df[df['Ticker'] == selected_ticker].copy()
    df_filtered.sort_values('Date', inplace=True)

    # Initializes a new Plotly figure to add traces (data series).
    fig = go.Figure()

    # Candlestick for actual price
    # Adds a candlestick chart trace with actual price OHLC data.
    # Green/red colors indicate days when price rose/fell respectively, just like real stock charts.
    # Visually shows detailed price movement patterns.

    # Adds a trace (a data series or layer) to your Plotly figure fig. Here, the trace is a candlestick chart.
    # Creates a candlestick chart object from Plotly's graph_objects module. This type of chart visualizes price movements of financial assets.
    fig.add_trace(go.Candlestick(
        # Sets the x-axis values as dates corresponding to each price record. This places candlesticks along the timeline.
        x=df_filtered['Date'],
        # Assigns the opening prices for each date. The bottom or top of the candlestick "box" depends on this value.
        open=df_filtered['Open'],
        # Specifies the highest price reached during the trading session for each date, marking the top whisker of the candlestick.
        high=df_filtered['High'],
        # Specifies the lowest price during the session, marking the bottom whisker.
        low=df_filtered['Low'],
        # The closing prices determine the other edge of the candlestick box opposite the open price.
        close=df_filtered['Actual_Close'],
        # Sets the line color for days where closing price is higher than opening price (positive price movement) as green, indicating gains.
        increasing_line_color='green',
        # Sets the line color for days where closing price is lower than opening price (negative price movement) as red, indicating losses.
        decreasing_line_color='red',
        # Sets the legend name for this trace, letting users distinguish it from others like predicted prices.
        name='Actual Price'
    ))

    # Overlay predicted close as dashed blue line
    # Adds a line chart trace overlay for predicted closing prices.
    # Blue dashed line differentiates prediction from actual candlestick price.
    # Helps users compare forecast vs real data visually.

    # Adds a new trace (layer of data) to the existing Plotly figure object fig. Traces determine what gets plotted.
    # Creates a scatter or line plot object from Plotly's graph_objects module. This can represent points, lines, or both.
    fig.add_trace(go.Scatter(
        # Sets the x-axis data to the Date column of your filtered DataFrame. Represents time axis for the data.
        x=df_filtered['Date'],
        # Sets the y-axis data to Predicted_Close prices corresponding to each date. This is the forecasted stock price.
        y=df_filtered['Predicted_Close'],
        # Specifies the trace should be drawn as continuous lines connecting all data points (no markers).
        mode='lines',
        # Defines the line appearance:
        #   Color is blue.
        #   dash means the line is drawn as dashed, distinguishing it visually from solid lines.
        line=dict(color='blue', dash='dash'),
        # Gives this trace a label shown in the chart legend for user reference.
        name='Predicted Price'
    ))

    # Configures graph styling:
    #   Dynamic title to show selected stock.
    #   Axis titles.
    #   Dark theme matching app background.
    #   "Unified hover" mode to show all trace values for a date on hover.
    #   Clean legend placement.
    # Improves usability and visual appeal.

    # Updates the layout properties of an existing Plotly figure fig. This is how you customize the overall appearance and layout settings.
    fig.update_layout(
        # Sets the main title of the plot dynamically based on the selected stock ticker, such as "RELIANCE.NS Price: Actual & Predicted".
        title=f"{selected_ticker} Price: Actual & Predicted",
        # Sets the label of the x-axis to "Date", providing a clear time reference for the data.
        xaxis_title="Date",
        # Sets the label of the y-axis to "Price", clarifying what the vertical axis represents.
        yaxis_title="Price",
        # Applies a predefined dark theme template to the chart, giving it a sleek, dark background with contrasting colors, improving visual clarity.
        template='plotly_dark',
        # Configures hover behavior so that when you hover over the chart, all data points aligned vertically with the cursor are shown together in a unified tooltip. This aids in comparing multiple traces at the same time.
        hovermode="x unified",
        # Sets the font style for all text elements in the chart:
        #   Font family: Arial (widely supported, clean)
        #   Font size: 12 pixels for readability
        font=dict(family="Arial", size=12),
        # Customizes the legend:
        #   x=0: Position along the x-axis (left side).
        #   y=1: Position at the top of the plot area.
        #   bgcolor='rgba(0,0,0,0)': Fully transparent background for the legend box.
        legend=dict(x=0, y=1, bgcolor='rgba(0,0,0,0)')
    )

    # Returns the completed figure to Dash, which renders it in the dcc.Graph output area.
    # This redraws the graph with the chosen stock’s actual and predicted price data.
    return fig

# Starts the Dash development server when you run this script.
# App listens for user interactions and updates UI reactively.
# Opens on your browser to interact with dropdown and price chart.
if __name__ == '__main__':
    app.run(debug=True)

# give line by line explaination of this code



# write an error handling code