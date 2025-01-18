import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from analise_dados import processar_planilha, analisar_dados, gerar_metricas_por_responsavel
import os

def configurar_estilo():
    # Configurar o estilo dos gráficos
    plt.style.use('default')
    sns.set_theme(style="whitegrid")
    sns.set_palette("husl")
    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12

def gerar_graficos():
    configurar_estilo()
    df = processar_planilha()
    metricas = analisar_dados()
    metricas_resp = gerar_metricas_por_responsavel()
    
    # Criar diretório para os gráficos se não existir
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'public', 'reports')
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Gráfico de Distribuição de Status por Grupo
    plt.figure(figsize=(12, 6))
    df_status = df.groupby(['GRUPO', 'STATUS'])['DEMANDAS'].sum().unstack()
    df_status.plot(kind='bar', stacked=True)
    plt.title('Distribuição de Status por Grupo')
    plt.xlabel('Grupo')
    plt.ylabel('Número de Demandas')
    plt.legend(title='Status')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'status_distribution.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Comparação entre Grupos
    plt.figure(figsize=(12, 6))
    grupos_stats = df.groupby('GRUPO').agg({
        'DEMANDAS': 'sum',
        'STATUS': lambda x: (x == 'RESOLVIDO').sum() / len(x) * 100,
        'TIPO': lambda x: (x == 'RECEPTIVO').sum() / len(x) * 100
    }).round(2)
    
    ax = grupos_stats.plot(kind='bar', width=0.8)
    plt.title('Comparação entre Grupos')
    plt.xlabel('Grupo')
    plt.ylabel('Valores')
    plt.legend(['Total Demandas', 'Taxa Resolução (%)', 'Taxa Receptivo (%)'])
    
    # Adicionar valores nas barras
    for i in ax.containers:
        ax.bar_label(i, fmt='%.1f', padding=3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'group_comparison.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Evolução Temporal por Grupo
    plt.figure(figsize=(12, 6))
    for grupo in df['GRUPO'].unique():
        df_grupo = df[df['GRUPO'] == grupo]
        demandas_diarias = df_grupo.groupby('DATA')['DEMANDAS'].sum()
        plt.plot(demandas_diarias.index, demandas_diarias.values, label=grupo, marker='o')
    
    plt.title('Evolução Temporal das Demandas por Grupo')
    plt.xlabel('Data')
    plt.ylabel('Número de Demandas')
    plt.legend(title='Grupo')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'temporal_evolution.png'), dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    try:
        print("Gerando gráficos...")
        gerar_graficos()
        print("Gráficos gerados com sucesso!")
    except Exception as e:
        print(f"Erro ao gerar gráficos: {str(e)}")
