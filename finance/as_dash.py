# -*- coding: utf-8 -*-

# https://bitbucket.org/m_c_/sample-dash/src/1e2cfabf58ee0493bc5af73260fb2615de42c8d6/app/as_dash.py?at=master&fileviewer=file-view-default

import datetime as dt

import dash

import pandas as pd
import os

import colorlover as cl
import dash_core_components as dcc
import dash_html_components as html
# import quandl
import json
import requests
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=TAYPN59BT91HYQ90'
from django.conf import settings

colorscale = cl.scales['9']['qual']['Paired']

symbols_file = os.path.join(settings.BASE_DIR, 'nasdaq-company-list.csv')

df_symbol = pd.read_csv(symbols_file)

def dispatcher(request):
    '''
    Main function
    @param request: Request object
    '''

    app = _create_app()
    params = {
        'data': request.body,
        'method': request.method,
        'content_type': request.content_type
    }
    with app.server.test_request_context(request.path, **params):
        app.server.preprocess_request()
        try:
            response = app.server.full_dispatch_request()
        except Exception as e:
            response = app.server.make_response(app.server.handle_exception(e))
        return response.get_data()

# this code can be taken from dash sample codes in github


def _create_app():
    ''' Creates dash application '''

    app = dash.Dash(csrf_protect=False)
    app.layout = html.Div([
        html.Div([
            html.H2('NASDAQ stock ticker',
                    style={'display': 'inline',
                           'float': 'left',
                           'font-size': '2.65em',
                           'margin-left': '7px',
                           'font-weight': 'bolder',
                           'font-family': 'Product Sans',
                           'color': "rgba(117, 117, 117, 0.95)",
                           'margin-top': '20px',
                           'margin-bottom': '0'
                           }),
            html.A('Home', href='/', style={
                'color': 'red',
                'display': 'inline',
                'margin-left': '54%'
            })
        ]),
        dcc.Dropdown(
            id='stock-ticker-input',
            options=[{'label': s[0], 'value': s[1]}
                     for s in zip(df_symbol['Name'], df_symbol['Symbol'])],
            value=['AAPL', 'TSLA'],
            multi=True
        ),
        html.Div(id='graphs'),

    ], className="container")

    @app.callback(
        dash.dependencies.Output('graphs', 'children'),
        [dash.dependencies.Input('stock-ticker-input', 'value')])
    def update_graph(tickers):
        graphs = []
        for i, ticker in enumerate(tickers):
            try:
                # df = DataReader(ticker, 'quandl',
                #                 dt.datetime(2017, 1, 1),
                #                 dt.datetime.now())

                # type(df)df = quandl.get(
                #     "AAPL", start_date="2001-12-31", end_date="2005-12-31")

                # alphavantage api ###
                resp = requests.get(url)
                data = resp.json()
                df = pd.DataFrame.from_dict(
                    data['Time Series (Daily)'], orient='index')
                # with open('data1.json', 'w') as outfile:
                #     json.dump(data, outfile)

                # file = 'data1.json'
                # with open(file) as train_file:
                #     dict_train = json.load(train_file)

                # # converting json dataset from dictionary to dataframe
                # df = pd.DataFrame.from_dict(
                #     dict_train['Time Series (Daily)'], orient='index')
            except:
                graphs.append(html.H3(
                    'Data is not available for {}'.format(ticker),
                    style={'marginTop': 20, 'marginBottom': 20}
                ))
                continue

            candlestick = {
                'x': df.index,
                'open': df['1. open'],
                'high': df['2. high'],
                'low': df['3. low'],
                'close': df['4. close'],
                'type': 'candlestick',
                'name': ticker,
                'legendgroup': ticker,
                'increasing': {'line': {'color': colorscale[0]}},
                'decreasing': {'line': {'color': colorscale[1]}}
            }
            bb_bands = bbands(df['4. close'])
            bollinger_traces = [{
                'x': df.index, 'y': y,
                'type': 'scatter', 'mode': 'lines',
                'line': {'width': 1, 'color': colorscale[(i*2) % len(colorscale)]},
                'hoverinfo': 'none',
                'legendgroup': ticker,
                'showlegend': True if i == 0 else False,
                'name': '{} - bollinger bands'.format(ticker)
            } for i, y in enumerate(bb_bands)]
            graphs.append(dcc.Graph(
                id=ticker,
                figure={
                    'data': [candlestick] + bollinger_traces,
                    'layout': {
                        'margin': {'b': 0, 'r': 10, 'l': 60, 't': 0},
                        'legend': {'x': 0}
                    }
                }
            ))

        return graphs

    return app


def bbands(price, window_size=10, num_of_std=5):
    rolling_mean = price.rolling(window=window_size).mean()
    rolling_std = price.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std*num_of_std)
    lower_band = rolling_mean - (rolling_std*num_of_std)
    return rolling_mean, upper_band, lower_band


if __name__ == '__main__':
    app = _create_app()
    app.run_server()
