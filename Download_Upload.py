'''
To do:
1. Download button to download csv template -> done
2. Upload button to injest contingency exposure
3. QA and Data enhancements:
    1. Check if UMR exist in v_PAS_USD
        -> yes - continue - let user know UMR found in PAS
        -> no - exist - tell user UMR does not exist in PAS
    2. Check if UMR exit in the stagging expsoure db [Contingency_Exposure_Stagging]
        -> yes - continue - tell user UMR already has been capture, it will be overwritten
                -- *UMR Found = True*
        -> no - continue - new entry will be made
    3. Perform pervious QA checks on: 
        1. Date of Event: PAS - check all dates within risk inception and expiry
        2. Country: Check valid country
        3. State: if USA, Check states (or state codes) are valid
        4. Currency: PAS - Check currency is valid and the same as at least on of the currencies for the risk in the PAS 
        5. Gross Guarantees: PAS - if GG provided, check abs(sum of GG - 100% Policy limit) <= 5% of 100% Policy limit for 
        the (valid) currency stated in exposure sheet
    4. Enhacements: 
        -- If QA passed, then continue, please exit and report where QA failed.
        1. Spotify -> Master artist name, genre, image url, premium 100% -> send to -Mastered Artist- table
        2. geolocation -> Azure Atast geolocation -> Lat, Long, geolocation precision (street, state, country)
4. Upload event data to exposure db:
    1. *UMR Found = True*, delete information corresponding to that umr from db
    2. insert artist information
    3. insert event information
'''

import streamlit as st
import pandas as pd
import datetime
import time
from Styler import *


st.set_page_config(layout="wide")


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index = False).encode("utf-8")

columns_events = ['Date','Venue','State','Country', 'Gross Guarantees']
template = pd.DataFrame(columns = columns_events)
csv_template = convert_df(template)



#Headers
st.markdown(f'<p style="{style_h1}">InsurX</p> <p style="{style_h2}">Contingency Exposure Uploader</p>', unsafe_allow_html=True)
st.markdown(f'<p style="{style_p}">Complete the form below and upload a <span style="{style_italic}">csv</span> file with event information to upload the contingency policy exposure! Press the button below to get a template of the csv file. </p>', unsafe_allow_html=True)
st.markdown(f'<p> </p>', unsafe_allow_html=True)
st.markdown(f'<p> </p>', unsafe_allow_html=True)

#Template button
st.download_button(
    label="Download csv template!",
    data=csv_template,
    file_name="Contingency Capture Template.csv",
    mime="text/csv",
    use_container_width = True,
)


col1, _,  col2 = st.columns([4,0.1,5])

with col1:
    #form
    st.markdown(f'<p style="{style_h2}">Complete the following: </p>', unsafe_allow_html=True)

    umr = st.text_input("Policy UMR:", "")

    #Policy Category
    category = st.selectbox("Category:",
    ("Music - Tour", "Festival", "Sport", "Conference", "Other"))

    #Policy subcategory for music -> add additional stuff for other categories
    if category == 'Music - Tour':
        subcat_list = ('Solo Artist', 'Band')
    elif category == 'Sport':
        subcat_list = ('Football', 'Cricket', 'Rugby', 'Tennis', 'Olympics', 'Other')
    else:
        subcat_list = (None, None)
    
    subcategory = st.selectbox("Sub-category:",subcat_list)

    if subcategory == 'Band':
        bandno = st.selectbox("Number of band members:", range(1,11))
    else:
        bandno = 1
    
    if category == 'Music - Tour':
        name_dob_all = []

        col1_1, col1_2 = st.columns([5,2])

        if subcategory == 'Band':
            for i in range(bandno):
                name_dob = {'name':None, "dob":None}
                with col1_1:
                    name_dob['name'] = st.text_input(f"Name {i+1}:", "")
                    
                with col1_2:
                    name_dob['dob'] = st.date_input(f"Date of birth {i+1}:", datetime.date(2000, 1, 1), format="DD/MM/YYYY",
                                                    min_value = datetime.date(1900, 1, 1), max_value = datetime.date(2024, 1, 1))

                name_dob_all.append(name_dob)

        else:
            name_dob = {'name':None, "dob":None}

            with col1_1:
                name_dob['name'] = st.text_input("Name:", "")
            with col1_2:
                name_dob['dob'] = st.date_input("Date of birth:", datetime.date(2000, 1, 1), format="DD/MM/YYYY",
                                                min_value = datetime.date(1900, 1, 1), max_value = datetime.date(2024, 1, 1))
            name_dob_all.append(name_dob)

    #Upload event data csv file
    upload_file = st.file_uploader("Upload Event .csv file:", accept_multiple_files=False, type= ['csv'])
    if upload_file is not None:
        events = pd.read_csv(upload_file)
        st.write(events)

        

with col2:

    #QA and Status information
    st.markdown(f'<p style="{style_h2}">QA and Status: </p>', unsafe_allow_html=True)

    with st.spinner('Wait for it...'):
        time.sleep(5)
        # Do some process
    st.success('Done!', icon="✅")
    st.error('This is an error', icon="🚨")

        

            
            

    





