import json
import streamlit as st
from v2.output.charts.sentiment_types_chart import create_sentiment_types_chart
from v2.output.counts.sentiment_type_counts import count_sentiment_types
from v2.output.charts.negativity_gauge_meter import *

@st.cache_data
def load_and_process_data(path: str):
    """
    Loads the JSON, converts time strings to seconds and returns the data
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for comment in data:
            comment['time_in_seconds'] = time_str_to_seconds(comment.get('time_elapsed', '0:0'))
        
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        st.error(f"Erro ao carregar o arquivo JSON em '{path}': {e}")
        return []

def sentiment_analysis_page(path:str = 'input/comments.json'):
    """
    Returns page for sentiment types analysis.
    This function sets up the Streamlit page configuration and sidebar selection for sentiment types analysis.
    """
    data = load_and_process_data(path)
    # Adiciona o tempo em segundos a cada comentário para facilitar a filtragem (o json nao sera modificado)
    for comment in data:
        comment['time_in_seconds'] = time_str_to_seconds(comment.get('time_elapsed', '0:0'))
    
    st.title('Sentiment Analysis using Pysentimiento')

    with st.expander("Negativity Gauge Meter", expanded=True):
        if not data:
            st.warning("No data available.")
            return

        # Define os limites do slider
        min_time = data[0]['time_in_seconds']
        max_time = data[-1]['time_in_seconds']

        # Cria o slider de tempo
        selected_seconds = st.slider(
            label="Select the video/stream timestamp:",
            min_value=min_time,
            max_value=max_time,
            value=max_time
        )

        st.info(f"**Timestamp selected:** `{seconds_to_time_str(selected_seconds)}`")

        # Filtra os comentários até o tempo selecionado
        filtered_data = [c for c in data if c['time_in_seconds'] <= selected_seconds]

        # Calcula a porcentagem de negatividade
        if not filtered_data:
            negativity_percentage = 0.0
        else:
            total_comments = len(filtered_data)
            negative_comments = sum(1 for c in filtered_data if c.get('sentiment') == 'NEG')
            negativity_percentage = (negative_comments / total_comments) * 100 if total_comments > 0 else 0

        # Cria e exibe o gauge       
        st.plotly_chart(
            create_negativity_gauge(negativity_percentage),
            use_container_width=True
        )

    # Grafico de barra com porcentagens de todos sentimentos em geral
    with st.expander('Sentiment Types in General', expanded=True):
        st.plotly_chart(
            create_sentiment_types_chart(
                count_sentiment_types(path)
            ),
            use_container_width=True
        )
    
