# Import necessary libraries
import dash
from dash import dcc
from dash import html
from dash import Input, Output
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd

app = dash.Dash(__name__)

data = pd.read_csv("data.csv")

colors = {
    # 'background': '#000000',
    # 'background': '#B3C8CF',
    'background': '#FFEFEF',
    'text1': '#392467',
    'text': '#5D3587',
    'line' : "#BB9CC0",
    'graph' : "#67729D"
}

font_size = "20px"

pio.templates.default = "plotly_white"

app.layout = html.Div([
    html.Br(),
    html.H1("Smart Neonatal Incubator", style={
                'textAlign': 'center',
                'color': colors['text1']
            }),
    html.Hr(style={'borderWidth': "2.5px", "borderColor": "#BB9CC0", 'opacity':'unset'}),
    
    html.Div([
        html.Div([
        html.Div([
             html.Div("Doctor:", style={'font-size': font_size, 'color': colors['text']}),
              html.Div("(Give name)", style={'font-size': font_size, 'color': colors['text']}),
        ], style={"display":"flex", 'justify-content':'space-between'}),
        html.Br(),
        
        html.H2("Patient Details", style={'textAlign':"center", 'color': colors['text1'],}),
        html.Hr(style={'borderWidth': "0.5px", "borderColor": "#BB9CC0"}),

        html.Br(),
        html.Div([
             html.Div("Name:", style={'font-size': font_size, 'color': colors['text']}),
              html.Div("(Give name)", style={'font-size': font_size, 'color': colors['text']}),
        ], style={"display":"flex", 'justify-content':'space-between'}),

        html.Div([
             html.Div("Age:", style={'font-size': font_size, 'color': colors['text']}),
              html.Div("10 days", style={'font-size': font_size, 'color': colors['text']}),
        ], style={"display":"flex", 'justify-content':'space-between'}),

        html.Div([
             html.Div("Gender:", style={'font-size': font_size, 'color': colors['text']}),
              html.Div("Female", style={'font-size': font_size, 'color': colors['text']}),
        ], style={"display":"flex", 'justify-content':'space-between'}),

        html.Div([
             html.Div("Reasons for admission:", style={'font-size': font_size, 'color': colors['text']}),
              html.Div("Premature", style={'font-size': font_size, 'color': colors['text']}),
        ], style={"display":"flex", 'justify-content':'space-between'}),
        html.Br(),

        html.Div([
            html.Div("Balance:", style={'font-size': font_size, 'color': colors['text']}),
            html.Div(id="balance", style={'font-size': font_size, 'color': colors['text']}),
        ], style={"display":"flex", 'justify-content':'space-between'}),

        html.Div([
             html.Div("Sound recognized:", style={'font-size': font_size, 'color': colors['text']}),
              html.Div(id="sound", style={'font-size': font_size, 'color': colors['text']}),
        ], style={"display":"flex", 'justify-content':'space-between'}),

    ], style={
        'width':'25vw',
        'backgroundColor': colors['background'],
        'padding':'50px 20px',
        'border-right':'3px solid #BB9CC0',
        # 'border-top':'2px dotted black',
        }),

    html.Div([
        html.H2("Vital Parameters", style={
                'textAlign': 'center',
                'color': colors['text1'],
                'padding': '20px 0px'
            }),
        
        dcc.Graph(id='pulse-plot'),
        html.Br(),
        dcc.Graph(id='temp-plot'),
        html.Br(),
        dcc.Graph(id='humidity-plot'),
        dcc.Interval(id='interval-component', disabled=False, interval=1*1000, n_intervals=0)
    ], style={
        'width':'75vw',
        'backgroundColor': colors['background'],
        'padding':'20px 20px',
        'display' : 'flex',
        'align-items':'center',
        'flex-direction' :'column'
        })
    ], style={
        'display':'flex',
        # 'justify-content':'space-between'
        })
    ], style={
        'backgroundColor': colors['background'],
        'margin':'0px',
        'padding':'0px',
        'font-family':'Georgiya, serif', 
        # 'font-family':'Alegreya, serif', 
        })

@app.callback(
    [Output('temp-plot', 'figure'),
     Output('humidity-plot', 'figure'),
     Output('pulse-plot', 'figure'),
     Output('balance', 'children'),
     Output('sound', 'children'),
     ],
    [Input('interval-component', "n_intervals")]
)

def update_graph(interval):
    if interval==0:
        raise PreventUpdate
    df = pd.read_csv("data.csv")

    temp_fig = go.Figure()
    temp_fig.add_trace(go.Scatter(
        x=df['time'][-20:],
        y=df['temperature'][-20:],
        line=dict(color=colors['line'],),
        ))
    temp_fig.update_layout(
        title_text="Temperature",
        font=dict(
            size=15,
            color=colors['graph']
        ),
        height=300,
        width=800,
        margin=dict(l=30, r=20, t=50, b=0),
    )

    humidity_fig = go.Figure(data=go.Scatter(
        x=df['time'][-20:],
        y=df['humidity'][-20:],
        line=dict(color=colors['line'],),
        ))
    humidity_fig.update_layout(
        title_text="Humidity",
        font=dict(
            size=15,
            color=colors['graph'],
        ),
        height=300,
        width=800,
        margin=dict(l=30, r=20, t=50, b=0),
    )

    pulse_fig = go.Figure(data=go.Scatter(
        x=df['time'][-20:],
        y=df['pulse_rate'][-20:],
        line=dict(color=colors['line'],),
        ))
    pulse_fig.update_layout(
        title_text="Pulse Rate",
        font=dict(
            size=15,
            color=colors['graph']
        ),
        height=300,
        width=800,
        margin=dict(l=30, r=20, t=50, b=0),
    )

    balance = str((df['balance'].tolist())[-1])
    sound = str((df['sound'].tolist())[-1])
    return temp_fig, humidity_fig, pulse_fig, balance, sound

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)