import dash_core_components as dcc
import dash_html_components as html

descriptions = ["Danceability doesn't vary much, so it's safe to say that most of these songs are quite danceable. ",
              "Energy is similar, but these songs seem to hover around 0.5 or so, which means that they all feel somewhat fast, loud, and noisy. Death metal is considered high energy, while a Bach prelude is considered low energy.",
             "Acousticness is low but varies quite a bit. However, this is a confidence measure, so all this means is that Spotify is fairly certain these tracks aren't acoustic.",
             "Instrumentalness - a value above 0.5 implies the track is purely instrumental. These are not. ",
             "Liveness detects the presence of an audience, with a value of 0.8 impying high confidence that the track is played live. These tracks are not near that level of confidence.",
             "Valence detects 'positiveness' with 1.0 being very 'happy', 'cheerful', or 'euphoric', while a low valence implies that song could be 'sad', 'depressed', or 'angry'. The valence for these tracks show that they're somewhere near the middle, leaning more towards sad than happy.",
               ]

from .data import year_dict_dataframe

year_dict_df = year_dict_dataframe()

li_style = {'color': '#3B846D',
            'font-style': 'italic',
            'font-weight': 'bold'}

layout = html.Div([

    html.Title('Yearly Spotify Thingamajig'),

    # dropdowns
    html.Div([
        html.Label('Year', style = {'font-weight': 'bold',
                                    }),
        dcc.Dropdown(
            id = 'year',
            options = [
                {'label': '2017', 'value': '2017'},
                 {'label': '2018', 'value': '2018'},
                 {'label': '2019', 'value': '2019'},
                 {'label': '2020', 'value': '2020'},
            ],
            value = '2020',
            style = {'width': '98%'}),
        html.H4('*Data pulled from SpotifyCharts Weekly US Top 200 from 2017 - 2020',
                style = {'font-style': 'italic'})
    ],
    style = {'width': '98%',
             'columnCount': 2,
             #'display': 'inline-block'
            }),

    # radar chart for yearly top 100
    html.Div([
        dcc.Graph(
        id = 'radar-chart'),
        # radar description
        #html.H2(' this is where words can be',
        #       style = {'font-size': '16px'}),
    ], style = {'width': '49%',
                'display': 'inline-block'}
    ),

    # std bar for yearly top 100
    html.Div([
        dcc.Graph(
        id = 'std-bar'),
        # std description
        #html.H2('more words can appear!?!?!',
        #       style = {'font-size': '16px'}),
        ], style = {'width': '49%',
                    'display': 'inline-block'}
    ),

    # analysis/descriptions
    html.Div([
        html.Ul(children = [
            html.Li(desc, style = li_style) for desc in descriptions
        ]),
    ], style = {'width': '98%',
                'display': 'inline-block',
                #'border': '5px solid black'
               }),

    html.H2('Some of the songs included in the analylsis:'),

    # table of songs for selected year
    html.Div(id = 'user-table',
             style = {'display': 'inline-block',
                      #'width': '60%'
                                     }
                      ),

    html.H2('Enter a spotify song url like the one below, or copy and paste a uri\
    from above to get the audio features for that song!'),

    # enduser enter song radar thing
    html.Div([
        dcc.Input(id = 'spotify_url',
                  type = 'text',
                  value = 'https://open.spotify.com/track/0bAkKNCQfWkexHFn7fIKns',
                  style = {'width': '50%'}),
        dcc.Graph(
        id = 'search-radar'),

    ], style = {'width': '60%',
                'display': 'inline-block',
                #'columnCount': 2
                }),



], #style = {'columnCount': 1}
)
