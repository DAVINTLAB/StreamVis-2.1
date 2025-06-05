import json
import streamlit as st
from output.charts.sentiment_types_chart import create_sentiment_types_chart
from output.counts.sentiment_type_counts import count_sentiment_types

def sentiment_analysis_page(path:str = 'input/oscar_comments.json'):
    """
    Returns page for sentiment types analysis.
    This function sets up the Streamlit page configuration and sidebar selection for sentiment types analysis.
    """
    data = json.load(open(path, 'r', encoding='utf-8'))

    st.title('Sentiment Analysis')

    with st.expander('Sentiment Types in General', expanded=True):
        st.plotly_chart(
            create_sentiment_types_chart(
                count_sentiment_types(path)
            ),
            use_container_width=True
        )
    
