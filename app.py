import pandas as pd
import dash
from dash import html, dcc
import plotly.express as px

# Load the data
df = pd.read_csv('StudentsPerformance.csv')

# Calculate average scores
average_scores = df[['math score', 'reading score', 'writing score']].mean()

# Create visualizations
score_fig = px.histogram(df.melt(value_vars=['math score', 'reading score', 'writing score']),
                         x='value', color='variable', nbins=20,
                         title='Score Distribution by Subject',
                         labels={'value': 'Score', 'variable': 'Subject'})

average_fig = px.bar(
    x=average_scores.index,
    y=average_scores.values,
    title='Average Scores by Subject',
    labels={'x': 'Subject', 'y': 'Average Score'}
)

# Build the Dash app
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Student Performance Dashboard"),
    dcc.Graph(figure=score_fig),
    dcc.Graph(figure=average_fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)



