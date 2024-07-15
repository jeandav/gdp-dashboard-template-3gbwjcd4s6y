import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Titre de la page',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
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

    df = df[df['genre'] == 'HOMMES']
    df = df[df['tranche_age'] == '75 ans et plus']
    df = df[df['hyp_evol_dependance'] == 'stable']
    df = df[df['hyp_evol_demo'] == 'central']
    df = df[['dep', 'annee', 'nb_proj_seniors']]


    return df

gdp_df = get_gdp_data()

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
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

countries = gdp_df['dep'].unique()

if not len(countries):
    st.warning("Select at least one country")

selected_countries = st.multiselect(
    'Sélectionnez un département à afficher',
    countries,
    ['1', '2'])

''
''
''

# Filter the data
filtered_gdp_df = gdp_df[
    (gdp_df['dep'].isin(selected_countries))
    & (gdp_df['annee'] <= to_year)
    & (from_year <= gdp_df['annee'])
]

st.header('Nombre de seniors projetés', divider='gray')

''

st.line_chart(
    filtered_gdp_df,
    x='annee',
    x_label='Année',
    y='nb_proj_seniors',
    y_label='Nombre de seniors projetés',
    color='dep',
)


'''
Champ : France métropolitaine et DOM (sauf Mayotte)

Source : modèle LIVIA (DREES) et modèle EP24 (INSEE-DREES)
'''

# first_year = gdp_df[gdp_df['annee'] == from_year]
# last_year = gdp_df[gdp_df['annee'] == to_year]

# st.header(f'GDP in {to_year}', divider='gray')

# ''

# cols = st.columns(4)

# for i, country in enumerate(selected_countries):
#     col = cols[i % len(cols)]

#     with col:
#         first_gdp = first_year[gdp_df['dep'] == country]['nb_proj_seniors'].iat[0] / 1000000000
#         last_gdp = last_year[gdp_df['dep'] == country]['nb_proj_seniors'].iat[0] / 1000000000

#         if math.isnan(first_gdp):
#             growth = 'n/a'
#             delta_color = 'off'
#         else:
#             growth = f'{last_gdp / first_gdp:,.2f}x'
#             delta_color = 'normal'

#         st.metric(
#             label=f'{country} GDP',
#             value=f'{last_gdp:,.0f}B',
#             delta=growth,
#             delta_color=delta_color
#         )
