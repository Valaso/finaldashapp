import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load the data
data_por = pd.read_csv('student-por.csv')

# Initialize the Dash app (optionally add external stylesheets)
app = dash.Dash(__name__)
server = app.server

# Define the layout of the app
app.layout = html.Div([
    html.H1("Student Performance Visualization"),
    dcc.RangeSlider(
        id='grade-slider',
        min=data_por['G3'].min(),
        max=data_por['G3'].max(),
        value=[data_por['G3'].min(), data_por['G3'].max()],
        marks={i: str(i) for i in range(data_por['G3'].min(), data_por['G3'].max()+1, 2)},
        step=1,
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    dcc.Graph(id='heatmap-graph'),
    dcc.Graph(id='bar-chart-graph')
])

# Callback to update heatmap
@app.callback(
    Output('heatmap-graph', 'figure'),
    Input('grade-slider', 'value')
)
def update_heatmap(grade_range):
    filtered_data = data_por[(data_por['G3'] >= grade_range[0]) & (data_por['G3'] <= grade_range[1])]
    fig_heatmap = px.density_heatmap(
        filtered_data,
        x='studytime',
        y='G3',
        title='Heatmap of Study Time vs Grades'
    )
    return fig_heatmap

# Callback to update bar chart
@app.callback(
    Output('bar-chart-graph', 'figure'),
    Input('grade-slider', 'value')
)
def update_bar_chart(grade_range):
    filtered_data = data_por[(data_por['G3'] >= grade_range[0]) & (data_por['G3'] <= grade_range[1])]
    support_counts = {
        'Family Support': (filtered_data['famsup'] == 'yes').sum(),
        'School Support': (filtered_data['schoolsup'] == 'yes').sum(),
        'Romantic Relationships': (filtered_data['romantic'] == 'yes').sum()
    }
    fig_bar = px.bar(
        x=list(support_counts.keys()),
        y=list(support_counts.values()),
        title='Support Count for Selected Grade Range'
    )
    return fig_bar

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
