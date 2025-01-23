"""
Dashboard para análise de demandas usando dados do Google Sheets.
Lê a planilha 'DEMANDAS JULIO' e exibe análises e filtros.
"""

import pandas as pd
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from config import (
    SPREADSHEET_ID,
    SHEET_NAME,
    RANGE_NAME,
    CREDENTIALS_FILE,
    SCOPES
)

def load_credentials():
    """Carrega as credenciais do Google Sheets"""
    try:
        if not os.path.exists(CREDENTIALS_FILE):
            st.error(f"Arquivo de credenciais não encontrado: {CREDENTIALS_FILE}")
            st.info("Por favor, configure o arquivo service_account.json na pasta docs/")
            return None

        credentials = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE,
            scopes=SCOPES
        )
        return credentials
    except Exception as e:
        st.error(f"Erro ao carregar credenciais: {str(e)}")
        st.info("Verifique se o arquivo service_account.json está correto.")
        return None

def debug_sheet_structure(values):
    """Função para debug da estrutura da planilha"""
    st.subheader("🔍 Debug: Estrutura da Planilha")
    
    if not values:
        st.error("Nenhum dado encontrado na planilha")
        return
    
    # Mostra as primeiras linhas brutas
    st.write("Primeiras 5 linhas (dados brutos):")
    for i, row in enumerate(values[:5]):
        st.write(f"Linha {i}: {row}")
    
    # Mostra informações sobre as colunas
    if values[0]:  # Se tem cabeçalho
        st.write("Colunas encontradas:")
        for i, col in enumerate(values[0]):
            st.write(f"Coluna {i}: '{col}'")
    
    # Análise de valores únicos em cada coluna
    if len(values) > 1:  # Se tem dados além do cabeçalho
        df = pd.DataFrame(values[1:], columns=values[0])
        st.write("Análise de valores únicos por coluna:")
        for col in df.columns:
            unique_values = df[col].unique()
            st.write(f"'{col}': {len(unique_values)} valores únicos")
            if len(unique_values) < 10:  # Mostra valores únicos se forem poucos
                st.write(f"Valores: {sorted(unique_values)}")

def get_sheet_data():
    """Lê os dados da planilha do Google Sheets"""
    try:
        credentials = load_credentials()
        if not credentials:
            return None

        # Constrói o serviço do Google Sheets
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()

        # Tenta ler os dados da planilha
        try:
            result = sheet.values().get(
                spreadsheetId=SPREADSHEET_ID,
                range=RANGE_NAME
            ).execute()
        except HttpError as e:
            if e.resp.status == 404:
                st.error(f"Planilha não encontrada. Verifique o ID: {SPREADSHEET_ID}")
            elif e.resp.status == 403:
                st.error("Sem permissão para acessar a planilha. Verifique as permissões.")
            else:
                st.error(f"Erro ao acessar planilha: {str(e)}")
            return None

        # Processa os dados
        values = result.get('values', [])
        if not values:
            st.warning('Nenhum dado encontrado na planilha.')
            return None

        # Debug da estrutura da planilha
        debug_sheet_structure(values)
            
        # Converte para DataFrame
        df = pd.DataFrame(values[1:], columns=values[0])
        
        # Mapeamento de colunas antigas para novas
        colunas_mapeadas = {
            'Banco': 'BANCO',
            'Responsável': 'RESPONSÁVEL',
            'Status': 'SITUAÇÃO',
            'Resolução': 'RESOLUÇÃO',
            'CTT': 'CTT',
            'Escritório': 'ESCRITÓRIO',
            'Ativo/Receptivo': 'ATIVO/RECEPTIVO',
            'Diretor': 'DIRETOR'
        }
        
        # Renomeia as colunas se existirem
        df = df.rename(columns=colunas_mapeadas)
        
        # Verifica colunas necessárias após o mapeamento
        required_columns = ['RESOLUÇÃO', 'CTT', 'ESCRITÓRIO', 'ATIVO/RECEPTIVO',
                          'DIRETOR', 'BANCO', 'RESPONSÁVEL', 'SITUAÇÃO']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"Colunas ausentes na planilha: {', '.join(missing_columns)}")
            st.write("Colunas disponíveis:", df.columns.tolist())
            return None

        return df

    except Exception as e:
        st.error(f"Erro inesperado: {str(e)}")
        return None

def main():
    st.set_page_config(
        page_title="Dashboard de Demandas",
        page_icon="📊",
        layout="wide"
    )

    st.title("📊 Dashboard de Análise de Demandas")
    
    # Carrega os dados
    with st.spinner("Carregando dados da planilha..."):
        df = get_sheet_data()
    
    if df is None:
        st.stop()
    
    # Exibe os dados brutos para debug
    st.subheader("🔍 Debug: Dados Carregados")
    st.write("Formato do DataFrame:", df.shape)
    st.write("Colunas:", df.columns.tolist())
    st.write("Primeiras linhas:")
    st.dataframe(df.head())
    
    # Continua com o resto do código apenas se tivermos todas as colunas necessárias
    colunas_desejadas = ['RESOLUÇÃO', 'CTT', 'ESCRITÓRIO', 'ATIVO/RECEPTIVO',
                         'DIRETOR', 'BANCO', 'RESPONSÁVEL', 'SITUAÇÃO']
    
    if not all(col in df.columns for col in colunas_desejadas):
        st.error("Algumas colunas necessárias estão faltando. Verifique o mapeamento de colunas.")
        st.stop()
    
    # Filtra as colunas
    df_selecionado = df[colunas_desejadas]
    
    # Sidebar
    st.sidebar.title("🔍 Filtros")
    
    # Filtro do Banco
    bancos_disponiveis = sorted(df['BANCO'].unique())
    banco_selecionado = st.sidebar.selectbox(
        "Escolha um Banco",
        bancos_disponiveis,
        help="Selecione o banco para filtrar as demandas"
    )
    
    # Filtro do Responsável
    responsaveis_disponiveis = sorted(df['RESPONSÁVEL'].unique())
    responsavel_selecionado = st.sidebar.selectbox(
        "Escolha um Responsável",
        responsaveis_disponiveis,
        help="Selecione o responsável para filtrar as demandas"
    )
    
    # Aplica os filtros
    df_filtrado = df_selecionado[
        (df_selecionado['BANCO'] == banco_selecionado) & 
        (df_selecionado['RESPONSÁVEL'] == responsavel_selecionado)
    ]
    
    # Métricas principais
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Demandas", len(df_filtrado))
    with col2:
        st.metric("Banco", banco_selecionado)
    with col3:
        st.metric("Responsável", responsavel_selecionado)
    
    # Exibe o DataFrame filtrado
    st.subheader("📋 Demandas Filtradas")
    st.dataframe(
        df_filtrado,
        use_container_width=True,
        hide_index=True
    )
    
    # Análise de situações
    st.subheader("📈 Análise de Situações")
    situacoes_desejadas = ['RESOLVIDO', 'RECEPTIVO', 'ANÁLISE',
                          'PRIORIDADE TOTAL', 'PENDENTE']
    
    # Contagem de situações
    contagem_situacoes = {
        situacao: (df_filtrado['SITUAÇÃO'] == situacao).sum()
        for situacao in situacoes_desejadas
    }
    
    # Exibe as contagens com barras de progresso
    for situacao, contagem in contagem_situacoes.items():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.metric(
                situacao,
                contagem,
                help=f"Quantidade de demandas com status {situacao}"
            )
        with col2:
            if len(df_filtrado) > 0:
                progress = contagem / len(df_filtrado)
                st.progress(progress)
                st.caption(f"{progress:.1%}")

if __name__ == "__main__":
    main()
