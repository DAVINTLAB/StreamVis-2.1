from app_pages.scream_index.scream_index import scream_index_page
from app_pages.toxic.toxic_types import toxic_types_page
import streamlit as st

st.set_page_config(
    page_title='Views',
    page_icon='📊',
    layout='wide',
    menu_items={'Get Help': None, 'Report a Bug': None, 'About': None}
)

secao = st.sidebar.selectbox(
    'Select a section',
    ['Toxic Speech', 'Scream Index', 'Sentiment Analysis'],
)

match secao:
    case 'Toxic Speech':
        toxic_types_page()

    case 'Scream Index':
        scream_index_page()
    case 'Sentiment Analysis':
        st.title('Sentiment Analysis')
        st.write('This section is for Sentiment Analysis.')
        st.write('You can upload your data and analyze it here.')