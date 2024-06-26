import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load the data
data_por = pd.read_csv('student-por.csv')

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Define the layout of the app
app.layout = html.Div([
    html.H1("Social Support and Study Habits"),

    # Two graphs side by side using a flexbox layout
    html.Div(
        children=[
            dcc.Graph(id='heatmap-graph', style={'width': '48%', 'display': 'inline-block'}),
            dcc.Graph(id='bar-chart-graph', style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%'})
        ],
        style={'display': 'flex', 'justifyContent': 'center'}
    ),

    # Slider positioned below the two graphs wrapped in a div for styling
    html.Div(
        dcc.RangeSlider(
            id='grade-slider',
            min=data_por['G3'].min(),
            max=data_por['G3'].max(),
            value=[data_por['G3'].min(), data_por['G3'].max()],
            marks={i: str(i) for i in range(data_por['G3'].min(), data_por['G3'].max() + 1, 2)},
            step=1,
            tooltip={"placement": "bottom", "always_visible": True}
        ),
        style={'width': '80%', 'margin': 'auto', 'marginTop': '20px'}
    )
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
        title='Study Time vs Final Grades Heatmap',
        labels={'studytime': 'Study Time (hours per week)', 'G3': 'Final Grade'}
    )
    return fig_heatmap

# Callback to update bar chart
@app.callback(
    Output('bar-chart-graph', 'figure'),
    Input('grade-slider', 'value')
)
def update_bar_chart(grade_range):
    # Filter the data based on the grade range
    filtered_data = data_por[(data_por['G3'] >= grade_range[0]) & (data_por['G3'] <= grade_range[1])]
    
    # Count the occurrences of each support type and calculate percentages
    total_count = len(filtered_data)
    support_counts = {
        'Family Support': (filtered_data['famsup'] == 'yes').sum() / total_count * 100,
        'School Support': (filtered_data['schoolsup'] == 'yes').sum() / total_count * 100,
        'Romantic Relationships': (filtered_data['romantic'] == 'yes').sum() / total_count * 100
    }
    
    # Create the bar chart with percentages
    fig_bar = px.bar(
        x=list(support_counts.keys()),
        y=list(support_counts.values()),
        title='Prevalence of Support Types Among Students',
        labels={'x': 'Type of Support', 'y': 'Percentage (%)'}
    )
    return fig_bar

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
