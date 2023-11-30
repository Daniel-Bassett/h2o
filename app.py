import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu


@st.cache_data
def load_data(dir):
    df = pd.read_csv(dir)
    return df


valid_cities = load_data('accurate_income.csv')
valid_cities = valid_cities.sort_values(by='municipality')


# define function for making map
def make_map(df):
    customdata = np.stack((df['municipality'], df['population_est_2022'], df['median_income_2014'], df['municipality_profile']),  axis=-1)
    color_scale = [
        (0, 'blue'), # Blue for the lowest value
        (1, 'red') # Red for the highest value
    ]
    fig = px.scatter_mapbox(df,
                            lon=df['longitude'],
                            lat=df['latitude'],
                            zoom=5,
                            color=df['median_income_2014'],
                            text=df['municipality'],
                            hover_data=['municipality_profile'],
                            color_continuous_scale=color_scale,
                            range_color=[40000, 55000]
    )
    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(coloraxis_showscale=False)
    fig.update_traces(customdata=customdata, hovertemplate='City: %{customdata[0]}<br>Population: %{customdata[1]}</br>Median Income: %{customdata[2]}<br>href: %{customdata[3]}</br>')
    return fig

st.markdown("""#### Empowering Rural Communities: Sustainable Water Solutions""", unsafe_allow_html=True)
st.divider()

median_income = st.slider('Median Income',  min_value=10000, max_value=55000, value=(10000, 55000), step=1000)

temp_df = valid_cities.query(f'median_income_2014.between({median_income[0]}, {median_income[1]})')

fig = make_map(temp_df)
st.plotly_chart(fig, use_container_width=True)


cities = valid_cities.municipality.unique()
cities = sorted(np.append(cities, '(All Cities)'))
selected_city = st.selectbox('Choose City', options=cities)

temp_df = valid_cities[['municipality', 'population_est_2022', 'median_income_2014', 'municipality_profile']]

if selected_city != '(All Cities)':
    temp_df = temp_df[temp_df['municipality'] == selected_city]

st.data_editor(
    temp_df,
    column_config={
        "municipality_profile": st.column_config.LinkColumn("City Profile")
    },
    hide_index=True,
)