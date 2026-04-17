import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('output.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

# Group by date for total daily sales
daily = df.groupby('date')['sales'].sum().reset_index()

# Create line chart
fig = px.line(daily, x='date', y='sales',
              labels={'date': 'Date', 'sales': 'Sales ($)'},
              title='Pink Morsel Sales Over Time')

# Add vertical line for price increase
import datetime
fig.add_vline(x=datetime.datetime(2021, 1, 15).timestamp() * 1000,
              line_dash='dash', line_color='red',
              annotation_text='Price Increase')

# Build app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Soul Foods Pink Morsel Sales Visualiser',
            style={'textAlign': 'center', 'fontFamily': 'Arial'}),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run(debug=True)
