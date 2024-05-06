import pandas as pd
from math import floor, log10
from ast import literal_eval
from Styler import * 
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.image_in_tables import table_with_images



pas_path = r'Steamlit_Spotify/Data/Artist.csv'
PAS_data = pd.read_csv(pas_path)

playlist_url = "https://open.spotify.com/playlist/4Z5uQy7BPvZDZD67mFEdy8"

N_sig_top = len(PAS_data) if len(PAS_data) < 5 else 5
N_sig_recent = len(PAS_data) if len(PAS_data) < 10 else 10

string_len_short = 7
string_len_long = 15


st.set_page_config(layout="wide")

#Headers
st.markdown(f'<p style="{style_h1}">InsurX</p> <p style="{style_h3}"> Made for <span style="{style_italic}">Binding</span>, Born for <span style="{style_italic}">Vibing</span></p>', unsafe_allow_html=True)
st.markdown(f'<p style="{style_p}">Find the artist InsurX has insured and check out the <a href={playlist_url}>playlist</a>!</p>', unsafe_allow_html=True)
st.markdown(f'<p> </p>', unsafe_allow_html=True)
st.markdown(f'<p> </p>', unsafe_allow_html=True)
artist_unique = PAS_data.groupby('Mastered Name').first().reset_index()[['Mastered Name', 'Image URL', 'Genre']]

# Top Artist by GWP and Commission

#Artist sorted by sum Premium
col1, col2, col3 = st.columns([3,1,5])
      
with col1:
   with st.container():

      artist_total_GWP = PAS_data.groupby('Mastered Name').sum().reset_index().sort_values(['Premium'], ascending=False)
      artist_total_GWP['Premium'] = '$' + (artist_total_GWP['Premium'].astype(float)/1e6).round(3).astype(str) + 'M'
      artist_total_GWP = artist_total_GWP[['Mastered Name','Premium']].merge(artist_unique, on = 'Mastered Name', how = 'left')
      artist_total_GWP = artist_total_GWP[['Image URL','Mastered Name','Premium']]

      # st.header()
      st.markdown(f'<p style="{style_text_heading_left}">Top Artist - Total GWP</p>', unsafe_allow_html=True)
      st.markdown(f'<p> </p>', unsafe_allow_html=True)
      st.markdown(f'<p> </p>', unsafe_allow_html=True)
      
      for i in range(N_sig_top):
         artist = artist_total_GWP.iloc[i]

         r_col1, r_col2, r_col3 = st.columns([1,3,2])

         with r_col1:
            st.markdown(f'<img src="{artist["Image URL"]}" style="{style_image1}">',unsafe_allow_html=True,)
         with r_col2:
            name = artist["Mastered Name"]
            name = (name[:string_len_long] + '..') if len(name) > string_len_long else name
            st.markdown(f'<p style="{style_text_left}">{name}</p>', unsafe_allow_html=True)
            # st.subheader()
         with r_col3:
            st.markdown(f'<p style="{style_text_right}">{artist["Premium"]}</p>', unsafe_allow_html=True)
         

# st.markdown(f'<p> </p>', unsafe_allow_html=True)

with col3:
   with st.container():
      PAS_data_recent = PAS_data.copy(deep=True)

      PAS_data_recent['dateBound'] = pd.to_datetime(PAS_data_recent['dateBound'], format = "%d/%m/%Y")

      PAS_data_recent = PAS_data_recent.sort_values(['dateBound'], ascending=False)
      PAS_data_recent['dateBound'] = PAS_data_recent['dateBound'].dt.strftime('%m/%y')
      PAS_data_recent['Premium'] = '$' + (PAS_data['Premium'].astype(float)/1e6).round(3).astype(str) + 'M'
      PAS_data_recent['Genre'] = PAS_data_recent['Genre'].apply(literal_eval)

      st.markdown(f'<p style="{style_text_heading_left}">Recent Artist - Sorted by Date Bound</p>', unsafe_allow_html=True)
      st.markdown(f'<p> </p>', unsafe_allow_html=True)
      st.markdown(f'<p> </p>', unsafe_allow_html=True)

      for i in range(N_sig_recent):
         artist = PAS_data_recent.iloc[i]

         r_col1, r_col2, r_col3, r_col4, r_col5  = st.columns([1,3,2,2,2])

         with r_col1:
            st.markdown(f'<img src="{artist["Image URL"]}" style="{style_image1}">',unsafe_allow_html=True,)
         with r_col2:
            st.markdown(f'<p style="{style_text_left}">{artist["Mastered Name"]}</p>', unsafe_allow_html=True)
         with r_col3:
            try:
               genre = artist["Genre"][0].capitalize()
               genre = (genre[:string_len_short] + '..') if len(genre) > string_len_short else genre
            except:
               genre = ''
            st.markdown(f'<p style="{style_text_left}">{genre}</p>', unsafe_allow_html=True)
         with r_col4:
            st.markdown(f'<p style="{style_text_right}">{artist["dateBound"]}</p>', unsafe_allow_html=True)
         with r_col5:
            st.markdown(f'<p style="{style_text_right}">{artist["Premium"]}</p>', unsafe_allow_html=True)

