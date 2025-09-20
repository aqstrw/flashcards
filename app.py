import numpy as np
import gspread
from google.auth import default
import pandas as pd
from dash import Dash, dcc, html, Input, Output, callback, ctx
import plotly.express as px
import dash_bootstrap_components as dbc

creds, _ = default()
gc = gspread.authorize(creds)
sh = gc.open("Dutch wordlist")
sheetdata = sh.sheet1.get_all_values()
sheetdata[0]
df = pd.DataFrame(data = sheetdata[1:],columns = sheetdata[0]).sample(frac = 1,ignore_index = True)

app = Dash(external_stylesheets=[dbc.themes.MINTY])
def serve_layout():
    return dbc.Container(
        [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Button(
                                    ["Prompt"],
                                    id = 'prompt_button',
                                    className = 'mb-3',
                                    color = 'primary',
                                    n_clicks = 0
                                ),
                                dbc.Spinner(
                                    [  
                                        dbc.Collapse(
                                            [
                                                dbc.Card(
                                                    [
                                                        dbc.CardBody(
                                                            ["Meaning"],
                                                            id = 'meaning'
                                                        ),
                                                    ],
                                                    style = {'width':'100%'},
                                                    className = 'd-flex',
                                                ),
                                            ],
                                            id = 'collapse',
                                            is_open = False,
                                            style = {'width':'100%'},
                                            # className='border border-primary',
                                        ),
                                    ],
                                    # className = 'd-flex',
                                    delay_hide = 300,
                                    # style = {'width':'100%'},
                                ),
                            ],
                            style = {'width':'100%'},
                        ),
                    ],
                    style = {'width':'100%'},
                    className="d-flex p-2 justify-content-start align-items-start",
                ),
            ],
            style = {'width':'100%'},
            className="d-flex flex-column flex-md-row m-2 border border-warning justify-content-start align-items-center",
        ),
        dbc.Row(
            [
                dbc.Col([
                        dbc.Button("Next",color = "primary",id = 'next'),
                        dbc.Button("Mark and Next",color = "secondary", id = "mark"),
                    ],
                    className="d-flex gap-2 border border-secondary justify-content-center align-items-center",
                ),
            ],
            style = {'width':'100%'},
            className="d-flex justify-content-center align-items-center",
        ),
    ],
    style = {'width':'60vw'},
    className = 'd-flex border border-info flex-wrap justify-content-center align-items-center',
    # className = 'border border-info', 
)
app.layout = serve_layout()

@callback(
    #outputs
    Output('collapse','is_open'),
    Output('prompt_button','children'),
    Output('meaning','children'),
    # Output('accord','start_collapsed'),
    #inputs
    Input('prompt_button','n_clicks'),
    Input('next','n_clicks'),
    # prevent_initial_call = True,
    running=[(Output("collapse", 'is_open'), False, False)]
)
def update_card(prompt_click,next_clicks):
    collapse_open = 0
    if ctx.triggered_id == 'prompt_button':
        collapse_open = 1
    if next_clicks is None:
        next_clicks = 0
    return (collapse_open,df.loc[next_clicks,'Nederlands'],df.loc[next_clicks,'English'])


if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port = 8050)