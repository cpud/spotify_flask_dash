import numpy as np
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

spotify = spotipy.Spotify(client_credentials_manager=cc_manager)


def year_dict_dataframe():

    years = ['2017', '2018', '2019', '2020']
    year_df_dict = {}

    for year in years:
        temp = pd.read_csv("data/" + year + '.csv')
        year_df_dict[year] = temp

    return year_df_dict


"""
def year_dict_dataframe():
    #Create Pandas DataFrame from local CSV
    df = pd.read_csv("data/music_data.csv")

    years = ['2017', '2018', '2019', '2020']
    year_df_dict = {}

    for year in years:

        # specific year
        temp = df[df['year'] == year]
        # grab top 100 songs at their most streamed for the given year.
        temp = temp.sort_values(by = 'Streams', ascending = False).drop_duplicates(subset = ['Track Name'])[:100]

        # get songs, artist names
        songs = list(temp['Track Name'])
        artists = list(temp['Artist'])

        # get audio features for 100 of the 200 songs (api limits)
        temp = pd.DataFrame(spotify.audio_features(tracks = list(temp['URL'])))

        # add artists and song names to yearly df
        #temp['Artist'] = artists
        #temp['Track Name'] = songs

        # add to dictionary
        year_df_dict[year] = temp

    return year_df_dict
"""
