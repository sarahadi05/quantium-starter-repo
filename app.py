import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import datetime

# Load data
df = pd.read_csv('output.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

app = dash.Dash(__name__)

app.layout = html.Div(style={
    'backgroundColor': '#f8f0f5',
    'fontFamily': 'Arial',
    'padding': '20px'
}, children=[

    html.H1('Soul Foods Pink Morsel Sales Visualiser', style={
        'textAlign': 'center',
        'color': '#8b1a6b',
        'marginBottom': '10px'
    }),

    html.P('Filter by region:', style={
        'textAlign': 'center',
        'color': '#555',
        'marginBottom': '5px'
    }),

    dcc.RadioItems(
        id='region-filter',
        options=[
            {'label': 'All', 'value': 'all'},
            {'label': 'North', 'value': 'north'},
            {'label': 'East', 'value': 'east'},
            {'label': 'South', 'value': 'south'},
            {'label': 'West', 'value': 'west'},
        ],
        value='all',
        inline=True,
        style={
            'textAlign': 'center',
            'marginBottom': '20px',
            'fontSize': '16px',
            'color': '#8b1a6b'
        }
    ),

    dcc.Graph(id='sales-chart')
])

@app.callback(
    Output('sales-chart', 'figure'),
    Input('region-filter', 'value')
)
def update_chart(region):
    if region == 'all':
        filtered = df.groupby('date')['sales'].sum().reset_index()
    else:
        filtered = df[df['region'] == region].groupby('date')['sales'].sum().reset_index()

    fig = px.line(filtered, x='date', y='sales',
                  labels={'date': 'Date', 'sales': 'Sales ($)'},
                  title=f'Pink Morsel Sales Over Time — {region.capitalize()}')

    fig.add_vline(
        x=datetime.datetime(2021, 1, 15).timestamp() * 1000,
        line_dash='dash', line_color='red',
        annotation_text='Price Increase'
    )

    fig.update_layout(
        plot_bgcolor='#fff0fa',
        paper_bgcolor='#f8f0f5',
        font_color='#8b1a6b',
        title_font_size=18
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)
