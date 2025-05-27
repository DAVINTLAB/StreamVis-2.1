import plotly.graph_objects as go

def create_toxic_types_chart(toxic_types):
    """
    Creates a bar chart for toxic types.

    Args:
        toxic_types (dict): A dictionary containing toxic types and their counts.

    Returns:
        plotly.graph_objects.Figure: A Plotly bar chart figure.
    """
    fig = go.Figure(data=[
        go.Bar(
            x=list(toxic_types.keys()),
            y=list(toxic_types.values()),
            marker_color='indianred'
        )
    ])

    fig.update_layout(
        title='Toxic Types Distribution',
        xaxis_title='Toxic Type',
        yaxis_title='Count',
        template='plotly_white'
    )

    return fig