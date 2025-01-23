"""
Ferramenta de debug interno para análise da planilha do Google Sheets.
Uso exclusivo para desenvolvimento e testes.
"""

import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from config import (
    SPREADSHEET_ID,
    SHEETS,
    CREDENTIALS_FILE,
    SCOPES
)

def load_credentials():
    """Carrega as credenciais do Google Sheets"""
    try:
        if not os.path.exists(CREDENTIALS_FILE):
            print(f"[ERRO] Arquivo de credenciais não encontrado: {CREDENTIALS_FILE}")
            return None

        credentials = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE,
            scopes=SCOPES
        )
        print("[OK] Credenciais carregadas com sucesso!")
        return credentials
    except Exception as e:
        print(f"[ERRO] Erro ao carregar credenciais: {str(e)}")
        return None

def analyze_sheet(service, sheet_info):
    """Analisa uma única planilha"""
    print(f"\n[INFO] Analisando planilha: {sheet_info['name']}")
    print(f"[INFO] Range: {sheet_info['range']}")
    
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=sheet_info['range']
        ).execute()
        
        values = result.get('values', [])
        if not values:
            print("[ERRO] Nenhum dado encontrado na planilha")
            return
        
        # Análise do cabeçalho
        print("\n[INFO] Análise do Cabeçalho:")
        header = values[0]
        for i, col in enumerate(header):
            print(f"Coluna {i}: '{col}'")
        
        # Converte para DataFrame para análise
        df = pd.DataFrame(values[1:], columns=header)
        
        # Análise básica
        print(f"\n[INFO] Total de linhas: {len(df)}")
        print(f"[INFO] Total de colunas: {len(df.columns)}")
        
        # Análise de valores únicos por coluna
        print("\n[INFO] Valores únicos por coluna:")
        for col in df.columns:
            unique_values = df[col].dropna().unique()
            print(f"\n'{col}':")
            print(f"- Número de valores únicos: {len(unique_values)}")
            if len(unique_values) < 10:  # Mostra valores apenas se houver poucos
                print(f"- Valores: {sorted(unique_values)}")
        
        # Análise de dados faltantes
        print("\n[INFO] Análise de dados faltantes:")
        missing = df.isna().sum()
        for col, count in missing.items():
            if count > 0:
                print(f"'{col}': {count} valores faltantes ({count/len(df):.1%})")
        
        return df
        
    except Exception as e:
        print(f"[ERRO] Erro ao analisar planilha: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return None

def main():
    print("[INFO] Iniciando debug das planilhas...")
    print(f"[INFO] Planilha ID: {SPREADSHEET_ID}")
    
    credentials = load_credentials()
    if not credentials:
        return
    
    service = build('sheets', 'v4', credentials=credentials)
    
    # Analisa cada planilha separadamente
    for key, sheet_info in SHEETS.items():
        df = analyze_sheet(service, sheet_info)
        if df is not None:
            # Salva uma amostra dos dados para análise offline
            sample_file = f"sheet_sample_{key}.csv"
            df.head(10).to_csv(sample_file, index=False, encoding='utf-8')
            print(f"\n[OK] Amostra dos dados salvos em {sample_file}")

if __name__ == "__main__":
    main()
