import plotly.graph_objects as go

# Data for the funnel chart
labels = ["Before Sentiment Analysis", "After Sentiment Analysis", "Customers Interested after reaching out"]
values = [20, 16, 4]

# Create a funnel chart using plotly.graph_objects
fig = go.Figure(go.Funnel(
    y=labels,
    x=values,
    textinfo="value+percent initial",
    textposition="inside",
    marker=dict(color=["royalblue", "darkblue", "midnightblue"]),
    opacity=0.75
))

# Set layout and display the chart
fig.update_layout(
    title="Target Customer Funnel Chart",
    height=400,
    funnelmode="stack",
    paper_bgcolor="lightgray",
    font=dict(size=14)
)

fig.show()