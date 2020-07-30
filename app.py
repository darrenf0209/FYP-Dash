import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
import pandas as pd
import os
import glob

data_files = glob.glob("data\\*.csv")
data_files = list(data_files)

alt1_data = pd.read_csv("data\\alternative_1_20200527.csv")
null1_data = pd.read_csv("data\\null_1_20200517.csv")
all_data = [alt1_data, null1_data]

video_dir_lr = "assets\\video_sequences\\low_res"
video_dir_hr = "assets\\video_sequences\\high_res"
videos_lr = [os.path.splitext(vid)[0] for vid in os.listdir(video_dir_lr)]
videos_hr = [os.path.splitext(vid)[0] for vid in os.listdir(video_dir_hr)]

models = ['Alternative', 'Null']
metrics = ['PSNR', 'Loss']

# Initialising the app
app = dash.Dash(__name__, update_title=None)

# Container of div and html elements
app.layout = html.Div([

    # Banner
    html.Div([
        html.H3(
            "Supervised Causal Video Super-Resolution",
            className="eight columns offset-by-one",
            style={
                "text-align": "left"
            },
        ),
        html.Img(
            src="assets/logos/Monash-University-Logo.png",
            className="two columns",
            style={
                "height": "50px",
                "width": "auto",
                "margin-top": "1%",
                "text-align": "right"
            },
        ),
    ],
        className="row",
        style={
            "background-color": "#dcdddf"
        },
    ),

    html.Div([
        html.H4(
            "Darren Flaks",
            className="two columns offset-by-one",
            style={
                "text-align": "left"
            }
        ),
        html.A([
            html.Img(
                src="assets/logos/linked_in_logo.png",
                className="one column",
                style={
                    "width": "auto",
                    "height": "40px",
                    "margin-top": "1.25%",
                    "margin-right": "1%",
                },
            ),
        ],
            href='https://www.linkedin.com/in/darrenflaks/'
        ),
        html.A([
            html.Img(
                src="assets/logos/github_logo.png",
                className="one column",
                style={
                    "width": "auto",
                    "height": "40px",
                    "margin-top": "1.25%",
                },
            ),
        ],
            href='https://github.com/darrenf0209'
        ),
        html.H4(
            "Supervisors: Dr. Titus Tang, Prof. Tom Drummond",
            className="six columns offset-by-two",
            style={
                "text-align": "right",
            },
        ),
    ],
        className="row",
        style={
            "background-color": "#dcdddf"
        },
    ),

    html.Div([
        html.H4('Project Synposis')
    ],
    ),

    html.Div([
        dcc.Markdown(
            "Lorem Ipsum is simply dummy **text** of the printing and typesetting industry. Lorem Ipsum has been the "
            "industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and "
            "scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap "
            "into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the "
            "release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing "
            "software like Aldus PageMaker including versions of Lorem Ipsum ",
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
            html.H4(
                "Input",
            ),
            html.Img(
                id='video_lr',
                style={
                    "width": "100%",
                    "height": "auto"
                },
            ),
        ],
            className="five columns offset-by-one",
        ),

        html.Div([
            html.H4(
                "Output",
            ),
            html.Img(
                id='video_hr',
                style={
                    "width": "100%",
                    "height": "auto"
                },
            ),
        ],
            className="five columns",
        ),
    ],
        className="row",
        style={
            "text-align": "center"
        },
    ),

    html.Div([
        html.H4("Model Training Results")
    ],
    ),

    html.Div([
        html.H6("Model Select",
                className="two columns offset-by-one"),
        html.Div(
            dcc.Dropdown(
                id='model-selector',
                options=[{'label': i, 'value': i} for i in models],
                value='Alternative',
                multi=True,
                className="four columns",
            ),
        ),
        html.Div(
            dcc.Dropdown(
                id='metric-selector',
                options=[{'label': i, 'value': i} for i in metrics],
                value='PSNR',
                className="two columns offset-by-one",
            ),
        ),
    ],
        className="row"
    ),

    html.Div(
        dcc.Graph(
            id='training-results-scatter',
            # id="Alt 1 Training",
            # figure=fig,
            className="ten columns offset-by-one"
        ),
        className="row"
    ),
],
)


@app.callback([
    Output('video_lr', 'src'),
    Output('video_hr', 'src')],
    [Input('video-sequence-selector', 'value')])
def update_video(value):
    src_lr = os.path.join(video_dir_lr, value + '.png')
    src_hr = os.path.join(video_dir_hr, value + '.png')
    return src_lr, src_hr


@app.callback(
    Output('training-results-scatter', 'figure'),
    [Input('model-selector', 'value'),
     Input('metric-selector', 'value')])
def update_graph(model_choice, metric):
    # choice = [model_choice]
    # data_load = []
    # for i in range(0, len(choice)):
    #     print(choice[i])
    #     if models.index(choice[i]) is not None:
    #         index = models.index(choice[i])
    #         # print(data_files[index])
    #         # print(index, type(index))
    #         df = pd.read_csv(data_files[index])
            # print(df['Iterations'])
            # data_load.append(all_data[index])

    # print(data_load)
    # print(models)
    # print(index)
    # data_select = all_data[index]
    graph = go.Scatter(
        x=alt1_data['Iteration'],
        y=alt1_data[metric],
        name="{}".format(model_choice)
    )
    data = [graph]
    layout = dict(title="Alternative 1", showlegend=True)
    fig = dict(data=data, layout=layout)
    return fig



if __name__ == "__main__":
    app.run_server(debug=True)
