# Dashboard de Análise de Demandas

Dashboard profissional para análise e acompanhamento de demandas em tempo real.

## Funcionalidades

- **Análise em Tempo Real**
  - KPIs principais (total, em progresso, concluídas, pendentes)
  - Gráficos interativos de distribuição por status
  - Visualização de demandas por grupo
  - Filtros dinâmicos por data, grupo e status

- **Interface Moderna**
  - Sidebar para filtros
  - Layout responsivo
  - Visualização otimizada
  - Design profissional

## Requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)
- Navegador web moderno

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/manfullwel/ddemandreport.git
cd ddemandreport
```

2. (Opcional) Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Executando o Dashboard

1. Execute o servidor:
```bash
python app.py
```

2. Acesse o dashboard em: http://localhost:8050

## Estrutura do Projeto

```
demo/
├── app.py           # Aplicação principal
├── requirements.txt # Dependências
└── README.md       # Documentação
```

## Tecnologias

- **Frontend**
  - Dash
  - Plotly
  - Bootstrap Components

- **Backend**
  - Python
  - Pandas
  - NumPy

## Dados

O dashboard inclui um gerador de dados de exemplo para demonstração. Em um ambiente de produção, você pode:

1. Modificar a função `generate_sample_data()` em `app.py`
2. Conectar com sua própria fonte de dados
3. Importar dados de arquivos CSV/Excel

## Suporte

Para suporte ou dúvidas, abra uma issue no GitHub.
