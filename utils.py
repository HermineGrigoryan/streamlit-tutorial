import pandas as pd
import numpy as np
import plotly.express as px

def top_barplot(data, x, y, col, n_obs):
    fig = px.bar(data.sort_values(x, ascending=False).iloc[:n_obs].sort_values(x),
     x = x, y = y, color = col)
    fig.update_layout(xaxis={'categoryorder':'total descending'},
    title = f'Top {n_obs} hotels with the highest {x}')
    return fig

def distribution_box(data, x, y, col):
    fig = px.box(data, x = x, y = y, color = col)
    fig.update_layout(title = f'Distribution of {y} per {x}')
    return fig

def scatter_plot(data, x, y, col):
    fig = px.scatter(data, x = x, y = y, color = col)
    fig.update_layout(title = f'Relationship between {x} and {y}')
    return fig