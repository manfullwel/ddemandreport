import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import os
from functools import lru_cache
import warnings
import logging
import sys

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

warnings.filterwarnings('ignore')

# Configurações globais
EXCEL_PATH = "F:/demandstest/docs/_DEMANDAS DE JANEIRO_2025.xlsx"
logger.info(f"Arquivo Excel configurado: {EXCEL_PATH}")

STATUS_COLORS = {
    'RESOLVIDO': '#2ecc71',
    'PENDENTE ATIVO': '#e74c3c',
    'PENDENTE RECEPTIVO': '#f1c40f',
    'PRIORIDADE': '#9b59b6',
    'PRIORIDADE TOTAL': '#8e44ad',
    'ANÁLISE': '#3498db',
    'ANÁLISE DO DIA': '#2980b9',
    'RECEPTIVO': '#1abc9c',
    'QUITADO CLIENTE': '#27ae60',
    'QUITADO': '#16a085',
    'APROVADO': '#2ecc71'
}

class DataManager:
    _instance = None
    _data = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            logger.debug("Criando nova instância do DataManager")
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        logger.debug("Inicializando DataManager")
        if self._data is None:
            self.load_data()
    
    def load_data(self):
        """Carrega e processa os dados do Excel com tratamento de erros e validações"""
        try:
            logger.info(f"Iniciando carregamento dos dados de: {EXCEL_PATH}")
            
            # Verificar se o arquivo existe
            if not os.path.exists(EXCEL_PATH):
                logger.error(f"Arquivo não encontrado: {EXCEL_PATH}")
                raise FileNotFoundError(f"Arquivo não encontrado: {EXCEL_PATH}")
            
            logger.debug("Carregando planilha DEMANDA LEANDROADRIANO...")
            df_leandro = pd.read_excel(EXCEL_PATH, sheet_name='DEMANDA LEANDROADRIANO')
            logger.info(f"Planilha LEANDRO carregada: {len(df_leandro)} registros")
            df_leandro['GRUPO'] = 'DEMANDA LEANDROADRIANO'
            
            logger.debug("Carregando planilha DEMANDAS JULIO...")
            df_julio = pd.read_excel(EXCEL_PATH, sheet_name='DEMANDAS JULIO')
            logger.info(f"Planilha JULIO carregada: {len(df_julio)} registros")
            df_julio['GRUPO'] = 'DEMANDAS JULIO'
            
            # Padronizar colunas
            logger.debug("Padronizando colunas...")
            df_julio = df_julio.rename(columns={
                ' DATA': 'DATA',
                'RESOLUÇÃO': 'RESOLUÇÃO',
                'RESPONSÁVEL': 'RESPONSÁVEL',
                'SITUAÇÃO': 'SITUAÇÃO'
            })
            
            # Combinar os dataframes
            logger.debug("Combinando dataframes...")
            df = pd.concat([df_leandro, df_julio], ignore_index=True)
            logger.info(f"Total de registros após combinação: {len(df)}")
            
            # Limpeza e transformação dos dados
            logger.debug("Realizando limpeza e transformação dos dados...")
            df['DATA'] = pd.to_datetime(df['DATA'], errors='coerce')
            df['RESOLUÇÃO'] = pd.to_datetime(df['RESOLUÇÃO'], errors='coerce')
            df['SITUAÇÃO'] = df['SITUAÇÃO'].fillna('NÃO ESPECIFICADO')
            df['RESPONSÁVEL'] = df['RESPONSÁVEL'].fillna('NÃO ATRIBUÍDO')
            
            # Validar dados
            if df['DATA'].isna().any():
                logger.warning("Existem datas inválidas nos dados")
                logger.debug(f"Linhas com datas inválidas: {df[df['DATA'].isna()].index.tolist()}")
            
            # Criar colunas calculadas
            df['SEMANA'] = df['DATA'].dt.isocalendar().week
            df['DIA_SEMANA'] = df['DATA'].dt.day_name()
            
            logger.info(f"Processamento concluído:")
            logger.info(f"- Total de registros: {len(df)}")
            logger.info(f"- Período: {df['DATA'].min().strftime('%d/%m/%Y')} a {df['DATA'].max().strftime('%d/%m/%Y')}")
            logger.info(f"- Grupos: {df['GRUPO'].unique().tolist()}")
            logger.info(f"- Status: {df['SITUAÇÃO'].unique().tolist()}")
            
            self._data = df
            return df
            
        except Exception as e:
            logger.error(f"ERRO ao carregar dados: {str(e)}")
            import traceback
            logger.error(f"Traceback:\n{traceback.format_exc()}")
            return pd.DataFrame()

    @property
    def data(self):
        """Retorna o DataFrame com os dados"""
        if self._data is None or self._data.empty:
            self.load_data()
        return self._data
    
    def get_filtered_data(self, start_date=None, end_date=None, grupo=None, responsavel=None):
        """Retorna dados filtrados com base nos parâmetros"""
        df = self.data.copy()
        
        if start_date:
            df = df[df['DATA'] >= start_date]
        if end_date:
            df = df[df['DATA'] <= end_date]
        if grupo:
            if isinstance(grupo, list):
                df = df[df['GRUPO'].isin(grupo)]
            else:
                df = df[df['GRUPO'] == grupo]
        if responsavel:
            if isinstance(responsavel, list):
                df = df[df['RESPONSÁVEL'].isin(responsavel)]
            else:
                df = df[df['RESPONSÁVEL'] == responsavel]
        
        return df
    
    @lru_cache(maxsize=32)
    def get_summary_stats(self, start_date, end_date, grupo=None):
        """Retorna estatísticas resumidas dos dados"""
        df = self.get_filtered_data(start_date, end_date, grupo)
        
        stats = {
            'total': len(df),
            'resolvidos': len(df[df['SITUAÇÃO'] == 'RESOLVIDO']),
            'pendentes': len(df[df['SITUAÇÃO'].isin(['PENDENTE ATIVO', 'PENDENTE RECEPTIVO'])]),
            'prioridades': len(df[df['SITUAÇÃO'].isin(['PRIORIDADE', 'PRIORIDADE TOTAL'])]),
            'media_diaria': len(df) / max((df['DATA'].max() - df['DATA'].min()).days, 1)
        }
        
        return stats

# Inicializar o gerenciador de dados
data_manager = DataManager.get_instance()

# Inicializar o app Dash com tema moderno
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title='Dashboard de Análise de Demandas',
    update_title='Atualizando...'
)

# Layout do dashboard
app.layout = html.Div([
    # Sidebar
    html.Div([
        html.H4("Filtros", className="mb-3"),
        
        html.Label("Período de Análise"),
        dcc.DatePickerRange(
            id='date-range',
            start_date=datetime(2025, 1, 1),
            end_date=datetime(2025, 1, 31),
            display_format='DD/MM/YYYY',
            className="mb-3"
        ),
        
        html.Label("Grupos"),
        dcc.Dropdown(
            id='group-filter',
            placeholder='Todos os Grupos',
            multi=True,
            className="mb-3"
        ),
        
        html.Label("Responsáveis"),
        dcc.Dropdown(
            id='responsible-filter',
            placeholder='Todos os Responsáveis',
            multi=True,
            className="mb-3"
        ),
        
        html.Hr(),
        
        html.Div(id='summary-stats', className="mt-3")
    ], style={
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'bottom': 0,
        'width': '250px',
        'padding': '20px',
        'background-color': '#f8f9fa',
        'borderRight': '1px solid #dee2e6'
    }),
    
    # Conteúdo Principal
    html.Div([
        html.H2("Dashboard de Análise de Demandas", className="mb-4"),
        
        # KPIs em Cards
        html.Div(id='kpi-cards', className="row mb-4"),
        
        # Tabs para Grupos
        dcc.Tabs([
            dcc.Tab(label="DEMANDA LEANDROADRIANO", children=[
                html.Div(id='leandro-content', className="mt-3")
            ]),
            dcc.Tab(label="DEMANDAS JULIO", children=[
                html.Div(id='julio-content', className="mt-3")
            ])
        ], className="mb-4"),
        
        # Gráfico de Status
        dcc.Graph(id='status-distribution')
        
    ], style={
        'marginLeft': '250px',
        'padding': '20px'
    })
], style={'fontFamily': 'Arial'})

# Callbacks
@app.callback(
    [Output('kpi-cards', 'children'),
     Output('leandro-content', 'children'),
     Output('julio-content', 'children'),
     Output('status-distribution', 'figure'),
     Output('summary-stats', 'children')],
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('group-filter', 'value'),
     Input('responsible-filter', 'value')]
)
def update_dashboard(start_date, end_date, selected_groups, selected_responsibles):
    # Carregar dados filtrados
    df = data_manager.get_filtered_data(
        start_date=start_date,
        end_date=end_date,
        grupo=selected_groups,
        responsavel=selected_responsibles
    )
    
    # 1. KPI Cards
    total_demandas = len(df)
    total_resolvidos = len(df[df['SITUAÇÃO'] == 'RESOLVIDO'])
    total_pendentes = len(df[df['SITUAÇÃO'].isin(['PENDENTE ATIVO', 'PENDENTE RECEPTIVO'])])
    total_prioridades = len(df[df['SITUAÇÃO'].isin(['PRIORIDADE', 'PRIORIDADE TOTAL'])])
    
    kpi_cards = [
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(f"{total_demandas:,}", className="text-center"),
                    html.P("Total", className="text-center text-muted mb-0")
                ])
            ])
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(f"{total_resolvidos:,}", className="text-center text-success"),
                    html.P("Resolvidos", className="text-center text-muted mb-0")
                ])
            ])
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(f"{total_pendentes:,}", className="text-center text-warning"),
                    html.P("Pendentes", className="text-center text-muted mb-0")
                ])
            ])
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(f"{total_prioridades:,}", className="text-center text-danger"),
                    html.P("Prioridades", className="text-center text-muted mb-0")
                ])
            ])
        ], width=3)
    ]
    
    # 2. Conteúdo por Grupo
    def create_group_content(grupo_df):
        if grupo_df.empty:
            return html.P("Nenhum dado disponível para o período selecionado")
        
        # Tabela de responsáveis
        resp_stats = []
        for resp in grupo_df['RESPONSÁVEL'].unique():
            resp_df = grupo_df[grupo_df['RESPONSÁVEL'] == resp]
            stats = {
                'Responsável': resp,
                'Total': len(resp_df),
                'Resolvidos': len(resp_df[resp_df['SITUAÇÃO'] == 'RESOLVIDO']),
                'Pendentes': len(resp_df[resp_df['SITUAÇÃO'].isin(['PENDENTE ATIVO', 'PENDENTE RECEPTIVO'])]),
                'Prioridades': len(resp_df[resp_df['SITUAÇÃO'].isin(['PRIORIDADE', 'PRIORIDADE TOTAL'])])
            }
            resp_stats.append(stats)
        
        df_stats = pd.DataFrame(resp_stats)
        
        return dbc.Table.from_dataframe(
            df_stats,
            striped=True,
            bordered=True,
            hover=True,
            responsive=True,
            className="mt-3"
        )
    
    leandro_content = create_group_content(df[df['GRUPO'] == 'DEMANDA LEANDROADRIANO'])
    julio_content = create_group_content(df[df['GRUPO'] == 'DEMANDAS JULIO'])
    
    # 3. Distribuição por Status
    status_dist = df.groupby('SITUAÇÃO').size().reset_index(name='count')
    status_dist = status_dist.sort_values('count', ascending=True)
    
    dist_fig = go.Figure(go.Bar(
        x=status_dist['count'],
        y=status_dist['SITUAÇÃO'],
        orientation='h',
        marker_color=[STATUS_COLORS.get(status, '#95a5a6') for status in status_dist['SITUAÇÃO']]
    ))
    
    dist_fig.update_layout(
        title='Distribuição por Status',
        xaxis_title="Quantidade",
        yaxis_title="Status",
        template='plotly_white',
        height=400,
        margin=dict(l=200)
    )
    
    # 4. Estatísticas Resumidas para Sidebar
    summary_stats = html.Div([
        html.H5("Resumo", className="mb-3"),
        html.P([
            html.Strong("Período: "), 
            f"{pd.to_datetime(start_date).strftime('%d/%m/%Y')} a {pd.to_datetime(end_date).strftime('%d/%m/%Y')}"
        ]),
        html.P([html.Strong("Total de Demandas: "), f"{total_demandas:,}"]),
        html.P([html.Strong("Taxa de Resolução: "), 
               f"{(total_resolvidos/total_demandas*100):.1f}%" if total_demandas > 0 else "0%"]),
        html.P([html.Strong("Pendências: "), f"{total_pendentes:,}"]),
        html.P([html.Strong("Prioridades: "), f"{total_prioridades:,}"])
    ])
    
    return kpi_cards, leandro_content, julio_content, dist_fig, summary_stats

# Callback para atualizar os filtros
@app.callback(
    [Output('group-filter', 'options'),
     Output('responsible-filter', 'options')],
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_filters(start_date, end_date):
    df = data_manager.get_filtered_data(start_date=start_date, end_date=end_date)
    
    group_options = [{'label': x, 'value': x} for x in sorted(df['GRUPO'].unique())]
    responsible_options = [{'label': x, 'value': x} for x in sorted(df['RESPONSÁVEL'].unique())]
    
    return group_options, responsible_options

if __name__ == '__main__':
    logger.info("=== Iniciando Dashboard de Análise de Demandas ===")
    
    try:
        logger.info("\nVerificando dados iniciais...")
        data_manager = DataManager.get_instance()
        initial_data = data_manager.data
        
        if initial_data.empty:
            logger.error("ERRO: Não foi possível carregar os dados iniciais!")
            sys.exit(1)
        
        logger.info("\nDados carregados com sucesso!")
        logger.info(f"Total de registros: {len(initial_data):,}")
        logger.info(f"Período dos dados: {initial_data['DATA'].min().strftime('%d/%m/%Y')} a {initial_data['DATA'].max().strftime('%d/%m/%Y')}")
        
        logger.info("\nIniciando servidor Dash...")
        app.run_server(debug=True, port=8050)
        
    except Exception as e:
        logger.error(f"ERRO FATAL: {str(e)}")
        import traceback
        logger.error(f"Traceback:\n{traceback.format_exc()}")
        sys.exit(1)
