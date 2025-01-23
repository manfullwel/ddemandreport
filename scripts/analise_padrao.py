import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import Counter, defaultdict
from colorama import init, Fore, Style

# Inicializar colorama para cores no terminal
init()

class AnalisePadrao:
    def __init__(self):
        # Padrões esperados para comparação
        self.padrao_status = {
            'RESOLVIDO': 127,
            'PENDENTE': 249,
            'PRIORIDADE': 5,
            'PRIORIDADE TOTAL': 3,
            'SOMA DAS PRIORIDADES': 8,
            'ANÁLISE': 38,
            'ANÁLISE DO DIA': 31
        }
        
        self.padrao_colaboradores = {
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
        
        self.total_padrao = 148

    def conectar_planilha(self):
        """Conecta à planilha do Google Sheets"""
        print(f"{Fore.CYAN}[DEBUG] Iniciando conexão com a planilha...{Style.RESET_ALL}")
        
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        
        # Usar credenciais da conta de serviço
        credentials_path = 'F:/demandstest/panilhas-448405-29bde26e8961.json'
        print(f"{Fore.CYAN}[DEBUG] Usando arquivo de credenciais: {credentials_path}{Style.RESET_ALL}")
        
        try:
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                credentials_path, scope)
            print(f"{Fore.GREEN}[DEBUG] Credenciais carregadas com sucesso{Style.RESET_ALL}")
            
            gc = gspread.authorize(credentials)
            print(f"{Fore.GREEN}[DEBUG] Autorização concluída{Style.RESET_ALL}")
            
            # ID da planilha
            planilha = gc.open_by_key('1_TmRgpFGmXkLenbACQpWHNAZuT94CTzlG9DZV0KmC8g')
            print(f"{Fore.GREEN}[DEBUG] Planilha aberta com sucesso{Style.RESET_ALL}")
            
            # Listar todas as abas disponíveis
            worksheets = planilha.worksheets()
            print(f"{Fore.CYAN}[DEBUG] Abas disponíveis:{Style.RESET_ALL}")
            for ws in worksheets:
                print(f"{Fore.CYAN}[DEBUG] - {ws.title}{Style.RESET_ALL}")
            
            # Selecionar a aba específica
            aba = planilha.worksheet('DEMANDA LEANDROADRIANO')
            print(f"{Fore.GREEN}[DEBUG] Aba selecionada: DEMANDA LEANDROADRIANO{Style.RESET_ALL}")
            
            # Obter todos os valores
            valores = aba.get_all_values()
            print(f"{Fore.CYAN}[DEBUG] Total de linhas obtidas: {len(valores)}{Style.RESET_ALL}")
            
            # Pegar o cabeçalho (primeira linha)
            headers = valores[0]
            print(f"{Fore.CYAN}[DEBUG] Cabeçalhos encontrados: {headers}{Style.RESET_ALL}")
            
            # Criar cabeçalhos únicos adicionando um número para duplicados
            unique_headers = []
            header_count = {}
            
            for header in headers:
                if header in header_count:
                    header_count[header] += 1
                    unique_headers.append(f"{header}_{header_count[header]}")
                else:
                    header_count[header] = 1
                    unique_headers.append(header)
            
            # Converter para DataFrame usando os cabeçalhos únicos
            dados = pd.DataFrame(valores[1:], columns=unique_headers)
            print(f"{Fore.GREEN}[DEBUG] Dados convertidos para DataFrame. Total de linhas: {len(dados)}{Style.RESET_ALL}")
            
            return dados
            
        except Exception as e:
            print(f"{Fore.RED}[DEBUG] Erro ao acessar planilha: {str(e)}{Style.RESET_ALL}")
            print(f"{Fore.RED}[DEBUG] Tipo do erro: {type(e)}{Style.RESET_ALL}")
            raise e

    def analisar_dados(self, df):
        """Analisa os dados da planilha e compara com os padrões"""
        # Verificar formato das datas
        print(f"{Fore.CYAN}[DEBUG] Primeiras 5 datas na planilha:{Style.RESET_ALL}")
        print(df['DATA'].head())
        
        # Filtrar apenas registros do dia atual
        hoje = datetime.now().strftime('%d/%m/%Y')
        print(f"{Fore.CYAN}[DEBUG] Filtrando registros para a data: {hoje}{Style.RESET_ALL}")
        
        # Tentar converter a coluna de data
        try:
            df['DATA'] = pd.to_datetime(df['DATA'], format='%d/%m/%Y', errors='coerce')
            print(f"{Fore.CYAN}[DEBUG] Datas após conversão:{Style.RESET_ALL}")
            print(df['DATA'].head())
            
            df_hoje = df[df['DATA'].dt.strftime('%d/%m/%Y') == hoje]
            print(f"{Fore.CYAN}[DEBUG] Total de registros para hoje: {len(df_hoje)}{Style.RESET_ALL}")
            
            # Se não houver registros para hoje, mostrar registros mais recentes
            if len(df_hoje) == 0:
                ultima_data = df['DATA'].max()
                df_recente = df[df['DATA'] == ultima_data]
                print(f"{Fore.YELLOW}[DEBUG] Nenhum registro para hoje. Mostrando registros da última data: {ultima_data.strftime('%d/%m/%Y')}")
                print(f"Total de registros: {len(df_recente)}{Style.RESET_ALL}")
                df_hoje = df_recente
            
            # Mostrar todas as colunas disponíveis
            print(f"{Fore.CYAN}[DEBUG] Todas as colunas disponíveis:{Style.RESET_ALL}")
            for col in df_hoje.columns:
                print(f"- {col}")
            
            # Mostrar algumas linhas de exemplo
            print(f"{Fore.CYAN}[DEBUG] Primeiras 5 linhas dos dados:{Style.RESET_ALL}")
            print(df_hoje.head())
            
            # Verificar valores únicos das colunas
            print(f"{Fore.CYAN}[DEBUG] Valores únicos na coluna RESPONSAVEL:{Style.RESET_ALL}")
            print(df_hoje['  RESPONSAVEL'].unique())
            
            print(f"{Fore.CYAN}[DEBUG] Valores únicos na coluna SITUAÇÃO:{Style.RESET_ALL}")
            print(df_hoje['SITUAÇÃO'].unique())
            
        except Exception as e:
            print(f"{Fore.RED}[DEBUG] Erro ao converter datas: {str(e)}{Style.RESET_ALL}")
            raise e
        
        # Contagem de status
        status_atual = Counter(df_hoje['SITUAÇÃO'])
        print(f"{Fore.CYAN}[DEBUG] Status encontrados: {dict(status_atual)}{Style.RESET_ALL}")
        
        # Contagem por colaborador
        colaboradores_atual = Counter(df_hoje[df_hoje['SITUAÇÃO'] == 'RESOLVIDO']['  RESPONSAVEL'])
        print(f"{Fore.CYAN}[DEBUG] Colaboradores encontrados: {dict(colaboradores_atual)}{Style.RESET_ALL}")
        
        return status_atual, colaboradores_atual

    def comparar_e_imprimir(self, status_atual, colaboradores_atual):
        """Compara os dados atuais com os padrões e imprime os resultados"""
        hoje = datetime.now().strftime('%d/%m/%Y')
        
        print(f"\nANÁLISE COMPARATIVA - {hoje}")
        print("=" * 80)
        
        # Análise de status
        print("\nANÁLISE DE STATUS")
        print("-" * 80)
        for status, padrao in self.padrao_status.items():
            atual = status_atual.get(status, 0)
            diff = atual - padrao
            print(f"{status}: {atual} (Padrão: {padrao}, Diferença: {'+' if diff >= 0 else ''}{diff})")
        
        # Análise por colaborador
        print("\nANÁLISE POR COLABORADOR")
        print("-" * 80)
        for colab, padrao in self.padrao_colaboradores.items():
            atual = colaboradores_atual.get(colab, 0)
            diff = atual - padrao
            print(f"{colab}: {atual} (Padrão: {padrao}, Diferença: {'+' if diff >= 0 else ''}{diff})")
        
        # Total e média
        print("\n" + "=" * 80)
        total_atual = sum(colaboradores_atual.values())
        print(f"TOTAL ATUAL: {total_atual} (Padrão: {self.total_padrao}, Diferença: {'+' if total_atual - self.total_padrao >= 0 else ''}{total_atual - self.total_padrao})")
        
        print("\nANÁLISE DE PERFORMANCE")
        print("-" * 80)
        
        # Calcular média por colaborador ativo
        colaboradores_ativos = len([v for v in colaboradores_atual.values() if v > 0])
        media_atual = total_atual / colaboradores_ativos if colaboradores_ativos > 0 else 0
        media_padrao = self.total_padrao / len([v for v in self.padrao_colaboradores.values() if v > 0])
        
        print("Média de resolução por colaborador ativo:")
        print(f"Atual: {media_atual:.1f}")
        print(f"Padrão: {media_padrao:.1f}")
        
        print("\nColaboradores acima do padrão:")
        encontrou_acima = False
        for colab, atual in colaboradores_atual.items():
            padrao = self.padrao_colaboradores.get(colab, 0)
            if atual > padrao:
                print(f"- {colab} ({atual} vs {padrao})")
                encontrou_acima = True
        
        if not encontrou_acima:
            print("Nenhum colaborador acima do padrão hoje")

def main():
    try:
        analise = AnalisePadrao()
        print(f"{Fore.CYAN}Conectando à planilha...{Style.RESET_ALL}")
        df = analise.conectar_planilha()
        
        print(f"{Fore.CYAN}Analisando dados...{Style.RESET_ALL}")
        status_atual, colaboradores_atual = analise.analisar_dados(df)
        
        analise.comparar_e_imprimir(status_atual, colaboradores_atual)
        
    except Exception as e:
        print(f"{Fore.RED}Erro ao processar dados: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
