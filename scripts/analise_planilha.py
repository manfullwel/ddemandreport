import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import Counter, defaultdict

def conectar_planilha():
    """Conecta à planilha do Google Sheets"""
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'credentials.json', scope)
    
    gc = gspread.authorize(credentials)
    
    # Abrir a planilha pelo ID (substitua pelo ID da sua planilha)
    planilha = gc.open_by_key('your-spreadsheet-id')
    
    # Selecionar a aba específica
    aba = planilha.worksheet('DEMANDAS LEANDROADRIANO')
    
    # Converter para DataFrame
    dados = pd.DataFrame(aba.get_all_records())
    return dados

def analisar_dados(df):
    """Analisa os dados da planilha"""
    # Filtrar apenas registros do dia atual
    hoje = datetime.now().strftime('%d/%m/%Y')
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y', errors='coerce')
    df_hoje = df[df['Data'].dt.strftime('%d/%m/%Y') == hoje]
    
    # Contagem de status
    status_counts = Counter(df_hoje['Status'])
    
    # Contagem por colaborador
    demandas_por_colaborador = Counter(df_hoje[df_hoje['Status'] == 'RESOLVIDOS']['Colaborador'])
    
    return status_counts, demandas_por_colaborador

def imprimir_resultados(status_counts, demandas_por_colaborador):
    """Imprime os resultados no formato especificado"""
    # Imprimir contagem de status
    print("\nStatus do dia:")
    print("=" * 50)
    for status, count in status_counts.items():
        print(f"{status}: {count}")
    
    # Calcular total de demandas resolvidas
    total_resolvido = sum(demandas_por_colaborador.values())
    
    print("\nDemandas resolvidas por colaborador:")
    print("=" * 50)
    for colab, count in sorted(demandas_por_colaborador.items()):
        print(f"{colab}: {count}")
    
    print(f"\nTOTAL = {total_resolvido}")

def main():
    try:
        print("Conectando à planilha...")
        df = conectar_planilha()
        
        print("Analisando dados...")
        status_counts, demandas_por_colaborador = analisar_dados(df)
        
        print("\nRESULTADOS DA ANÁLISE")
        print("=" * 50)
        imprimir_resultados(status_counts, demandas_por_colaborador)
        
    except Exception as e:
        print(f"Erro ao processar dados: {str(e)}")

if __name__ == "__main__":
    main()
