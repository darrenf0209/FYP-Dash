import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
import pandas as pd
import os
import flask

# ---------------------------------------------------------------
df = pd.read_csv("data/training_data_merged.csv")
df_mean = df.groupby(["Model", "Iteration"], as_index=False)[["PSNR", "Loss", "Training Time (s)"]].mean()
df_mean = df_mean[["Model", "Iteration", "PSNR", "Loss", "Training Time (s)"]]

# ---------------------------------------------------------------

video_dir_lr = "assets/video_sequences/low_res_compressed"
video_dir_hr = "assets/video_sequences/high_res_compressed"
videos_lr = sorted([os.path.splitext(vid)[0] for vid in os.listdir(video_dir_lr)])
videos_hr = sorted([os.path.splitext(vid)[0] for vid in os.listdir(video_dir_hr)])

models = ('Alternative', 'Control (3)', 'Control (5)', 'Control (7)', 'Null')
metrics = ('PSNR', 'Loss', 'Training Time (s)')

server = flask.Flask(__name__)

@server.route('/')
def index():
    return 'Hello World'

# Initialising the app
app = dash.Dash(
    __name__,
    server=server,
    routes_pathname_prefix='/dash/',
    update_title=None
)
# server = app.server

app.title = "Darren's FYP"

# Container of div and html elements
app.layout = html.Div([

    # Banner
    html.Div([
        html.H3(
            "Supervised Causal Video Super-Resolution",
            className="six columns offset-by-three",
            style={
                "text-align": "center",
                "font-weight": "bold",
            },
        ),
        html.Img(
            src="assets/logos/Monash-University-Logo.png",
            className="three columns",
            style={
                "height": "40px",
                "width": "auto",
                "margin-top": "2%",
            },
        ),
    ],
        className="row",
        style={
            "background-color": "#dcdddf"
        },
    ),

    html.Div([
        html.H5(
            "Darren Flaks",
            className="two columns offset-by-one",
            style={
                "text-align": "left"
            },
        ),
        html.A([
            html.Img(
                src="assets/logos/linkedin-logo.png",
                className="one column",
                style={
                    "width": "auto",
                    "height": "30px",
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
                    "height": "30px",
                    "margin-top": "1.25%",
                },
            ),
        ],
            href='https://github.com/darrenf0209'
        ),
        dcc.Markdown(
            "Supervisors: [Dr. Titus Tang](https://scholar.google.com.au/citations?user=lBfZ9rgAAAAJ&hl=en), "
            "[Prof. Tom Drummond](https://scholar.google.com.au/citations?user=6sWGL5wAAAAJ&hl=en)",
            className="six columns offset-by-two",
            id="header-links",
            style={
                "text-align": "right",
                "padding-right": "2%",
                "font-size": "2.2rem",
                "margin-bottom": "1.4rem",
                "margin-top": "1.4rem"
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
            '''
            
            This dashboard is a snapshot of my Final-Year Project (Honours) in Electrical and Computer Systems 
            Engineering at Monash University in the field of deep learning and computer vision. This research 
            project investigates if spatial information of a video frame is a more important factor than the 
            temporal correlation across multiple frames. The motivation for this project is proposing a novel 
            approach for applying video-super resolution with a causal network. This may lead to real-time 
            applications, such as teleconferencing or live video feeds, that can rely upon a deep-learning network 
            for higher quality. With thanks to the original authors of the _Progressive Fusion Video Super-Resolution 
            Network via Exploiting Non-Local Spatio-Temporal Correlations_ (PFNL) [research paper]
            (https://openaccess.thecvf.com/content_ICCV_2019/html/Yi_Progressive_Fusion_Video_Super-Resolution_Network_via_Exploiting_Non-Local_Spatio-Temporal_Correlations_ICCV_2019_paper.html) 
            and [github](https://github.com/psychopa4/PFNL) for laying the foundation of this project. 
            
            ''',
            className="ten columns offset-by-one",
            style={
                "text-align": "justify",
                "text-justify": "inter-word",
                "font-size": "18px",
                "padding-bottom": "1.5%"
            },
        ),
    ],
        className="row"
    ),

    html.Div([
        dcc.Markdown(
            ''' 
            
            You can view the source code for the [proposed network](https://github.com/darrenf0209/PFNL), written using 
            TensorFlow, or for this [dashboard] (https://github.com/darrenf0209/FYP-Dash), written using Dash. Thank you 
            for exploring this exciting research and feel free to reach out with any questions. 

            ''',
            className="ten columns offset-by-one",
            style={
                "text-align": "justify",
                "text-justify": "inter-word",
                "font-size": "18px",
                "padding-bottom": "1.5%"
            },
        ),
    ],
        className="row"
    ),

    html.Div([
        html.H4('Visual Results of 2x Video Super-Resolution')
    ],
    ),

    html.Div([
        dcc.Markdown(
            ''' 
            
            With this supervised causal deep learning network, a video sequence can be doubled in size. The input 
            video frame to the network is downsampled and Gaussian blurred, and the output is the high resolution 
            estimate. The model trains with more than 500 low-resolution and high-resolution short video sequence 
            pairs. A sample of testing video sequences are presented below to demonstrate its effectiveness. 

            ''',
            className="ten columns offset-by-one",
            style={
                "text-align": "justify",
                "text-justify": "inter-word",
                "font-size": "18px",
                "padding-bottom": "1.5%"
            },
        ),
    ],
        className="row"
    ),

    html.Div([
        html.H5(
            "Please select a video sequence"
                ),
        dcc.Dropdown(
            id='video-sequence-selector',
            options=[{'label': i, 'value': i} for i in videos_lr],
            value=videos_lr[0],
            clearable=False,
            className="four columns offset-by-four",
        ),
    ],
        className="row",
        style={
            "text-align": "center",
            "padding-bottom": "1.5%"
        }
    ),

    html.Div([
        html.Div([
            html.H5(
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
            html.H5(
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
            "text-align": "center",
            "padding-bottom": "1.5%"
        },
    ),

    html.Div([
        dcc.Markdown(
            '''

            The above video sequences are generated with the _Alternative_ proposed model from this research. It is a 
            causal network which utilises a previous high-resolution frame and the current low-resolution frame. A 
            visual representation of the network utilising this approach is shown below. For GPU limitations, 
            only upscaling video sequences by two is considered. 

            ''',
            className="ten columns offset-by-one",
            style={
                "text-align": "justify",
                "text-justify": "inter-word",
                "font-size": "18px",
                "padding-bottom": "1.5%"
            },
        ),
    ],
        className="row"
    ),

    html.Div([
        html.Div([
            html.H5(
                "Alternative Proposed Network (5 input frames)",
            ),
            html.Img(
                src="assets/alternative_proposed_network.PNG",
                style={
                    "width": "100%",
                    "height": "auto",
                    "padding-bottom": "1.5%"
                },
            ),
        ],
            className="eight columns offset-by-two",
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
        dcc.Markdown(
            '''
            
            Several models were trained and evaluated throughout this research project. The _Alternative_ and _Null_ 
            were the primary models for investigating the impact of extracting different degrees of spatial 
            information. While the _Alternative_ model utilised a high-resolution frame, the _Null_ model did not. 
            The _Alternative_ slightly outperformed from the experiments undertaken, but did require longer training 
            times. Both of these models are causal systems. As a benchmark for this research investigation, 
            the original network, modified for 2x video super-resolution, were tested with varying input frames. 
            These are the _Control_ models which can also be compared below, with either 3, 5 or 7 input frames. The 
            _Control_ models utilise frames from the future and hence are not causal systems, making them 
            inapplicable to real-time applications. They do, however, greatly outperform the causal systems 
            investigated by the _Null_ and _Alternative_. The data shown is the average of three identically trained 
            models. 
    
            ''',
            className="ten columns offset-by-one",
            style={
                "text-align": "justify",
                "text-justify": "inter-word",
                "font-size": "18px",
                "padding-bottom": "1.5%"
            },
        ),
    ],
        className="row"
    ),

    html.Div([
        html.H5(
            "Select Model(s)",
            className="five columns offset-by-one"
        ),
        html.H5(
            "Select Metric",
            className="five columns"
        )
    ],
        className="row"
    ),

    html.Div([
        html.Div(
            dcc.Dropdown(
                id='model-selector',
                options=[{'label': i, 'value': i} for i in models],
                value=['Alternative', 'Null'],
                multi=True,
                className="five columns offset-by-one",
            ),
        ),
        html.Div(
            dcc.Dropdown(
                id='metric-selector',
                options=[{'label': i, 'value': i} for i in metrics],
                value='PSNR',
                className="two columns offset-by-two",
            ),
        ),
    ],
        className="row",
        style={
            "text-align": "center"
        }

    ),

    html.Div(
        dcc.Graph(
            id='training-results-scatter',
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
    src_lr = os.path.join(video_dir_lr, value + '.gif')
    src_hr = os.path.join(video_dir_hr, value + '.gif')
    return src_lr, src_hr


@app.callback(
    Output('training-results-scatter', 'figure'),
    [Input('model-selector', 'value'),
     Input('metric-selector', 'value')])
def update_graph(model_choice, metric):
    fig = go.Figure()
    choices = list(model_choice)
    for i in range(0, len(choices)):
        model_selection = df_mean.loc[df_mean["Model"] == choices[i]]
        fig.add_trace(
            go.Scatter(
                x=model_selection["Iteration"],
                y=model_selection[metric],
                name="{}".format(choices[i])
            ))

    fig.update_layout(
        title={
            'text': "{} vs Iteration".format(metric),
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Iteration",
        yaxis_title="{}".format(metric),
        legend_title="Model Names",
        showlegend=True,
        font=dict(
            family="Century Schoolbook",
            size=16
        )
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
