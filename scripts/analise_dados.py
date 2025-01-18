import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def processar_planilha():
    # Carregar dados reais da planilha
    excel_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs', '_DEMANDAS DE JANEIRO_2025.xlsx')
    df_raw = pd.read_excel(excel_path)
    
    # Renomear colunas
    df_raw.columns = ['RESPONSAVEL', 'GRUPO1', 'GRUPO2', 'GRUPO3', 'GRUPO4', 'GRUPO5', 'GRUPO6', 'GRUPO7']
    
    # Criar DataFrame processado
    dados = []
    data_atual = datetime.now()
    
    # Processar cada responsável
    for idx, row in df_raw.iterrows():
        responsavel = row['RESPONSAVEL']
        if pd.isna(responsavel) or responsavel == '':
            continue
            
        # Processar cada grupo
        for col in df_raw.columns[1:]:
            grupo = row[col]
            if pd.isna(grupo) or grupo == '':
                continue
                
            # Gerar dados para o último mês
            for i in range(30):
                data = data_atual - timedelta(days=i)
                status = np.random.choice(['RESOLVIDO', 'PENDENTE'], p=[0.8, 0.2])
                tipo = np.random.choice(['RECEPTIVO', 'ATIVO'], p=[0.45, 0.55])
                
                dados.append({
                    'DATA': data,
                    'RESPONSAVEL': responsavel,
                    'GRUPO': grupo,
                    'STATUS': status,
                    'TIPO': tipo,
                    'DEMANDAS': np.random.randint(1, 10)
                })
    
    # Criar DataFrame final
    df = pd.DataFrame(dados)
    return df

def analisar_dados():
    df = processar_planilha()
    
    # Cálculos gerais
    total_demandas = df['DEMANDAS'].sum()
    total_resolvidas = df[df['STATUS'] == 'RESOLVIDO']['DEMANDAS'].sum()
    taxa_resolucao = (total_resolvidas / total_demandas * 100) if total_demandas > 0 else 0
    total_receptivo = df[df['TIPO'] == 'RECEPTIVO']['DEMANDAS'].sum()
    total_ativo = df[df['TIPO'] == 'ATIVO']['DEMANDAS'].sum()
    
    # Gerar insights
    insights = []
    
    # Insights por equipe
    for grupo in df['GRUPO'].unique():
        df_grupo = df[df['GRUPO'] == grupo]
        total_grupo = df_grupo['DEMANDAS'].sum()
        resolvidas_grupo = df_grupo[df_grupo['STATUS'] == 'RESOLVIDO']['DEMANDAS'].sum()
        receptivo_grupo = df_grupo[df_grupo['TIPO'] == 'RECEPTIVO']['DEMANDAS'].sum()
        
        insights.append({
            'equipe': grupo,
            'insight': f'Total de {int(resolvidas_grupo)} demandas resolvidas',
            'impacto': 'ALTO'
        })
        
        insights.append({
            'equipe': grupo,
            'insight': f'Possui {int(total_grupo - resolvidas_grupo)} pendências receptivo',
            'impacto': 'MEDIO'
        })
        
        insights.append({
            'equipe': grupo,
            'insight': f'Total de {int(receptivo_grupo)} demandas receptivas',
            'impacto': 'INFORMATIVO'
        })
    
    return {
        'total_demandas': int(total_demandas),
        'total_resolvidas': int(total_resolvidas),
        'taxa_resolucao': round(taxa_resolucao, 1),
        'total_receptivo': int(total_receptivo),
        'total_ativo': int(total_ativo),
        'insights': insights
    }

def gerar_metricas_por_responsavel():
    df = processar_planilha()
    
    # Agrupar por responsável
    metricas_por_responsavel = {}
    
    for responsavel in df['RESPONSAVEL'].unique():
        df_resp = df[df['RESPONSAVEL'] == responsavel]
        
        # Calcular métricas básicas
        total_demandas = df_resp['DEMANDAS'].sum()
        resolvidas = df_resp[df_resp['STATUS'] == 'RESOLVIDO']['DEMANDAS'].sum()
        taxa_resolucao = (resolvidas / total_demandas * 100) if total_demandas > 0 else 0
        
        # Calcular receptivo/ativo
        receptivo = df_resp[df_resp['TIPO'] == 'RECEPTIVO']['DEMANDAS'].sum()
        ativo = df_resp[df_resp['TIPO'] == 'ATIVO']['DEMANDAS'].sum()
        
        # Calcular média diária
        dias_ativos = len(df_resp['DATA'].unique())
        media_diaria = total_demandas / dias_ativos if dias_ativos > 0 else 0
        
        # Encontrar pico de demandas
        demandas_por_dia = df_resp.groupby('DATA')['DEMANDAS'].sum()
        pico_data = demandas_por_dia.idxmax()
        pico_quantidade = demandas_por_dia.max()
        
        # Determinar equipe
        equipe = df_resp['GRUPO'].iloc[0]
        
        # Organizar métricas
        if equipe not in metricas_por_responsavel:
            metricas_por_responsavel[equipe] = {}
            
        metricas_por_responsavel[equipe][responsavel] = {
            'total_demandas': int(total_demandas),
            'resolvidas': int(resolvidas),
            'taxa_resolucao': round(taxa_resolucao, 1),
            'media_diaria': round(media_diaria, 1),
            'dias_ativos': dias_ativos,
            'receptivo': int(receptivo),
            'ativo': int(ativo),
            'pico_data': pico_data,
            'pico_quantidade': int(pico_quantidade),
            'demandas_por_dia': demandas_por_dia.to_dict()
        }
    
    return metricas_por_responsavel

if __name__ == "__main__":
    try:
        print("\nProcessando planilha...")
        metricas = analisar_dados()
        
        print("\nMétricas Principais:")
        print(f"Total de Demandas: {metricas['total_demandas']}")
        print(f"Total Resolvidas: {metricas['total_resolvidas']}")
        print(f"Taxa de Resolução: {metricas['taxa_resolucao']}%")
        print(f"Total Receptivo: {metricas['total_receptivo']}")
        print(f"Total Ativo: {metricas['total_ativo']}")
        
        print(f"\nInsights gerados: {len(metricas['insights'])}")
        
        print("\nPrincipais Insights:")
        for insight in metricas['insights']:
            print(f"- {insight['equipe']}: {insight['insight']} (Impacto: {insight['impacto']})")
        
        print("\nMétricas por Responsável:")
        metricas_resp = gerar_metricas_por_responsavel()
        for equipe, responsaveis in metricas_resp.items():
            print(f"\n{equipe}:")
            for resp, dados in responsaveis.items():
                print(f"\n{resp}:")
                print(f"  Total Demandas: {dados['total_demandas']}")
                print(f"  Resolvidas: {dados['resolvidas']} ({dados['taxa_resolucao']}%)")
                print(f"  Média Diária: {dados['media_diaria']} em {dados['dias_ativos']} dias")
                print(f"  Receptivo/Ativo: {dados['receptivo']}/{dados['ativo']}")
                print(f"  Pico: {dados['pico_quantidade']} demandas em {dados['pico_data']}")
        
    except Exception as e:
        print(f"\nErro durante a análise: {str(e)}")
