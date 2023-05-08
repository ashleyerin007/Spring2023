from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd
#import plotly.graph_objects as go
import sql_calls

# pandas dataframe from show_table query results
df_basic = sql_calls.show_table()

# pandas dataframe from scatterp query results
df_scatter = sql_calls.scatterp()

# generate list of values for drop-down menus
menu_options = sql_calls.get_list()

# list of values for radio buttons
best_schools = sql_calls.top_schools()

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in df_basic.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df_basic.iloc[i][col]) for col in df_basic.columns
            ]) for i in range(min(len(df_basic), max_rows))
        ])
    ])

app = Dash(__name__)

colors = {
    'background': '#b39292',
    'text': '#7FDBFF'
}

# generate scatter plot
scatterpl = px.scatter(df_scatter, x="name", y="frequency", size="frequency", color="name")

# layout made up of a tree of components like html.Div tags and dcc.Graph

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    # generates h1 HTML element in the app
    # children property is always the first attribute and as such can be omitted
    # below is the same as html.H1('Hello Dash') and can contain a string, number, or component(s)
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A web application framework for your data.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Br(),

    html.Div(children='Example of a basic table output: ', style={
        'textAlign': 'left',
        'color': colors['text']
        }),

    # output static table
    generate_table(df_basic),

    html.Br(),

    # output scatter plot
    html.Div([
        dcc.Graph(
            id = 'keyword_scater',
            figure = scatterpl
            )
        ]),

    html.Br(),

    # core components
    html.Div(children=[
        html.Label('Dropdown'),
        html.Br(),
        dcc.Dropdown(
            id='journals-dropdown',
            options=[{'label':venue, 'value': venue} for venue in menu_options],
        ), 

        #style={'width': '75%', 'display': 'flex', 'flexWrap': 'wrap'},

        html.Br(),

        html.Label('Multi-Select Dropdown'),
        dcc.Dropdown(
            id='journals-multi',
            options=[{'label':venue, 'value': venue} for venue in menu_options],
                     multi=True),

        html.Br(),

        html.Label('Radio Items'),
        dcc.RadioItems(
            # how to specify best_schools[0] as default selected here?
            id='schools-radio',
            options=[{'label': name, 'value': name} for name in best_schools], 
            style={'padding': 10, 'flex': 1}),

        html.Br(),
        html.Label('Checkboxes'),
        dcc.Checklist(
            id='schools-checkboxes',
            options=[{'label': name, 'value': name} for name in best_schools],
                ),

        html.Br(),
        html.Label('Text Input'),
        dcc.Input(value='Add your school', type='text'),


        html.Br(),
        html.Br(),
        html.Label('Slider'),
        dcc.Slider(
            min=0,
            max=9,
            marks={i: f'Label {i}' if i == 1 else str(i) for i in range(1, 6)},
            value=5,
            ),
        ], style={'padding': 10, 'flex': 1}),

    # look up flex
    # style={'display': 'flex', 'flex-direction': 'row'}

        html.Br()
    ])

if __name__ == '__main__':
    app.run_server(debug=True)