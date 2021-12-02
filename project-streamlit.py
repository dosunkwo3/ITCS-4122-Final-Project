import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
df1= pd.read_csv("crime-incidents-1.csv",low_memory=False)
df1 = df1.rename(columns={'incident_id': 'ID', 'case_number': 'Case Number','incident_datetime': 'Date','incident_type_primary': 'Primary Type','incident_description':'Description'})
df1.insert(3,'Year',pd.to_datetime(df1['Date']).dt.year)
df1 = df1.drop(columns=['clearance_type', 'address_1', 'address_2', 'city', 'created_at', 'updated_at', 'location', 'hour_of_day', 'day_of_week', 'parent_incident_type', 'Council Districts', 'Police Districts', 'Zip Codes', 'Tracts', 'state', 'zip', 'latitude', 'longitude' ])
sourceA = pd.DataFrame()
sourceA.insert(0,'Year',df1['Year'])
sourceA.insert(1,'CountA',1)
sourceA = sourceA.groupby('Year').sum()
sourceA = sourceA.reset_index()
sourceA = sourceA[sourceA['Year']>=2009]
colors = ['green','yellow','red']
A = alt.Chart(sourceA, title='Crimes Reported in Buffalo, NY from 2009 to 2018').mark_bar(size = 30).encode(
    alt.X('Year',
          axis=alt.Axis(format='.0f',title='Years of Crime'),
          scale=alt.Scale(domain=(2009,2018))
         ),
    alt.Y('CountA',
         axis=alt.Axis(title='Number of Crimes Reported')),
    color=alt.Color('CountA', scale=alt.Scale(range=colors)),
).configure_axis(
    grid=False
).properties(
    width=700
)
df2 = pd.read_csv("Crimes 2009 - 2018.csv", low_memory=False)
df2 = df2.drop(columns=['Block', 'IUCR', 'Location Description', 'Arrest', 'Domestic', 'Beat', 'Ward', 'FBI Code', 'X Coordinate', 'Y Coordinate', 'Latitude', 'Longitude'])
df2 = df2.drop(3106044)
sourceB = pd.DataFrame()
sourceB.insert(0,'Year',df2['Year'])
sourceB.insert(1,'CountB',1)
sourceB = sourceB.groupby('Year').sum()
sourceB = sourceB.reset_index()
sourceB = sourceB[sourceB['Year']>=2009]

colors = ['green','yellow','red']
B = alt.Chart(sourceB, title='Crimes Reported in Chicago, IL from 2009 to 2018').mark_bar(size = 30).encode(
    alt.X('Year',
          axis=alt.Axis(format='.0f',title='Years of Crime'),
          scale=alt.Scale(domain=(2009,2018))
         ),
    alt.Y('CountB',
         axis=alt.Axis(title='Number of Crimes Reported')),
    color=alt.Color('CountB', scale=alt.Scale(range=colors)),
).configure_axis(
    grid=False
).properties(
    width=700
)
full_source = sourceA.merge(sourceB, how='inner', on='Year')
full_source = full_source.set_index('Year')
base = alt.Chart(full_source.reset_index()).encode(x='Year')

alt.layer(
    base.mark_line(color='blue', point=alt.OverlayMarkDef(color="yellow")).encode(y=alt.Y('CountA' + ':Q', title='Crime Count'), tooltip=['Year', 'CountA'],),
    base.mark_line(color='red', point=alt.OverlayMarkDef(color="yellow")).encode(y='CountB', tooltip=['Year', 'CountB'])
).configure_axis(
    grid=False
).properties(
    width=700
)
full_source = sourceA.merge(sourceB, how='inner', on='Year')
full_source = full_source.set_index('Year')
base = alt.Chart(full_source.reset_index()).encode(x='Year')

trend_chart = alt.layer(
    base.mark_line(color='blue', point=alt.OverlayMarkDef(color="yellow")).encode(y=alt.Y('CountA' + ':Q', title='Crime Count'), tooltip=['Year', 'CountA'],),
    base.mark_line(color='red', point=alt.OverlayMarkDef(color="yellow")).encode(y='CountB', tooltip=['Year', 'CountB'])
).configure_axis(
    grid=False
).properties(
    width=700
)

display = st.sidebar.radio(
    "Select a display",
    ('Buffalo, NY', 'Chicago, IL', 'Trend Comparison'))
if display == 'Buffalo, NY':
    st.header('Buffalo, NY')
    st.write('Buffalo Crime Data')
    st.write(df1)
    st.write(A)
elif display == 'Chicago, IL':
    st.header('Chicago, IL')
    st.write('Chicago Crime Data')
    st.write(df2.head(99))
    st.write(B)
elif display == 'Trend Comparison':
    st.header('Trend Comparison')
    st.write('Trend Data')
    st.write(trend_chart)