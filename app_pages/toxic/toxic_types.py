import json
from output.charts.toxic_types_chart import create_toxic_types_chart
from output.counts.all_toxic_type_count import get_all_toxic_type_count
from output.counts.toxic_type_counts import count_toxic_types
from output.filter.toxic_types_filter import toxic_types_filter
from output.wordclouds.wordcloud import gerar_nuvem_palavras
import plotly.graph_objects as go
import streamlit as st

def toxic_types_page(path: str = 'input/oscar_comments.json'):
    """
    Returns page for toxic types analysis.
    This function sets up the Streamlit page configuration and sidebar selection for toxic types analysis.
    """
    data = json.load(open(path, 'r', encoding='utf-8'))

    def create_gauge_chart(title, value):
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": title, "font": {"size": 24}},
            gauge={
                'axis': {'range': [0, 1]},
                'bar': {'color': "red"},
                'steps': [
                    {'range': [0, 0.7], 'color': "lightgray"},
                    {'range': [0.7, 1], 'color': "red"}
                ]
            }
        ))
        return fig

    st.title('Toxic Types Analysis')
    st.plotly_chart(create_gauge_chart(
        "Toxic Types Count",
        get_all_toxic_type_count(path)
    ), use_container_width=True)
    
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
        toxic_data = toxic_types_filter(data, toxic_type)
        if(toxic_data.__len__() == 0):
            st.warning(f'No data found for {toxic_type}.')
            return
        gerar_nuvem_palavras(toxic_data, toxic_type)
        st.image(
            f'output/wordclouds/images/nuvem_palavras{toxic_type}.png',
            caption=f'Wordcloud for {toxic_type}',
            use_container_width=True
        )
        
    