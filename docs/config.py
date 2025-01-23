"""
Configurações para acesso à planilha do Google Sheets.
"""
import os

# ID da planilha
SPREADSHEET_ID = "1_TmRgpFGmXkLenbACQpWHNAZuT94CTzlG9DZV0KmC8g"

# Nome das abas e ranges
SHEETS = {
    'JULIO': {
        'name': 'DEMANDAS JULIO',
        'range': 'DEMANDAS JULIO!A:H'
    }
}

# Mapeamento de colunas da planilha
COLUMN_MAPPING = {
    ' DATA': 'DATA',                     # Mantém o espaço no início
    'RESOLUÇÃO': 'RESOLUCAO',            # Mantém o acento
    'CTT': 'CTT',                        # Mantém como está
    'N°': 'NUMERO',                      # Usa o símbolo correto
    'DEMANDA': 'DEMANDA',                # Mantém como está
    'ESCRITÓRIO': 'ESCRITORIO',          # Mantém o acento
    'ATIVO/RECEPTIVO': 'ATIVO_RECEPTIVO', # Mantém a barra
    'DIRETOR': 'DIRETOR'                 # Mantém como está
}

# Status possíveis para análise
STATUS_ANALISE = [
    'ATIVO',
    'RECEPTIVO'
]

# Configurações de autenticação
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "service_account.json")

# Escopo necessário para leitura da planilha
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
