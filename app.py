import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Inicializa o app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout do sidebar
sidebar = html.Div(
    [
        html.H2("Filtros", className="display-6"),
        html.Hr(),
        html.P("Selecione o período:"),
        dcc.DatePickerRange(
            id='date-picker',
            start_date_placeholder_text="Data Inicial",
            end_date_placeholder_text="Data Final",
            className="mb-3"
        ),
        html.P("Selecione o grupo:"),
        dcc.Dropdown(
            id='group-dropdown',
            options=[
                {'label': 'Grupo A', 'value': 'A'},
                {'label': 'Grupo B', 'value': 'B'},
                {'label': 'Grupo C', 'value': 'C'}
            ],
            className="mb-3"
        ),
        html.P("Status:"),
        dcc.Checklist(
            id='status-checklist',
            options=[
                {'label': ' Pendente', 'value': 'pending'},
                {'label': ' Em Progresso', 'value': 'progress'},
                {'label': ' Concluído', 'value': 'done'}
            ],
            value=['pending', 'progress', 'done']
        )
    ],
    style={
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'bottom': 0,
        'width': '250px',
        'padding': '20px',
        'background-color': '#f8f9fa'
    }
)

# Layout principal
content = html.Div(
    [
        html.H1("Dashboard de Demandas", className="text-center mb-4"),
        
        # KPI Cards
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Total Demandas", className="card-title"),
                    html.H2("150", className="card-text text-primary")
                ])
            ]), width=3),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Em Progresso", className="card-title"),
                    html.H2("45", className="card-text text-warning")
                ])
            ]), width=3),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Concluídas", className="card-title"),
                    html.H2("89", className="card-text text-success")
                ])
            ]), width=3),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Pendentes", className="card-title"),
                    html.H2("16", className="card-text text-danger")
                ])
            ]), width=3),
        ], className="mb-4"),

        # Gráficos
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Distribuição por Status"),
                        dcc.Graph(id='status-graph')
                    ])
                ])
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Demandas por Grupo"),
                        dcc.Graph(id='group-graph')
                    ])
                ])
            ], width=6),
        ])
    ],
    style={
        'margin-left': '250px',
        'padding': '20px'
    }
)

# Layout completo
app.layout = html.Div([sidebar, content])

# Callback para o gráfico de status
@app.callback(
    Output('status-graph', 'figure'),
    [Input('status-checklist', 'value')]
)
def update_status_graph(status):
    data = pd.DataFrame({
        'Status': ['Pendente', 'Em Progresso', 'Concluído'],
        'Quantidade': [16, 45, 89]
    })
    fig = px.pie(data, values='Quantidade', names='Status', hole=0.3)
    return fig

# Callback para o gráfico de grupos
@app.callback(
    Output('group-graph', 'figure'),
    [Input('group-dropdown', 'value')]
)
def update_group_graph(group):
    data = pd.DataFrame({
        'Grupo': ['A', 'B', 'C'],
        'Quantidade': [50, 45, 55]
    })
    fig = px.bar(data, x='Grupo', y='Quantidade')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
