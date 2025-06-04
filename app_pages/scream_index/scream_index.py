import json
from output.counts.scream_index_counts import scream_index_mean
import streamlit as st
import plotly.graph_objects as go

def scream_index_page(json_file_path:str = 'input/oscar_comments.json'):
    """ Streamlit page to display the Scream Index.
    This function creates a Streamlit page that displays the mean Scream Index
    and a card with the Scream Index value.
    """
    def create_card(title, value, card_color="lightgray", text_color="black"):
        fig = go.Figure(go.Indicator(
            mode="number",
            value=value,
            title={"text": title, "font": {"size": 24, "color": text_color}},
            number={"font": {"size": 40, "color": text_color}},
            domain={'x': [0, 1], 'y': [0, 1]}
        ))
        
        fig.update_layout(
            paper_bgcolor=card_color,
            margin=dict(l=20, r=20, t=50, b=50),
            height=200
        )
        return fig

    st.title('Scream Index Analysis')
    st.plotly_chart(create_card("Mean scream index", scream_index_mean(json_file_path), card_color="red", text_color="white"),
                    use_container_width=True)
    
    with st.expander("Messages above 70 screan index", expanded=True):
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        scream_indices = [obj for obj in data if obj.get('scream_index', 0) > 0.70]
        st.dataframe(
            data=scream_indices,
            use_container_width=True
        )
    