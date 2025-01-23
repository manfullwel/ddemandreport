import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

class AnaliseDiaria:
    def __init__(self):
        self.status_counts = {
            'RESOLVIDOS': 127,
            'PENDENTE ATIVO': 249,
            'PENDENTE RECEPTIVO': 178,
            'PRIORIDADE': 5,
            'PRIORIDADE TOTAL': 3,
            'SOMA DAS PRIORIDADES': 8,
            'ANÁLISE': 38,
            'ANÁLISE DO DIA': 31,
            'RECEPTIVO': 0,
            'QUITADO CLIENTE': 0,
            'QUITADO': 9,
            'APROVADOS': 31
        }
        
        self.colaboradores = {
            'MARIA BRUNA': 15,
            'AMANDA SANTANA': 14,
            'BRUNO MARIANO': 0,
            'EDIANE': 15,
            'FABIANA': 16,
            'ITAYNNARA': 8,
            'VITORIA': 0,
            'SABRINA': 0,
            'JULIA': 14,
            'KATIA': 9,
            'ALINE SALVADOR': 10,
            'VICTOR ADRIANO': 5,
            'JULIANA': 0,
            'GREICY': 2,
            'SOFIA': 0
        }
        
        self.data_analise = datetime.now()
        
    def gerar_relatorio_status(self):
        """Gera um gráfico de barras para os status"""
        fig = go.Figure(data=[
            go.Bar(
                x=list(self.status_counts.keys()),
                y=list(self.status_counts.values()),
                text=list(self.status_counts.values()),
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title='Distribuição de Status',
            xaxis_title='Status',
            yaxis_title='Quantidade',
            xaxis_tickangle=-45,
            height=600
        )
        
        # Salvar o gráfico
        output_dir = Path('docs/relatorios')
        output_dir.mkdir(parents=True, exist_ok=True)
        fig.write_html(output_dir / 'status_diario.html')
        
    def gerar_relatorio_colaboradores(self):
        """Gera um gráfico de barras para os colaboradores"""
        # Ordenar colaboradores por quantidade
        sorted_colab = dict(sorted(self.colaboradores.items(), 
                                 key=lambda x: x[1], 
                                 reverse=True))
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(sorted_colab.keys()),
                y=list(sorted_colab.values()),
                text=list(sorted_colab.values()),
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title='Demandas Resolvidas por Colaborador',
            xaxis_title='Colaborador',
            yaxis_title='Quantidade',
            xaxis_tickangle=-45,
            height=600
        )
        
        # Salvar o gráfico
        output_dir = Path('docs/relatorios')
        output_dir.mkdir(parents=True, exist_ok=True)
        fig.write_html(output_dir / 'colaboradores_diario.html')
        
    def calcular_metricas(self):
        """Calcula métricas importantes"""
        total_demandas = sum(self.status_counts.values())
        total_resolvido = self.status_counts['RESOLVIDOS']
        total_pendente = (self.status_counts['PENDENTE ATIVO'] + 
                         self.status_counts['PENDENTE RECEPTIVO'])
        total_analise = self.status_counts['ANÁLISE']
        
        # Métricas por colaborador
        media_resolucao = sum(self.colaboradores.values()) / len([v for v in self.colaboradores.values() if v > 0])
        top_colaborador = max(self.colaboradores.items(), key=lambda x: x[1])
        
        return {
            'total_demandas': total_demandas,
            'total_resolvido': total_resolvido,
            'total_pendente': total_pendente,
            'total_analise': total_analise,
            'media_resolucao': media_resolucao,
            'top_colaborador': top_colaborador
        }
    
    def gerar_relatorio_html(self):
        """Gera um relatório HTML completo"""
        metricas = self.calcular_metricas()
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Relatório Diário - {self.data_analise.strftime('%d/%m/%Y')}</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                .metric-card {{
                    background: #f8f9fa;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 10px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .metric-value {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #0d6efd;
                }}
            </style>
        </head>
        <body>
            <div class="container py-5">
                <h1 class="text-center mb-5">Relatório Diário - {self.data_analise.strftime('%d/%m/%Y')}</h1>
                
                <div class="row mb-4">
                    <div class="col-md-3">
                        <div class="metric-card">
                            <h5>Total de Demandas</h5>
                            <div class="metric-value">{metricas['total_demandas']}</div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="metric-card">
                            <h5>Resolvidas</h5>
                            <div class="metric-value">{metricas['total_resolvido']}</div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="metric-card">
                            <h5>Pendentes</h5>
                            <div class="metric-value">{metricas['total_pendente']}</div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="metric-card">
                            <h5>Em Análise</h5>
                            <div class="metric-value">{metricas['total_analise']}</div>
                        </div>
                    </div>
                </div>
                
                <div class="row mb-4">
                    <div class="col-md-6">
                        <div class="metric-card">
                            <h5>Média de Resolução por Colaborador</h5>
                            <div class="metric-value">{metricas['media_resolucao']:.1f}</div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="metric-card">
                            <h5>Colaborador Destaque</h5>
                            <div class="metric-value">{metricas['top_colaborador'][0]} ({metricas['top_colaborador'][1]})</div>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-12 mb-4">
                        <iframe src="status_diario.html" width="100%" height="600px" frameborder="0"></iframe>
                    </div>
                    <div class="col-12">
                        <iframe src="colaboradores_diario.html" width="100%" height="600px" frameborder="0"></iframe>
                    </div>
                </div>
            </div>
            
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
        </body>
        </html>
        """
        
        output_dir = Path('docs/relatorios')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(output_dir / 'index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

def main():
    analise = AnaliseDiaria()
    analise.gerar_relatorio_status()
    analise.gerar_relatorio_colaboradores()
    analise.gerar_relatorio_html()
    print("Relatório gerado com sucesso!")

if __name__ == "__main__":
    main()
