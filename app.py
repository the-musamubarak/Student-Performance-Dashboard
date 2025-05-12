import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output

# Load data
df = pd.read_csv("StudentsPerformance.csv")

# Rename columns for consistency
df.columns = df.columns.str.strip()
df.rename(columns={
    'MathScore': 'Math Score',
    'ReadingScore': 'Reading Score',
    'WritingScore': 'Writing Score'
}, inplace=True)

# Create Dash app
app = dash.Dash(__name__)
server = app.server

# App layout
app.layout = html.Div([
    html.H1("Student Performance Dashboard", style={'textAlign': 'center', 'color': '#2c3e50'}),

    html.Div([
        html.Div([
            html.Label("Select Subject"),
            dcc.Dropdown(
                id='subject-dropdown',
                options=[
                    {'label': 'Math Score', 'value': 'Math Score'},
                    {'label': 'Reading Score', 'value': 'Reading Score'},
                    {'label': 'Writing Score', 'value': 'Writing Score'}
                ],
                value='Math Score'
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '3%'}),

        html.Div([
            html.Label("Group By"),
            dcc.Dropdown(
                id='groupby-dropdown',
                options=[
                    {'label': 'Gender', 'value': 'Gender'},
                    {'label': 'Ethnic Group', 'value': 'EthnicGroup'},
                    {'label': 'Parental Education', 'value': 'ParentEduc'},
                    {'label': 'Lunch Type', 'value': 'LunchType'},
                    {'label': 'Test Preparation', 'value': 'TestPrep'}
                ],
                value='Gender'
            )
        ], style={'width': '30%', 'display': 'inline-block'})
    ], style={'padding': '10px'}),

    dcc.Graph(id='boxplot-graph'),

    html.Hr(),

    html.Div([
        html.H4("Average Scores by Category", style={'textAlign': 'center'}),
        dcc.Graph(id='avg-bar-chart')
    ]),

    html.Hr(),

    html.Div([
        html.H4("Distribution of Scores", style={'textAlign': 'center'}),
        dcc.Graph(id='score-distribution')
    ])
], style={'fontFamily': 'Arial', 'backgroundColor': '#f9f9f9', 'padding': '20px'})

# Callback for boxplot and grouped bar chart
@app.callback(
    [Output('boxplot-graph', 'figure'),
     Output('avg-bar-chart', 'figure'),
     Output('score-distribution', 'figure')],
    [Input('subject-dropdown', 'value'),
     Input('groupby-dropdown', 'value')]
)
def update_graphs(subject, groupby):
    box_fig = px.box(df, x=groupby, y=subject, color=groupby,
                     title=f"{subject} by {groupby}",
                     labels={groupby: groupby, subject: subject})

    avg_scores = df.groupby(groupby)[subject].mean().reset_index()
    bar_fig = px.bar(avg_scores, x=groupby, y=subject, color=groupby,
                     title=f"Average {subject} by {groupby}",
                     labels={groupby: groupby, subject: f"Average {subject}"})

    melted_df = df.melt(value_vars=['Math Score', 'Reading Score', 'Writing Score'],
                        var_name='Subject', value_name='Score')
    hist_fig = px.histogram(melted_df, x='Score', color='Subject', barmode='overlay',
                            title="Distribution of All Scores")

    return box_fig, bar_fig, hist_fig

if __name__ == '__main__':
    app.run_server(debug=True)



