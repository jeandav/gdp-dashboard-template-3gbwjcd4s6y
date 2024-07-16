import streamlit as st
import pandas as pd
import math
from pathlib import Path

import plotly.express as px


# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Titre de la page',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
    layout="centered"
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_gdp_data():
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/traitement_drees/livia_lieux_vie_sc1.csv'
    df = pd.read_csv(DATA_FILENAME, encoding='latin-1', sep=';')

    # df = df[df['genre'] == 'HOMMES']
    # df = df[df['tranche_age'] == '75 ans et plus']
    df = df[df['hyp_evol_dependance'] == 'intermediaire']
    df = df[df['hyp_evol_demo'] == 'central']
    df = df[['ca', 'tranche_age', 'genre', 'annee', 'nb_proj_seniors']]
    df = df.groupby(['ca', 'tranche_age', 'genre', 'annee'])['nb_proj_seniors'].sum()
    df = df.reset_index()


    return df

gdp_df = get_gdp_data()

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.

st.image('https://upload.wikimedia.org/wikipedia/commons/0/06/Minist%C3%A8re_de_la_Justice.svg', width=100)

'''
# Projection et besoins des populations âgées dépendantes entre 2015 et 2050
'''

# Add some spacing
''
''

min_value = gdp_df['annee'].min()
max_value = gdp_df['annee'].max()

from_year = min_value
to_year = max_value

# from_year, to_year = st.slider(
#     'Which years are you interested in?',
#     min_value=min_value,
#     max_value=max_value,
#     value=[min_value, max_value])

countries = gdp_df['ca'].unique()
liste_ca = gdp_df['ca'].unique()

if not len(countries):
    st.warning("Select at least one country")

# selected_countries = st.multiselect(
#     'Sélectionnez un département à afficher',
#     countries,
#     ['Gers', 'Jura', 'La Réunion'])

selected_genre = st.selectbox(
    "Genre :",
    ("FEMMES", "HOMMES"))

selected_trancheage = st.selectbox(
    "Tranche d\'age :",
    ("75 ans et plus", "60-74 ans"))


cluster_options = {
    "Cluster 1" : ['Versailles', 'Paris'],
    "Cluster 2" : ['Angers', 'Dijon', 'Caen', 'Poitiers', 'Riom', 'Bourges', 'Limoges', 'Agen'],
    "Cluster 3" : ['Douai', 'Amiens', 'Chambéry', 'Rouen', 'Grenoble', 'Colmar', 'Lyon', 'Reims', 'Metz', 'Toulouse'],
    "Cluster 4" : ['Rennes', 'Orléans', 'Nancy', 'Besançon', 'Nîmes', 'Aix-en-Provence', 'Montpellier', 'Bordeaux', 'Pau'],
}

chosen_cluster = st.radio(
    "Cluster",
    cluster_options.keys(),
    horizontal=True
)


selected_ca = st.multiselect(
    'Cour d\'appel',
    liste_ca,
    cluster_options[chosen_cluster])
''
''
''

# Filter the data
filtered_gdp_df = gdp_df[
    # (gdp_df['dep2'].isin(selected_countries))
    (gdp_df['ca'].isin(selected_ca))
    & (gdp_df['genre'] == selected_genre)
    & (gdp_df['tranche_age'] == selected_trancheage)
    & (gdp_df['annee'] <= to_year)
    & (from_year <= gdp_df['annee'])
]

# st.header('Nombre de seniors projetés', divider='gray')

''

# st.line_chart(
#     filtered_gdp_df,
#     x='annee',
#     x_label='Année',
#     y='nb_proj_seniors',
#     y_label='Nombre de seniors projetés',
#     color='dep2',
# )


fig = px.line(filtered_gdp_df, x="annee", y="nb_proj_seniors", color='ca', markers=True)
fig.update_layout(
    yaxis_title='Nombre de seniors projetés',
    xaxis_title='Année',
    legend_title=None,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
        )
    )
fig.add_vline(x=2024, line_width=1, line_color="lightgrey")
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})