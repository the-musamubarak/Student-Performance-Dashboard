import os
import pandas as pd
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output

# Load the data
df = pd.read_csv('StudentsPerformance.csv')

# Clean column names
df.columns = [col.strip().replace(' ', '_').lower() for col in df.columns]
# Check cleaned column names for reference
# print(df.columns)

# Create folder to save images
output_dir = "graph_images"
os.makedirs(output_dir, exist_ok=True)

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Student Exam Dashboard"

app.layout = dbc.Container([
    html.H1("Student Performance Dashboard", className="text-center my-4"),

    dbc.Row([
        dbc.Col([
            html.Label("Select Gender"),
            dcc.Dropdown(
                id='gender-filter',
                options=[{'label': g, 'value': g} for g in df.gender.unique()],
                value=None,
                placeholder="All Genders"
            ),
        ], md=4),

        dbc.Col([
            html.Label("Select Parental Education Level"),
            dcc.Dropdown(
                id='parental-filter',
                options=[{'label': level, 'value': level} for level in df.parenteduc.unique()],
                value=None,
                placeholder="All Education Levels"
            ),
        ], md=8),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([dcc.Graph(id='score-distribution')], md=6),
        dbc.Col([dcc.Graph(id='score-by-subject')], md=6),
    ])
], fluid=True)

# Callback to update and save plots
@app.callback(
    [Output('score-distribution', 'figure'),
     Output('score-by-subject', 'figure')],
    [Input('gender-filter', 'value'),
     Input('parental-filter', 'value')]
)
def update_graphs(selected_gender, selected_parent_edu):
    filtered_df = df.copy()
    if selected_gender:
        filtered_df = filtered_df[filtered_df.gender == selected_gender]
    if selected_parent_edu:
        filtered_df = filtered_df[filtered_df.parenteduc == selected_parent_edu]

    # 1. Histogram
    fig1 = px.histogram(
        filtered_df.melt(id_vars=['gender'], value_vars=['mathscore', 'readingscore', 'writingscore']),
        x='value', color='variable', barmode='overlay',
        labels={'value': 'Score', 'variable': 'Subject'},
        title="Distribution of Scores"
    )
    fig1.write_image(os.path.join(output_dir, "score_distribution.png"))

    # 2. Average Score Bar Chart
    avg_scores = filtered_df[['mathscore', 'readingscore', 'writingscore']].mean().reset_index()
    avg_scores.columns = ['Subject', 'Average Score']
    fig2 = px.bar(avg_scores, x='Subject', y='Average Score', color='Subject', title="Average Scores by Subject")
    fig2.write_image(os.path.join(output_dir, "average_scores_by_subject.png"))

    return fig1, fig2

# Run the server
if __name__ == '__main__':
    print("Starting Dash server...")
    app.run(debug=True)


