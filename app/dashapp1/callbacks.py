from dash.dependencies import Input
from dash.dependencies import Output
import dash_core_components as dcc
import dash_html_components as html
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import plotly.graph_objects as go

from .data import year_dict_dataframe

# Spotipy docs: https://spotipy.readthedocs.io/en/2.12.0/

spotify = spotipy.Spotify(client_credentials_manager=cc_manager)



year_df_dict = year_dict_dataframe()

def register_callbacks(dashapp):
    @dashapp.callback(Output('radar-chart', 'figure'), [Input('year', 'value')])
    def update_radar(year):
        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r = [year_df_dict[year]['danceability'].mean(), year_df_dict[year]['energy'].mean(),
                 year_df_dict[year]['speechiness'].mean(), year_df_dict[year]['acousticness'].mean(),
                 year_df_dict[year]['instrumentalness'].mean(), year_df_dict[year]['liveness'].mean(),
                 year_df_dict[year]['valence'].mean()],
            theta = ['danceability', 'energy', 'speechiness', 'acousticness',
                     'intstrumentalness', 'liveness', 'valence'],
                fill = 'toself',
                name = 'Yearly Top 100'
        ))

        fig.update_layout(
          polar=dict(
            radialaxis=dict(
              #bgcolor = 'rgb(0,0,0)',
              visible=True,
              range=[0, 1],
              #gridcolor='white',
            ),
            angularaxis = dict(
              #gridcolor='white',
              #visible = False
            )),
          showlegend=True,
          title='Mean Audio Features',
          plot_bgcolor = '#FFFFFF',
          paper_bgcolor = '#FFFFFF',
          font_color = '#3B846D'
          #width=800,
          #height=800
        )
        return fig

    @dashapp.callback(Output('std-bar', 'figure'), [Input('year', 'value')])
    def update_std(year):

        features_list = ['danceability', 'energy', 'speechiness', 'acousticness',
         'intstrumentalness', 'liveness', 'valence']

        # std bar
        fig2 = go.Figure(data=[
            go.Bar(name='std', x=features_list, y=[year_df_dict[year]['danceability'].std(), year_df_dict[year]['energy'].std(),
                                                year_df_dict[year]['speechiness'].std(), year_df_dict[year]['acousticness'].std(),
                                                year_df_dict[year]['instrumentalness'].std(), year_df_dict[year]['liveness'].std(),
                                                year_df_dict[year]['valence'].std()]),
            go.Bar(name='mean', x=features_list, y=[year_df_dict[year]['danceability'].mean(), year_df_dict[year]['energy'].mean(),
                                                year_df_dict[year]['speechiness'].mean(), year_df_dict[year]['acousticness'].mean(),
                                                year_df_dict[year]['instrumentalness'].mean(), year_df_dict[year]['liveness'].mean(),
                                                year_df_dict[year]['valence'].mean()]),
        ])

        # std bar
        fig2.update_layout(barmode='group',
                           font_color = '#3B846D',
                           colorway = ['#1f77b4', '#d62728'],
                           title = 'Standard Deviation vs Mean',)

        return fig2

    @dashapp.callback(Output('search-radar', 'figure'), [Input('spotify_url', 'value')])
    def user_radar(spotify_url):
        # get audio features for track, put in dataframe
        features = pd.DataFrame(spotify.audio_features(str(spotify_url)))

        # radar
        fig = go.Figure()

        # chart doesn't work without the .mean()? strange
        # doesn't matter for one song anyways but still weird
        fig.add_trace(go.Scatterpolar(
            r = [features['danceability'].mean(), features['energy'].mean(),
                 features['speechiness'].mean(), features['acousticness'].mean(),
                 features['instrumentalness'].mean(), features['liveness'].mean(),
                 features['valence'].mean()],
            theta = ['danceability', 'energy', 'speechiness', 'acousticness',
                     'intstrumentalness', 'liveness', 'valence'],
                fill = 'toself',
                name = 'Selected Song'
        ))

        # radar
        fig.update_layout(
          polar=dict(
            radialaxis=dict(
              visible=True,
              range=[0, 1]
            )),
          showlegend=True,
          title='Song Features',
          font_color = '#3B846D',
          colorway = ['#2ca02c']
        )

        return fig

    @dashapp.callback(Output('user-table', 'children'), [Input('year', 'value')])
    def generate_table(year, max_rows = 20):
        dataframe = year_df_dict[year]
        dataframe['Year'] = year
        dataframe = dataframe.reindex(columns = ['Track Name', 'Artist',
                                        'Year', 'danceability',
                                        'energy', 'speechiness',
                                        'acousticness','instrumentalness',
                                        'liveness', 'valence', 'tempo', 'uri'])
        dataframe = dataframe.round(3)
        return html.Table([
            html.Thead(
                html.Tr([html.Th(col) for col in dataframe.columns]),
            ),
            html.Tbody([
                html.Tr([
                    html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
                ]) for i in range(min(len(dataframe), max_rows))
            ],#style = {'width': '50%'}
                        )
        ], style = {'background-color': '#FFFFFF',
                    'color': '#3B846D',
                    #'width': '49%'
                    #'font-style': 'italic'
                    })
