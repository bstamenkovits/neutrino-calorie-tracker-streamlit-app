import pandas as pd
import plotly.express as px

def construct_bar_chart(consumed, total_allowed):
    if consumed< total_allowed:
        data = pd.DataFrame(
            {
                "day": ["today"],
                "consumed": [consumed],
                "remaining": [total_allowed-consumed],
            }
        )

        fig = px.bar(
            data,
            x=["consumed", "remaining"],
            y="day",
            orientation="h",
            color_discrete_map={"consumed": "#2ca02c", "remaining": "#d3d3d3"},
        )
    else:
        data = pd.DataFrame(
            {
                "day": ["today"],
                "allowed": [total_allowed],
                "excess": [consumed-total_allowed],
            }
        )

        fig = px.bar(
            data,
            x=["allowed", "excess"],
            y="day",
            orientation="h",
            color_discrete_map={"allowed": "#2ca02c", "excess": "#d62728"},
        )

    fig.update_xaxes(title_text="Calories")
    fig.update_yaxes(title_text=None, showticklabels=False)
    fig.update_layout(height=150, showlegend=False)
    return fig
