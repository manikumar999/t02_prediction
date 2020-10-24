import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from datetime import date
import pickle

import plotly.express as px

app = dash.Dash(__name__)

model = pickle.load(open('qt_t02.pkl','rb'))








app.layout = html.Div([
        html.H1(children = ["Quench Overhead Temperature Prediction"], style ={'textAlign':'center'}),
        
        html.P(["Select the period of dates and model will predict The Quench Overhead Temparature"]),
        dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=date(2017, 10, 17),
        max_date_allowed=date(2021, 1, 1),
        start_date = date(2020,10,17),
        end_date=date(2020,10, 19)
    ),
        dcc.Graph(id = 'output-graph')
        
    
    ],style = {'textAlign':'center'})


@app.callback(
    dash.dependencies.Output('output-graph', 'figure'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_output(start_date, end_date):
    future = pd.DataFrame(pd.date_range(start = start_date,end = end_date,freq='h'))
    future.columns = ['ds']
    forecast = model.predict(future)

    df = forecast[['ds','yhat']]
    
    fig = px.line(df, x="ds", y="yhat", title='Quench Overhead Prediction')
    return fig 

if __name__ =="__main__":
    app.run_server(debug=False)


