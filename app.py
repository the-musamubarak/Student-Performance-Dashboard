# Import necessary libraries
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Create the Dash app instance
app = dash.Dash(__name__)

# Expose the server for Gunicorn
server = app.server  # This is the WSGI application that Gunicorn uses

# Sample data
data = {
    'Subject': ['Math', 'Science', 'English', 'History', 'Geography'],
    'Average Score': [85, 90, 80, 75, 88]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Create the bar chart
fig = px.bar(df, x='Subject', y='Average Score', title="Average Scores by Subject")

# Layout of the app
app.layout = html.Div([
    html.H1("Student Performance Dashboard"),
    dcc.Graph(figure=fig)
])

# Run the server if executed locally
if __name__ == '__main__':
    print("Starting Dash server...")
    app.run_server(debug=True)




