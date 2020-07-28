import dash
import dash_core_components as dcc
import dash_html_components as html

# Initialising the app
app = dash.Dash()

# Container of div and html elements
app.layout = html.Div(
    html.H1(children='Supervised Causal Video Super-Resolution')

)

if __name__ == "__main__":
    app.run_server(debug=True)
