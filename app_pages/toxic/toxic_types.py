import json
from output.charts.toxic_types_chart import create_toxic_types_chart
from output.counts.toxic_type_counts import count_toxic_types
from output.filter.toxic_types_filter import toxic_types_filter
import streamlit as st

def toxic_types_page(path: str = 'input/oscar_comments.json'):
    """
    Returns page for toxic types analysis.
    This function sets up the Streamlit page configuration and sidebar selection for toxic types analysis.
    """
    data = json.load(open(path, 'r', encoding='utf-8'))

    st.title('Toxic Types Analysis')
    with st.expander('Toxic Types in General', expanded=True):
        st.plotly_chart(
            create_toxic_types_chart(
                count_toxic_types(path)
            ),
            use_container_width=True
        )
    
    toxic_type = st.selectbox(
        'Select a toxic type to analyze',
        [
            'toxicity',
            'severe_toxicity',
            'obscene',
            'identity_attack',
            'insult',
            'threat',
            'sexual_explicit'
        ]
    )

    with st.expander(f'{toxic_type} Analysis', expanded=True):
        st.dataframe(
            data=toxic_types_filter(data, toxic_type),
            use_container_width=True
        )

    with st.expander(f'{toxic_type} Wordclouds', expanded=True):
        st.write(f'Wordclouds for {toxic_type} will be displayed here.')
        