import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import desc

app = dash.Dash(__name__)
server = app.server

# Read the data from CSV file
df = pd.read_csv("rf_data.csv")

# Define the layout of the app
app.layout = html.Div([
    html.Div([
        html.Pre(children="Radiative Forcing Infographic",
                 style={"text-align": "center", "font-size": "100%", "color": "black"})
    ]),
    html.Div([
        html.H1("Radiative Forcing")
    ]),
    html.Div([
        html.P("Radiative Forcing refers to the difference between the solar energy absorbed by Earth and the energy radiated back into space. A system in thermal balance has zero radiative forcing. Solar irradiance is the energy from the sun received per unit area per second (W/m²). A positive radiative forcing indicates more energy absorption than reflection, leading to warming, and vice versa. Here, we break down radiative forcing into its components, often called 'forcing agents', categorised by their sources.", className="intro"),
        html.P(["Some of these agents are ", html.Span("natural ", className="natural"), " while others are due to ", html.Span("human", className="human"), " activities."], className="agents"),
    ]),
    html.Div([
        html.Details([
            html.Summary('Useful Definitions'),
            html.P("Albedo: A measure of reflectivity. A perfectly black object (perfect absorber) has an albedo of 0, while a white object has an albedo of 1. For instance, replacing forests with agricultural land increases Earth's albedo as crops are more reflective than forests.", className="albedo"),
            html.P('Stratospheric Ozone: Ozone in the stratosphere absorbs energy and partially re-emits it back into space.', className="strozone"),
            html.P("Black Carbon on Snow: Carbon from fossil fuels gets trapped in ice, darkening it, reducing albedo, and causing the ice to absorb more sunlight.", className="blacksnow"),
            html.P("Aerosols: These particles contribute negatively to radiative forcing, but due to their short atmospheric lifetimes, they cannot offset the long-term effects of greenhouse gases.", className="aerosols"),
            html.P("Aerosol Cloud Albedo Effect: Aerosols decrease precipitation efficiency, inhibiting cloud formation, allowing more heat to radiate away at night that would otherwise be trapped by clouds."),
            html.P("Contrails: Formed by water vapour condensing around particles from aircraft engines. These ice clouds act like regular clouds, insulating the Earth and preventing heat from escaping."),
            html.P("Solar Irradiance: Natural variations in the sun’s energy as measured on Earth. This is the only truly non-anthropogenic source of radiative forcing.")
        ], className="definitions")
    ]),
    html.Div([
        dcc.Checklist(
            id='my_checklist',
            options=[{'label': x, 'value': x, 'disabled': False} for x in df['Source'].unique()],
            value=['Carbon Dioxide', 'Methane', 'Albedo (Land use)', 'Solar irradiance', 'Net total'],
            className='my_box_container',
            style={'display': 'flex'},
            inputClassName='my_box_input',
            inputStyle={'cursor': 'pointer'},
            labelClassName='my_box_label',
        ),
    ]),
    html.Div([
        dcc.Graph(id='the_graph')
    ]),
])

@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='my_checklist', component_property='value')]
)
def update_graph(selected_sources):
    filtered_df = df[df['Source'].isin(selected_sources)]

    fig = go.Figure(go.Waterfall(
        name="20", orientation="v",
        measure=filtered_df['Measure'],
        x=filtered_df['Source'],
        textposition="inside",
        text=filtered_df['Contribution'],
        y=filtered_df['Contribution'],
        increasing={"marker": {"color": "#8F2738"}},
        decreasing={"marker": {"color": "#5E8DB0"}},
        totals={"marker": {"color": "#ffb01f", "line": {"color": "gold", "width": 3}}},
        connector={"line": {"color": "#C0C0C0"}},
    ))
    fig.update_yaxes(visible=True, title_text='W/m<sup>2</sup>')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8124)