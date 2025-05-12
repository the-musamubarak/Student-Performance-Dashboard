import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server  # Expose the Flask server to be used by Gunicorn

# Make the server also accessible as 'app' for Gunicorn
application = app.server  # This is for AWS Elastic Beanstalk
app.server.config['PROPAGATE_EXCEPTIONS'] = True  # Optional but helpful for debugging

# Sample data (replace this with your actual data or load from CSV)
data = {
    'Subject': ['Math', 'English', 'Biology', 'Chemistry', 'Physics'],
    'Average Score': [75, 82, 70, 68, 74]
}
df = pd.DataFrame(data)

# Create a Plotly figure
fig = px.bar(df, x='Subject', y='Average Score', title='Average Scores by Subject')

# Define the layout
app.layout = html.Div(children=[
    html.H1('Student Performance Dashboard', style={'textAlign': 'center'}),
    dcc.Graph(id='score-chart', figure=fig)
])

# Run the server locally (used for development only)
if __name__ == '__main__':
    app.run_server(debug=True)



