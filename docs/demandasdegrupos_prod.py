"""
Dashboard para análise de demandas usando dados do Google Sheets.
Versão de produção.
"""

import pandas as pd
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from config import (
    SPREADSHEET_ID,
    SHEETS,
    CREDENTIALS_FILE,
    SCOPES,
    COLUMN_MAPPING
)

def load_credentials():
    """Carrega as credenciais do Google Sheets"""
    try:
        if not os.path.exists(CREDENTIALS_FILE):
            st.error("Erro ao carregar credenciais. Entre em contato com o suporte.")
            return None

        return service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE,
            scopes=SCOPES
        )
    except Exception as e:
        st.error("Erro ao carregar credenciais. Entre em contato com o suporte.")
        return None

def get_sheet_data(sheet_info):
    """Lê os dados da planilha do Google Sheets"""
    try:
        credentials = load_credentials()
        if not credentials:
            return None

        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()

        try:
            result = sheet.values().get(
                spreadsheetId=SPREADSHEET_ID,
                range=sheet_info['range']
            ).execute()
        except HttpError:
            st.error(f"Erro ao acessar a planilha {sheet_info['name']}. Entre em contato com o suporte.")
            return None

        values = result.get('values', [])
        if not values:
            st.warning(f'Nenhum dado encontrado na planilha {sheet_info["name"]}.')
            return None

        # Converte para DataFrame
        df = pd.DataFrame(values[1:], columns=values[0])
        
        # Remove linhas vazias
        df = df.dropna(how='all')
        
        # Renomeia as colunas conforme mapeamento
        df = df.rename(columns=COLUMN_MAPPING)
        
        return df

    except Exception as e:
        st.error(f"Erro inesperado ao ler {sheet_info['name']}. Entre em contato com o suporte.")
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
        df = get_sheet_data(SHEETS['JULIO'])
    
    if df is None:
        st.stop()
    
    # Debug - mostra os nomes das colunas
    st.write("Colunas disponíveis:", list(df.columns))
    
    # Seleciona colunas relevantes usando os nomes mapeados
    colunas_relevantes = [
        'DATA', 'RESOLUCAO', 'CTT', 'NUMERO', 'DEMANDA', 
        'ESCRITORIO', 'ATIVO_RECEPTIVO', 'DIRETOR'
    ]
    df1_selecionado = df[colunas_relevantes].copy()
    
    # Filtros na sidebar
    st.sidebar.title("🔍 Filtros")
    
    # Filtro de Escritório
    escritorios = ['Todos'] + sorted(df1_selecionado['ESCRITORIO'].dropna().unique().tolist())
    escritorio_padrao = 'ANTONIO MARINGA' if 'ANTONIO MARINGA' in escritorios else escritorios[0]
    escritorio_selecionado = st.sidebar.selectbox("Escritório", escritorios, index=escritorios.index(escritorio_padrao))
    
    # Filtro de Diretor
    diretores = ['Todos'] + sorted(df1_selecionado['DIRETOR'].dropna().unique().tolist())
    diretor_selecionado = st.sidebar.selectbox("Diretor", diretores, index=diretores.index('JULIO') if 'JULIO' in diretores else 0)
    
    # Filtro de Status
    status = ['Todos'] + sorted(df1_selecionado['ATIVO_RECEPTIVO'].dropna().unique().tolist())
    status_selecionado = st.sidebar.selectbox("Status", status, index=status.index('ATIVO') if 'ATIVO' in status else 0)
    
    # Aplica filtros
    df_filtrado = df1_selecionado.copy()
    
    if escritorio_selecionado != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['ESCRITORIO'] == escritorio_selecionado]
    
    if diretor_selecionado != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['DIRETOR'] == diretor_selecionado]
    
    if status_selecionado != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['ATIVO_RECEPTIVO'] == status_selecionado]
    
    # Métricas principais
    st.subheader("📈 Métricas Principais")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Demandas", len(df_filtrado))
    with col2:
        st.metric("Escritório", escritorio_selecionado)
    with col3:
        st.metric("Diretor", diretor_selecionado)
    with col4:
        st.metric("Status", status_selecionado)
    
    # Análises
    col1, col2 = st.columns(2)
    
    with col1:
        # Análise por Resolução
        st.subheader("📊 Análise por Resolução")
        resolucoes = df_filtrado['RESOLUCAO'].value_counts()
        
        for resolucao, total in resolucoes.items():
            if pd.notna(resolucao) and resolucao.strip():
                col_a, col_b = st.columns([1, 4])
                with col_a:
                    st.metric(resolucao, total)
                with col_b:
                    progress = total / len(df_filtrado)
                    st.progress(progress)
                    st.caption(f"{progress:.1%}")
    
    with col2:
        # Análise por Status
        st.subheader("📊 Análise por Status")
        status_counts = df_filtrado['ATIVO_RECEPTIVO'].value_counts()
        
        for status, total in status_counts.items():
            if pd.notna(status) and status.strip():
                col_a, col_b = st.columns([1, 4])
                with col_a:
                    st.metric(status, total)
                with col_b:
                    progress = total / len(df_filtrado)
                    st.progress(progress)
                    st.caption(f"{progress:.1%}")
    
    # Análise por Escritório
    st.subheader("📊 Análise por Escritório")
    escritorios_count = df_filtrado['ESCRITORIO'].value_counts().head(10)
    
    for escritorio, total in escritorios_count.items():
        if pd.notna(escritorio) and escritorio.strip():
            col1, col2 = st.columns([1, 4])
            with col1:
                st.metric(escritorio, total)
            with col2:
                progress = total / len(df_filtrado)
                st.progress(progress)
                st.caption(f"{progress:.1%}")
    
    # Tabela detalhada
    st.subheader("📋 Detalhamento das Demandas")
    st.dataframe(
        df_filtrado.sort_values('DATA', ascending=False),
        use_container_width=True,
        hide_index=True
    )

if __name__ == "__main__":
    main()
