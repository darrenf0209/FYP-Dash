import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
import pandas as pd
import os


alt1_data = pd.read_csv("data\\alternative_1_20200527.csv")
alt1_graph = go.Scatter(x=alt1_data['Iteration'],
                        y=alt1_data['PSNR'],
                        name="Alt1")

data = [alt1_graph]
layout = dict(title="Alternative 1", showlegend=False)
fig = dict(data=data, layout=layout)
# print(alt1_data['Loss'])

video_dir_lr = "assets\\video_sequences\\low_res"
video_dir_hr = "assets\\video_sequences\\high_res"
videos_lr = [os.path.splitext(vid)[0] for vid in os.listdir(video_dir_lr)]
videos_hr = [os.path.splitext(vid)[0] for vid in os.listdir(video_dir_hr)]
print(videos_lr)
print(videos_hr)


# Initialising the app
app = dash.Dash(__name__, update_title=None)

# Container of div and html elements
app.layout = html.Div([

    html.Div([
        html.H1(
            'Supervised Causal Video Super-Resolution',
        ),
        html.Img(
            src="assets\\Monash-University-Logo.png"
        ),
    ],
        className="banner"),
    html.Div([
        html.H2('Darren Flaks')
    ],
        className="banner",
        style={
            "text-align": "center"
        },
    ),

    html.Div([
        html.H4('Project Synposis')
    ], ),

    html.Div([
        html.Div([
            "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the "
            "industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and "
            "scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap "
            "into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the "
            "release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing "
            "software like Aldus PageMaker including versions of Lorem Ipsum "
        ],
            className="eight columns offset-by-two",
            style={
                "text-align": "justify",
                "text-justify": "inter-word"
            },
        ),
    ],
        className="row"
    ),


    html.Div([
        html.H4('Visual Results of 2x Video Super-Resolution')
    ]),

    html.Div([
        html.Div([
            "Video sequence",
        ],
            className="two columns offset-by-one",
            style={
                "padding-top": "0.5%",
                "padding-left": "3%"
            }
        ),
        dcc.Dropdown(
            id='video-sequence-selector',
            options=[{'label': i, 'value': i} for i in videos_lr],
            # options=[
            #     {'label': 'Fast-moving', 'value': 'Fast-moving'},
            #     {'label': 'Slow-moving', 'value': 'Slow-moving'},
            #     {'label': 'High Contrast', 'value': 'High Contrast'},
            #     {'label': 'Lots of Edges', 'value': 'Lots of Edges'},
            #     {'label': 'Vibrant Color', 'value': 'Vibrant Color'},
            #     {'label': 'Black and White', 'value': 'Black and White'},
            # ],
            value=videos_lr[0],
            clearable=False,
            className="two columns",
        ),
    ],
        className="row",
        style={
            "padding-top": "0.5%",
            "padding-bottom": "0.5%"
        }),

    html.Div([
        html.Div([
            # html.Div(id='dd-video-sequence'),
            html.H4(
                "Input",
            ),
            html.Img(
                id='video_lr'
                # src="assets/video_sequences/ezgif.com-gif-maker.gif",
            ),
        ],
            className="six columns",
        ),

        html.Div([
            html.H4(
                "Output",
            ),
            html.Img(
                id='video_hr'
                # src="assets/video_sequences/ezgif.com-gif-maker (1).gif",
            ),
        ],
            className="six columns",
        ),
    ],
        className="row",
        style={
            "text-align": "center"
        },
    ),

    html.Div([
        html.H4("Model Training Results")
    ], ),

    html.Div(
        dcc.Dropdown(
            options=[
                {'label': 'Control', 'value': 'Control'},
                {'label': 'Null', 'value': 'Null'},
                {'label': 'Alternative', 'value': 'Alt'},
            ],
            multi=True,
        ),
    ),

    html.Div(
        dcc.Graph(
            id="Alt 1 Training",
            figure=fig,
        ),
    ),
])


@app.callback([
    Output('video_lr', 'src'),
    Output('video_hr', 'src')],
    [Input('video-sequence-selector', 'value')])
def updateVideo(value):
    src_lr = os.path.join(video_dir_lr, value + '.png')
    src_hr = os.path.join(video_dir_hr, value + '.png')
    return src_lr, src_hr


if __name__ == "__main__":
    app.run_server(debug=True)
