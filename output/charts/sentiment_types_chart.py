import plotly.graph_objects as go

def create_sentiment_types_chart(sentiment_types):
    """
    Creates a bar chart for sentiment types.

    Args:
        sentiment_types (dict): A dictionary containing sentiment types and their counts.

    Returns:
        plotly.graph_objects.Figure: A Plotly bar chart figure.
    """
    total = sum(sentiment_types.values())

    # Cria rótulos com porcentagem
    labels = [
        f"{key} ({(value / total * 100):.1f}%)"
        for key, value in sentiment_types.items()
    ]

    fig = go.Figure(data=[
        go.Bar(
            x=labels,
            y=list(sentiment_types.values()),
            marker_color='indianred'
        )
    ])

    fig.update_layout(
        title='Sentiment Types Distribution',
        xaxis_title='Sentiment Type',
        yaxis_title='Count',
        template='plotly_white'
    )

    return fig
