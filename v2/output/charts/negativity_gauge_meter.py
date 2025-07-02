import plotly.graph_objects as go
from datetime import timedelta

def time_str_to_seconds(time_str: str) -> int:
    """Converts a time string 'H:M:S' or 'M:S' to seconds."""
    parts = list(map(int, time_str.split(':')))
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    elif len(parts) == 2:
        return parts[0] * 60 + parts[1]
    return 0

def seconds_to_time_str(seconds: int) -> str:
    """Converts seconds to a time string 'HH:MM:SS'."""
    return str(timedelta(seconds=seconds))

def create_negativity_gauge(percentage: float):
    """Creates a gauge meter."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=percentage,
        title={'text': "Level of Negativity (%)"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#d62728"}, # Cor vermelha para negatividade
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 75], 'color': "gray"}
            ],
        }
    ))
    fig.update_layout(height=400)
    return fig