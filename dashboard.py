import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np
import requests
import random
from PIL import Image
from io import BytesIO

import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv("data_cleaned.csv")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

#app.logger.info('Logging')
#iptables -t filter -A INPUT -p tcp --dport 8050 -j ACCEPT

### APP LAYOUT ###
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[

                ### Header Section ###
                html.Div(
                    className="row header",
                    children=[
                        html.Div(
                            className="five columns",
                            children=[
                                html.H2("Quilt.AI Coding Challenge - FIFA Team Comparer",
                                style={
                                    'textAlign': 'center',
                                        'color': 'white'
                                }),
                            ],
                        ),
                        html.Div(
                            className="three columns div-for-dropdown",
                            children=[
                                # Dropdown for club1
                                dcc.Dropdown(
                                    id="club1-dropdown",
                                    options=[
                                        {"label": i, "value": i}
                                        for i in sorted(list(set(df['Club'])))
                                    ],
                                    placeholder="Select first Club",
                                )
                            ],
                        ),
                        html.Div(
                            className="three columns div-for-dropdown",
                            children=[
                                # Dropdown for club2
                                dcc.Dropdown(
                                    id="club2-dropdown",
                                    options=[
                                        {"label": i, "value": i}
                                        for i in sorted(list(set(df['Club'])))
                                    ],
                                    placeholder="Select second Club",
                                )
                            ],
                        ),
                    ],
                ),

                ### Dashboard Section ###
                html.Div(
                    className="plots-container ",
                    children=[
                        # Overview Section
                        html.H2("Overview", style={'margin-bottom': '5%'}, className='Title'),

                        # Nationality Barplot w/ tabs + Skills Radar
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="one-half column",
                                    children=[
                                        html.Div([
                                            dcc.Tabs(id="tabs", value='tab-1', children=[
                                                dcc.Tab(label='Club 1', value='tab-1', id='tab-1'),
                                                dcc.Tab(label='Club 2', value='tab-2', id='tab-2'),
                                            ]),
                                            dcc.Loading(
                                                color='#2BB3B0',
                                                type='dot',
                                                style={'margin-top':'10%', 'margin-bottom':'10%'},
                                                children=[
                                                    html.Div(
                                                        id='tabs-content',
                                                        children=[
                                                            dcc.Graph(id='flags-scatter',
                                                                      figure={
                                                                        'layout': {
                                                                            'title': 'Nationality Distribution'
                                                                        }
                                                                    }),
                                                        ])
                                                ])
                                        ]),
                                    ],
                                ),

                                html.Div(
                                    className="one-half column  ",
                                    children=[
                                        dcc.Loading(
                                            color='#2BB3B0',
                                            type='dot',
                                            fullscreen=True,
                                            children=[
                                                dcc.Graph(id='skills-radar',
                                                          figure={
                                                            'layout': {
                                                                'title': 'Skills Radar'
                                                            }
                                                        }),
                                            ],
                                        ),
                                ]),
                            ],
                        ),

                        dcc.Loading(
                            color='#2BB3B0',
                            type='dot',
                            fullscreen=True,
                            children=[
                                # Age Hist + Position Barplot
                                html.Div(
                                    className="row",
                                    children=[
                                        html.Div(
                                            className="four columns",
                                            children=[
                                                dcc.Graph(id='player-age-histogram',
                                                          figure={
                                                            'layout': {
                                                                'title': 'Age Distribution'
                                                            }
                                                        }),
                                            ],
                                        ),
                                        html.Div(
                                            className="eight columns",
                                            children=[
                                                dcc.Graph(id='position-barplot'),
                                            ],
                                        ),
                                    ],
                                ),
                                # Height / Weight Hist
                                html.Div(
                                    className="row",
                                    children=[
                                        html.Div(
                                            className="one-half column",
                                            children=[
                                                dcc.Graph(id='height-boxplot',
                                                          figure={
                                                            'layout': {
                                                                'title': 'Height Distribution'
                                                            }
                                                        }),
                                            ],
                                        ),
                                        html.Div(
                                            className="one-half column",
                                            children=[
                                                dcc.Graph(id='weight-boxplot',
                                                          figure={
                                                            'layout': {
                                                                'title': 'Weight Distribution'
                                                            }
                                                        }),
                                            ],
                                        ),
                                    ],
                                ),
                        ]),

                        #Top 5 Players Plot
                        dcc.Loading(
                            color='#2BB3B0',
                            type='dot',
                            style={'margin-top':'10%', 'margin-bottom':'10%'},
                            children=[
                                html.Div(
                                    className="row",
                                    children=[
                                        html.Div(
                                            className="one-half column",
                                            style={'text-align': 'center'},
                                            children=[
                                                dcc.Graph(id='club1-top-players',
                                                          figure={
                                                            'layout': {
                                                                'title': 'Top 5 Players by Rating & Position'
                                                            }
                                                        }),
                                        ]),
                                        html.Div(
                                            className="one-half column",
                                            children=[
                                                dcc.Graph(id='club2-top-players',
                                                          figure={
                                                            'layout': {
                                                                'title': 'Top 5 Players by Rating & Position'
                                                            }
                                                        }),
                                        ]),
                                    ]),
                            ]),

                        #Radio Button for Position
                        dcc.RadioItems(id='position-radio',
                            options=[
                                {'label': 'GoalKeeper', 'value': '[GK]'},
                                {'label': 'Defender', 'value': '[RB, CB, LB, RWB, LWB, LCB, RCB]'},
                                {'label': 'Center', 'value': '[RM, LM, CM, LCM, RCM, CDM, LDM, RDM, CAM, LAM, RAM]'},
                                {'label': 'Attacker', 'value': '[LW, LS, RS, RW, CF, ST, LF, RF]'},
                            ],
                            value='[GK]',
                            labelStyle={'display': 'inline-block',},
                            style={'text-align':'center', 'zoom':'120%'}
                        ),

                        # Skills Section
                        html.H2("Skills", style={}, className='Title'),

                        # Special Score BarPlot + Skills Moves Pie
                        dcc.Loading(
                            color='#2BB3B0',
                            type='dot',
                            fullscreen=True,
                            children=[
                                html.Div(
                                    className="row",
                                    children=[
                                        html.Div(
                                            className="one-half column",
                                            children=[
                                                dcc.Graph(id='special-histogram',
                                                          figure={
                                                            'layout': {
                                                                'title': 'Special Score Distribution'
                                                            }
                                                        }),
                                            ],
                                        ),
                                        html.Div(
                                            className="three columns",
                                            children=[
                                                dcc.Graph(id='club1-skill-moves-pie',
                                                          figure={
                                                            'layout': {
                                                                'title': 'Skill Moves Repartition'
                                                            }
                                                        }),
                                            ],
                                        ),
                                        html.Div(
                                            className="three columns",
                                            children=[
                                                dcc.Graph(id='club2-skill-moves-pie',
                                                          figure={
                                                            'layout': {
                                                                'title': 'Skill Moves Repartition'
                                                            }
                                                        }),
                                            ],
                                        ),
                                    ],
                                ),

                                # Financial Section
                                html.H2("Financial", style={}, className='Title'),

                                # Value / Wage Hist
                                html.Div(
                                    className="row",
                                    children=[
                                        html.Div(
                                            className="one-half column",
                                            children=[
                                                dcc.Graph(id='player-value-histogram',
                                                          figure={
                                                            'layout': {
                                                                'title': 'Value Distribution'
                                                            }
                                                        }),
                                            ],
                                        ),
                                        html.Div(
                                            className="one-half column",
                                            children=[
                                                dcc.Graph(id='player-wage-histogram',
                                                          figure={
                                                            'layout': {
                                                                'title': 'Wage Distribution'
                                                            }
                                                        }),
                                            ],
                                        ),
                                    ],
                                ),

                                # Value by Rating & Wage Plot
                                dcc.Graph(id='value-rating-scatter',
                                          figure={
                                            'layout': {
                                                'title': 'Value by Rating | Sized by Wage'
                                            }
                                        }),

                                # General Section
                                html.H2("General", style={}, className='Title'),

                                # Pref / Weak Foot Barplot + International Rep Pie
                                html.Div(
                                    className="row",
                                    children=[
                                        html.Div(
                                            className="three columns",
                                            children=[
                                                dcc.Graph(id='player-pref-foot-barplot'),
                                            ],
                                        ),
                                        html.Div(
                                            className="three columns",
                                            children=[
                                                dcc.Graph(id='weak-foot-barplot'),
                                            ],
                                        ),
                                        html.Div(
                                            className="three columns",
                                            children=[
                                                dcc.Graph(id='club1-ir-pie',
                                                          figure={
                                                            'layout': {
                                                                'title': 'International Rep.'
                                                            }
                                                        }),
                                            ],
                                        ),
                                        html.Div(
                                            className="three columns",
                                            children=[
                                                dcc.Graph(id='club2-ir-pie',
                                                          figure={
                                                            'layout': {
                                                                'title': 'International Rep.'
                                                            }
                                                        }),
                                            ],
                                        ),
                                    ],
                                ),
                        ]),
                    ],
                ),
            ],
        )
    ]
)


### APP CALLBACKS ###
@app.callback(
    Output('player-age-histogram', 'figure'),
    [Input('club1-dropdown', 'value'), Input('club2-dropdown', 'value')])
def update_output(club1, club2):
    return px.histogram(df[(df['Club'] == club1) | (df['Club'] == club2)], x="Age", color="Club", marginal="box", hover_data=df.columns, color_discrete_sequence=['#2BB3B0', '#B277A7']).update_layout(
    title={
        'text': "Age Distribution",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})

@app.callback(
    [Output('height-boxplot', 'figure'), Output('weight-boxplot', 'figure')],
    [Input('club1-dropdown', 'value'), Input('club2-dropdown', 'value')])
def update_output(club1, club2):
    return (px.box(df[(df['Club'] == club1) | (df['Club'] == club2)], x="Club", y="Height", color="Club", points="all", color_discrete_sequence=['#2BB3B0', '#B277A7']).update_layout(
    title={
        'text': "Height Distribution",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}),
    px.box(df[(df['Club'] == club1) | (df['Club'] == club2)], x="Club", y="Weight", color="Club", points="all", color_discrete_sequence=['#2BB3B0', '#B277A7']).update_layout(
    title={
        'text': "Weight Distribution",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}))

@app.callback(
    Output('player-value-histogram', 'figure'),
    [Input('club1-dropdown', 'value'), Input('club2-dropdown', 'value')])
def update_output(club1, club2):
    return px.histogram(df[(df['Club'] == club1) | (df['Club'] == club2)], x="Value", color="Club", marginal="box", hover_data=df.columns, color_discrete_sequence=['#2BB3B0', '#B277A7']).update_layout(
    title={
        'text': "Value Distribution",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})

@app.callback(
    Output('player-wage-histogram', 'figure'),
    [Input('club1-dropdown', 'value'), Input('club2-dropdown', 'value')])
def update_output(club1, club2):
    return px.histogram(df[(df["Club"] == club1) | (df['Club'] == club2)], x="Wage", color="Club", marginal="box", hover_data=df.columns, color_discrete_sequence=['#2BB3B0', '#B277A7']).update_layout(
    title={
        'text': "Wage Distribution",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})

@app.callback(
    Output('value-rating-scatter', 'figure'),
    [Input('club1-dropdown', 'value'), Input('club2-dropdown', 'value')])
def update_output(club1, club2):
    return px.scatter(df[(df['Club'] == club1) | (df['Club'] == club2)], x="Value", y="Rating", color="Club", size="Wage", color_discrete_sequence=['#2BB3B0', '#B277A7']).update_layout(
    title={
        'text': "Value by Rating - Sized by Wage",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})

@app.callback(
    Output('player-pref-foot-barplot', 'figure'),
    [Input('club1-dropdown', 'value'), Input('club2-dropdown', 'value')])
def update_output(club1, club2):
    return {
        'data': [
            {'x': ['Right', 'Left'], 'y': [len(df[(df['Club'] == club1) & (df['Preferred Foot'] == 'Right')]), len(df[(df['Club'] == club1) & (df['Preferred Foot'] == 'Left')])], 'type': 'bar', 'name': club1},
            {'x': ['Right', 'Left'], 'y': [len(df[(df['Club'] == club2) & (df['Preferred Foot'] == 'Right')]), len(df[(df['Club'] == club2) & (df['Preferred Foot'] == 'Left')])], 'type': 'bar', 'name': club2},
        ],
        'layout': {
            'title': 'Most Preferred Foot Distribution',
            'colorway': ['#2BB3B0', '#B277A7']
        }
    }

@app.callback(
    Output('weak-foot-barplot', 'figure'),
    [Input('club1-dropdown', 'value'), Input('club2-dropdown', 'value')])
def update_output(club1, club2):
    return {
        'data': [
            {'x': ['1', '2', '3', '4', '5'], 'y': np.unique(df[(df['Club'] == club1)]['Weak Foot'], return_counts=True)[1], 'type': 'bar', 'name': club1},
            {'x': ['1', '2', '3', '4', '5'], 'y': np.unique(df[(df['Club'] == club2)]['Weak Foot'], return_counts=True)[1], 'type': 'bar', 'name': club2},
        ],
        'layout': {
            'title': 'Weak Foot Distribution',
            'colorway': ['#2BB3B0', '#B277A7']
        }
    }

@app.callback(
    [Output('club1-skill-moves-pie', 'figure'), Output('club2-skill-moves-pie', 'figure')],
    [Input('club1-dropdown', 'value'), Input('club2-dropdown', 'value')])
def update_output(club1, club2):
    return (px.pie(df[(df["Club"] == club1)], values="Skill Moves", names="Skill Moves", color_discrete_sequence=['#2BB3B0', '#B277A7']).update_layout(
    title={
        'text': 'Skill Moves Rep. for ' + club1,
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}),
    px.pie(df[(df['Club'] == club2)], values="Skill Moves", names="Skill Moves", color_discrete_sequence=['#2BB3B0', '#B277A7']).update_layout(
    title={
        'text': 'Skill Moves Rep. for ' + club2,
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}))

@app.callback(
    Output('skills-radar', 'figure'),
    [Input('club1-dropdown', 'value'), Input('club2-dropdown', 'value')])
def update_output(club1, club2):
    skills = ['General', 'Mental', 'Mobility', 'Power', 'Shooting', 'Passing','Defending', 'Goalkeeping', 'Rating']
    return go.Figure(
        data = [
            go.Scatterpolar(
                r=df[(df["Club"] == club1)].loc[: , ['General', 'Mental', 'Mobility', 'Power', 'Shooting', 'Passing','Defending', 'Goalkeeping', 'Rating']].median(),
                theta=skills,
                fill='toself',
                name=club1
            ),
            go.Scatterpolar(
                r=df[(df["Club"] == club2)].loc[: , ['General', 'Mental', 'Mobility', 'Power', 'Shooting', 'Passing','Defending', 'Goalkeeping', 'Rating']].median(),
                theta=skills,
                fill='toself',
                name=club2
            )
        ],
        layout = go.Layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title={
                'text': 'Skills Radar',
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            height=550,
            colorway=['#2BB3B0', '#B277A7']
            ),
        )

@app.callback(
    Output('special-histogram', 'figure'),
    [Input('club1-dropdown', 'value'), Input('club2-dropdown', 'value')])
def update_output(club1, club2):
    return px.histogram(df[(df['Club'] == club1) | (df['Club'] == club2)], x="Special", color="Club", marginal="box", hover_data=df.columns, color_discrete_sequence=['#2BB3B0', '#B277A7']).update_layout(
    title={
        'text': 'Special Score Distribution',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})

@app.callback(
    Output('position-barplot', 'figure'),
    [Input('club1-dropdown', 'value'), Input('club2-dropdown', 'value')])
def update_output(club1, club2):
    return {
        'data': [
            {'x': np.unique(df[(df['Club'] == club1)]['Position'], return_counts=True)[0], 'y': np.unique(df[(df['Club'] == club1)]['Position'], return_counts=True)[1], 'type': 'bar', 'name': club1},
            {'x': np.unique(df[(df['Club'] == club2)]['Position'], return_counts=True)[0], 'y': np.unique(df[(df['Club'] == club2)]['Position'], return_counts=True)[1], 'type': 'bar', 'name': club2},
        ],
        'layout': {
            'title': 'Position of the Players',
            'colorway': ['#2BB3B0', '#B277A7']
        }
    }

@app.callback(
    [Output('tab-1', 'label'), Output('tab-2', 'label')],
    [Input('club1-dropdown', 'value'), Input('club2-dropdown', 'value')])
def update_output(club1, club2):
    return 'Club 1' if club1 == None else club1, 'Club 2' if club2 == None else club2

@app.callback(
    Output('flags-scatter', 'figure'),
    [Input('club1-dropdown', 'value'), Input('club2-dropdown', 'value'), Input('tabs', 'value')])
def update_output(club1, club2, tab):
    if tab == 'tab-1':
        club_tab = club1
        color = ['#2BB3B0']
    elif tab == 'tab-2':
        club_tab = club2
        color = ['#B277A7']

    u = np.unique(df[(df["Club"] == club_tab)]['Nationality'], return_counts=True)
    nationality = u[0]
    freq = u[1]

    working_link = {'England':'united-kingdom',  'Wales':'united-kingdom',  'Costa Rica':'costa-rica',  'Bosnia Herzegovina':'bosnia-and-herzegovina',  'Korea Republic':'south-korea',  'Czech Republic':'czech-republic',  'Scotland':'united-kingdom',  'Central African Rep.':'central-african-republic',  'DR Congo':'congo-democratic-republic-of-the',  'Ivory Coast':'cote-d-ivoire',  'Dominican Republic':'dominican-republic',  'Republic of Ireland':'ireland',  'United States':'united-states-of-america',  'Cape Verde':'cape-verde',  'Burkina Faso':'burkina-faso',  'Equatorial Guinea':'equatorial-guinea',  'New Zealand':'new-zealand',  'FYR Macedonia':'macedonia',  'United Arab Emirates':'united-arab-emirates',  'China PR':'china',  'Guinea Bissau':'guinea',  'South Africa':'south-africa',  'Congo':'congo-republic-of-the',  'Northern Ireland':'united-kingdom',  'Saudi Arabia':'saudi-arabia',  'Curacao':'netherlands',  'Trinidad & Tobago':'trinidad-and-tobago',  'Sierra Leone':'sierra-leone',  'São Tomé & Príncipe':'sao-tome-and-principe',  'New Caledonia':'france',  'Korea DPR':'north-korea',  'St Kitts Nevis':'saint-kitts-and-nevis',  'El Salvador':'el-salvador',  'Bermuda':'united-kingdom',  'Antigua & Barbuda':'antigua-and-barbuda',  'Montserrat':'united-kingdom',  'Guam':'united-states-of-america',  'Faroe Islands':'denmark',  'St Lucia':'saint-lucia',  'Puerto Rico':'united-states-of-america',  'Hong Kong':'china',  'South Sudan':'sudan'}

    images = []
    pos = 0
    for nat in nationality:

            if nat in working_link:
                cname = working_link[nat]
            else:
                cname = nat

            response = requests.get("https://cdn.countryflags.com/thumbs/"+cname.lower()+"/flag-round-250.png")
            img = Image.open(BytesIO(response.content))
            images.append(dict(source=img,
                               xref='x',
                               yref='y',
                               x=pos,
                               y=freq[pos],
                               sizex=3,
                               sizey=3,
                               xanchor='center',
                               yanchor='middle'))
            pos+=1

    data = go.Bar(
    x=nationality,
    y=freq,
    hovertext=['{0} {1}'.format(w, f) for w, f in zip(freq, nationality)],
    hoverinfo='text')
    layout = go.Layout({'xaxis': {'showgrid': False, 'showticklabels': True, 'zeroline': False},
                        'yaxis': {'showgrid': False, 'showticklabels': True, 'zeroline': False, 'range':[0, max(freq)+2]},
                        'colorway': color},
                        images=images, title={
                                'text': 'Nationality Distribution',
                                'y':0.95,
                                'x':0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'})

    return go.Figure(data=[data], layout=layout)

@app.callback(
    [Output('club1-ir-pie', 'figure'), Output('club2-ir-pie', 'figure')],
    [Input('club1-dropdown', 'value'), Input('club2-dropdown', 'value')])
def update_output(club1, club2):
    return (px.pie(df[(df["Club"] == club1)], values="International Reputation", names="International Reputation", color_discrete_sequence=['#2BB3B0', '#B277A7']).update_layout(
    title={
        'text': 'International Rep. for '+club1,
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}),
    px.pie(df[(df['Club'] == club2)], values="International Reputation", names="International Reputation", color_discrete_sequence=['#2BB3B0', '#B277A7']).update_layout(
    title={
        'text': 'International Rep. for '+club2,
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}))

def create_top_players_figure(club, playerPosition):
    dff = df[df['Club'] == club].sort_values('Rating', ascending=False)

    images = []
    player_count = 0
    for index, row in dff[dff['Position'].isin(playerPosition)].iterrows():
        if player_count == 5:
            break
        player_count += 1

        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
        headers = {'User-Agent': user_agent}
        try:
            response = requests.get(row['Photo'].replace('.png','@2x.png'), headers=headers)
            img = Image.open(BytesIO(response.content))
        except:
            response = requests.get('https://cdn.sofifa.org/players/4/notfound_0@2x.png', headers=headers)
            img = Image.open(BytesIO(response.content))

        images.append(dict(source=img,
                           xref='x',
                           yref='y',
                           x=row['Name'],
                           y=row['Rating'],
                           sizex=10,
                           sizey=10,
                           xanchor='center',
                           yanchor='middle'))


    data = go.Bar(
    x=dff[dff['Position'].isin(playerPosition)]['Name'].head(5),
    y=dff[dff['Position'].isin(playerPosition)]['Rating'].head(5),
    hovertext=['{0} {1}'.format(w, f) for w, f in zip(dff[dff['Position'].isin(playerPosition)]['Name'].head(5), dff[dff['Position'].isin(playerPosition)]['Rating'].head(5))],
    hoverinfo='text',
    width=0,
    )
    min = dff[dff['Position'].isin(playerPosition)]['Rating'].head(5).min()
    max = dff[dff['Position'].isin(playerPosition)]['Rating'].head(5).max()
    layout = go.Layout({'xaxis': {'showgrid': False, 'showticklabels': True, 'zeroline': False,},
                        'yaxis': {'showgrid': True, 'showticklabels': True, 'zeroline': False, 'range': [min-10, max+10]},
                        },
                        images=images, title={
                                'text': 'Top 5 Players by Rating & Position for ' + club,
                                'y':0.95,
                                'x':0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'})

    return go.Figure(data=[data], layout=layout)

@app.callback(
    [Output('club1-top-players', 'figure'), Output('club2-top-players', 'figure')],
    [Input('club1-dropdown', 'value'), Input('club2-dropdown', 'value'), Input('position-radio', 'value')])
def update_output(club1, club2, playerPosition):
    return (create_top_players_figure(club1, playerPosition.strip('][').split(', ')), create_top_players_figure(club2, playerPosition.strip('][').split(', ')))


if __name__ == '__main__':
    app.run_server(debug=True)
