# Demand Report - Sistema de Gestão de Demandas em Tempo Real

<div align="center">

### 🚀 Sistema Inteligente de Gestão e Análise de Demandas

[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

</div>

## 📱 Demonstração do Sistema

### Grupos e Equipes

<div align="center">

#### Grupo Julio
![Grupo Julio](public/screenshots/grupo_julio.png)

#### Grupo Leandro e Adriano
![Grupo Leandro e Adriano](public/screenshots/grupo_leandro.png)

</div>

### 📊 Analisador de Relatórios

O sistema inclui um analisador de relatórios que permite:

1. **Upload de Arquivos CSV**
   - Suporte para arquivos do Relatório Diário
   - Análise automática dos dados
   - Visualização em tempo real do progresso

2. **Formato do Arquivo CSV**
   ```csv
   data,grupo,responsavel,contrato,status,ultima_atualizacao
   2025-01-14,Grupo Julio,Maria Silva,123456,Quitado,2025-01-14 14:30
   ```

3. **Métricas Geradas**
   - Total de demandas por grupo
   - Distribuição por status (Resolvidos, Pendentes, Quitados, Aprovados)
   - Desempenho individual dos membros
   - Última atualização de cada membro

4. **Visualização**
   - Gráficos interativos
   - Agrupamento por equipe
   - Detalhamento por membro
   - Histórico de atualizações

> Para acessar o analisador, execute o projeto localmente e acesse `http://localhost:5173/analisador`

### Versão Mobile

A versão mobile do sistema oferece:

- **Dashboard Otimizado**
  - Visualização clara de métricas importantes
  - Interface adaptada para toque
  - Carregamento rápido e eficiente

- **Sistema de Notificações**
  - Alertas em tempo real
  - Priorização visual de demandas urgentes
  - Interação rápida com notificações

- **Análises e Relatórios**
  - Gráficos otimizados para telas menores
  - Filtros e buscas simplificados
  - Exportação de dados facilitada

## 🌟 Por Que Este Sistema é Importante?

### Produtividade e Eficiência
- **Monitoramento em Tempo Real**: Acompanhamento instantâneo de todas as demandas
- **Redução de Tempo**: Diminuição significativa no tempo de resposta a demandas urgentes
- **Organização Inteligente**: Priorização automática baseada em critérios importantes

### Mobilidade e Acessibilidade
- **Acesso Universal**: Disponível em qualquer dispositivo, a qualquer momento
- **Notificações Instantâneas**: Alertas imediatos para demandas prioritárias
- **Interface Adaptativa**: Experiência otimizada tanto em desktop quanto em mobile

### Tomada de Decisão
- **Análise de Dados**: Métricas claras e objetivas para decisões estratégicas
- **Relatórios Detalhados**: Visão completa do desempenho individual e em equipe
- **Identificação de Padrões**: Análise de tendências para melhorias contínuas

## 🔄 Organograma do Projeto

<div align="center">

![Organograma do Projeto](screenshots/organograma.svg)

</div>

### Estrutura Atual

#### 1. Frontend (React + TypeScript)
- **Páginas**
  - `Demo`: Página inicial com demonstração do sistema
  - `RelatorioDiario`: Análise diária de demandas
  - `RelatorioGeral`: Visão geral das equipes
  - `MobileDemo`: Interface otimizada para mobile
  - `AnalisadorArquivos`: Upload e análise de relatórios
  - `Dashboard`: Painel principal do sistema

- **Componentes**
  - `FileUploadAnalyzer`: Processamento de arquivos CSV
  - `ErrorBoundary`: Tratamento de erros
  - `Dashboard`: Componentes do painel principal
  - `UI Components`: Biblioteca de componentes reutilizáveis

### Expansões Futuras

#### 1. Backend (Node.js + Express)
- API RESTful para gerenciamento de dados
- Autenticação e autorização
- Cache e otimização de performance
- Integração com serviços externos

#### 2. Database (PostgreSQL)
- Armazenamento estruturado de dados
- Histórico completo de demandas
- Backup e recuperação
- Queries otimizadas

#### 3. Recursos Avançados
- **Análise Preditiva**
  - Previsão de demandas
  - Identificação de padrões
  - Sugestões automáticas

- **Chatbot de Suporte**
  - Atendimento automatizado
  - FAQ inteligente
  - Direcionamento de demandas

- **Dashboards Personalizáveis**
  - Widgets configuráveis
  - Métricas personalizadas
  - Temas e layouts flexíveis

#### 4. Mobile Features
- **Push Notifications**
  - Alertas em tempo real
  - Priorização de mensagens
  - Configurações personalizadas

- **Offline Mode**
  - Sincronização automática
  - Cache local
  - Operações offline

- **Gestures & UX**
  - Interações touch otimizadas
  - Navegação intuitiva
  - Atualizações em tempo real

### Tecnologias Utilizadas

- **Frontend**
  - React 18
  - TypeScript 5
  - Tailwind CSS
  - Shadcn/ui
  - Vite

- **Futuras Implementações**
  - Node.js
  - Express
  - PostgreSQL
  - Redis (cache)
  - WebSocket
  - Machine Learning
  - PWA

## 💡 Inspiração e Agradecimentos

Este projeto foi inspirado nas necessidades reais do ambiente corporativo e contou com contribuições valiosas, especialmente de **Ediane F.**, que compartilhou insights fundamentais:

- Compreensão profunda do fluxo de trabalho diário
- Identificação de pontos críticos para otimização
- Sugestões práticas para melhorar a experiência do usuário
- Feedback sobre funcionalidades essenciais

## 🚀 Como Usar

1. Clone o repositório:
```bash
git clone https://github.com/manfullwel/ddemandreport.git
```

2. Instale as dependências:
```bash
cd ddemandreport
npm install
```

3. Execute o projeto:
```bash
npm run dev
```

## 🔄 Próximas Atualizações

- [ ] Integração com sistemas externos
- [ ] Análise preditiva de demandas
- [ ] Chatbot para suporte rápido
- [ ] Dashboards personalizáveis
- [ ] Módulo de relatórios avançados

## 👥 Contribuições

Este projeto é resultado de um esforço colaborativo, com destaque especial para:

- **Ediane F.** - Contribuições valiosas na definição do fluxo de trabalho e requisitos do sistema

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

<div align="center">
  <p>Desenvolvido com 💙 para otimizar o gerenciamento de demandas e impulsionar a produtividade das equipes.</p>
  <p>
    <a href="https://github.com/manfullwel/ddemandreport/issues">Reportar Bug</a>
    ·
    <a href="https://github.com/manfullwel/ddemandreport/issues">Sugerir Feature</a>
  </p>
</div>