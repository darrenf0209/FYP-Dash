import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

alt1_data = pd.read_csv("data\\alternative_1_20200527.csv")
alt1_graph = go.Scatter(x=alt1_data['Iteration'],
                        y=alt1_data['PSNR'],
                        name="Alt1")

data = [alt1_graph]
layout = dict(title="Alternative 1", showlegend=False)
fig = dict(data=data, layout=layout)
# print(alt1_data['Loss'])

# Initialising the app
app = dash.Dash(__name__, update_title=None)

# Container of div and html elements
app.layout = html.Div([

    html.Div([
        html.H1('Supervised Causal Video Super-Resolution'),
        html.Img(src="assets\\Monash-University-Logo.png"),
    ],
        className="banner"),
    html.Div(
        html.H2('Darren Flaks'),
        className="banner"
    ),

    html.Label(
        "Model Training Results"
    ),

    html.Div(
        dcc.Dropdown(
            options=[
                {'label': 'Control', 'value': 'Control'},
                {'label': 'Null', 'value': 'Null'},
                {'label': 'Alternative', 'value': 'Alt'}
            ]
        )
    ),

    html.Div(
        dcc.Graph(
            id="Alt 1 Training",
            figure=fig
        )
    )

])

if __name__ == "__main__":
    app.run_server(debug=True)
