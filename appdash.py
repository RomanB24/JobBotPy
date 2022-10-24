from dash import Dash, dcc, html, Input, Output
from dash.dependencies import Input, Output
from dash import dcc
from dash import dash_table
import dash_bootstrap_components as dbc
import pandas as pd

app = Dash(__name__)

@app.callback(
    Output('table_admin_ad', 'children'),
    Input('table_1', 'value'))
def get_error_admin(vacant):
    tab_candidates = pd.read_csv("Kandidats.csv", delimiter=",", encoding='cp1251')
    dff = pd.DataFrame(tab_candidates).sort_values('Вакансия')
    df = dff[dff["Вакансия"] == vacant]
    if df.empty == True:
        df = dff

    if len(df) == 0:
        list = {'Вакансия': ['Нет данных']}
        df = pd.DataFrame(list)
    table2 = dash_table.DataTable(data=df.to_dict('records'),
                                  columns=[{'id': x, 'name': x, 'presentation': 'markdown'} for x in df.columns],
                                  fixed_rows={'headers': True},
                                  style_cell={"textAlign": "center"},
                                  style_header={
                                      'backgroundColor': 'rgb(210, 210, 210)',
                                      'border': '1px solid Gray',
                                      'textAlign': 'center',
                                  },
                                  style_cell_conditional=[
                                      {'if': {'column_id': 'Ссылка'},
                                       'width': '60px',
                                       }
                                  ],
                                  style_data_conditional=[
                                      {
                                          'if': {'row_index': 'odd'},
                                          'backgroundColor': 'rgb(220, 220, 220)',
                                      }
                                  ],
                                  style_table={'width': '100%', 'height': '300px', 'lineHeight': '15px'}
                                  ),
    return table2

def get_vacant():
    vacants = []
    prioritet = pd.read_csv("Kandidats.csv", delimiter=",", encoding='cp1251')
    dff = pd.DataFrame(prioritet).sort_values('Вакансия')
    for i in dff['Вакансия'].unique():
        vacants.append(i)
    return vacants

app.layout = html.Div([
        html.Div(
            [
                dbc.Row([
                    dbc.Col([
                        html.H3('Кандидаты на вакансии', style={"textAlign": "center"},
                                className='text-secondary'),
                        html.Br(),

                        dbc.Col([
                            dcc.Dropdown(
                                id='table_1',
                                options=[{'label': i, 'value': i} for i in get_vacant()],
                                value=get_vacant()[0],
                                style={"textAlign": "center"},
                            ),
                        ], className="col-md"),
                        html.Br(),
                        html.Div(id='table_admin_ad',
                                 style={"textAlign": "center", 'font-size': '12px', 'width': '100%'}),
                    ], className="col-6 my-2"),
                ]),
                html.Br(),
            ], className="pad-row", )
    ], className='container-fluid')





if __name__ == '__main__':
    app.run_server(debug=True)
