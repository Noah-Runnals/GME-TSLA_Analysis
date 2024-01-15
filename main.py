import yfinance as yf
from bs4 import BeautifulSoup
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import warnings


warnings.filterwarnings("ignore", category=FutureWarning)
def analyze_stock(ticker,url_in):
    ticker_data = yf.download(ticker, period='max')

    url = url_in
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'html5lib')
    Ticker_revenue = pd.DataFrame(columns=['Date', 'Revenue'])
    table = soup.find_all('table', attrs={'class': 'historical_data_table table'})
    for row in table[1].find_all('tr'):
        col = row.find_all('td')
        if col:
            date = col[0].text
            revenue = col[1].text
            input = {"Date": date, "Revenue": revenue.replace("$","").replace(",","")}
            Ticker_revenue.loc[len(Ticker_revenue.index)] = input
    Ticker_revenue = Ticker_revenue.drop(51).set_index('Date')


    def make_graph(stock_data, revenue_data, stock):
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing=.3)
        stock_data_specific = stock_data[stock_data.index <= '2025-06-14']
        revenue_data_specific = revenue_data[revenue_data.index <= '2025-04-30']
        fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.index, infer_datetime_format=True),
                                 y=stock_data_specific['Close'].astype("float"), name="Share Price"), row=1, col=1)
        fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.index, infer_datetime_format=True),
                                 y=revenue_data_specific['Revenue'].astype("float"), name="Revenue"), row=2, col=1)
        fig.update_xaxes(title_text="Date", row=1, col=1)
        fig.update_xaxes(title_text="Date", row=2, col=1)
        fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
        fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
        fig.update_layout(showlegend=False,
                          height=900,
                          title=stock,
                          xaxis_rangeslider_visible=True)
        fig.show()


    make_graph(ticker_data, Ticker_revenue,ticker)


tsla_url ='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm'
gme_url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html'
analyze_stock("TSLA",tsla_url)
analyze_stock("GME",gme_url)