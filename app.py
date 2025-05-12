import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

# Load data
df = pd.read_csv("StudentsPerformance.csv")

# Compute average scores
average_scores = df[['MathScore', 'ReadingScore', 'WritingScore']].mean()

# Create histogram of all scores
score_fig = px.histogram(
    df.melt(value_vars=['MathScore', 'ReadingScore', 'WritingScore']),
    x="value",
    color="variable",
    barmode="overlay",
    title="Distribution of Exam Scores"
)

# Create bar chart of average scores
average_fig = px.bar(
    x=average_scores.index,
    y=average_scores.values,
    labels={'x': 'Subject', 'y': 'Average Score'},
    title="Average Scores by Subject"
)

# Create the Dash app
app = Dash(__name__)
server = app.server  # for deploying on Render

# Define layout
app.layout = html.Div([
    html.H1("Student Performance Dashboard", style={'textAlign': 'center'}),
    
    html.Div([
        html.H2("Score Distribution"),
        dcc.Graph(figure=score_fig)
    ]),

    html.Div([
        html.H2("Average Scores"),
        dcc.Graph(figure=average_fig)
    ])
])

if __name__ == "__main__":
    app.run_server(debug=True)



