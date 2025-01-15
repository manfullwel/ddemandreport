# Demand Count Sentinel 📊

> "A simplicidade é o último grau de sofisticação" - Leonardo da Vinci

Um dashboard revolucionário para monitoramento e análise de demandas em tempo real, inspirado nos princípios de visualização de dados de Edward Tufte e nas metodologias ágeis modernas.

[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-B73BFE?style=for-the-badge&logo=vite&logoColor=FFD62E)](https://vitejs.dev/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

## 🎯 Visão Geral

O Demand Count Sentinel nasceu da necessidade de transformar dados complexos em insights acionáveis. Inspirado por obras como "Information Dashboard Design" de Stephen Few e "The Visual Display of Quantitative Information" de Edward Tufte, desenvolvemos uma solução que combina elegância visual com funcionalidade prática.

### 📈 Exemplo de Impacto Real

```markdown
RELATÓRIO GERAL DE DEMANDAS (10/01/2025)

🔵 Equipe Julio
┌─────────────────────────┬─────────┐
│ Métricas               │ Valores │
├─────────────────────────┼─────────┤
│ ✅ Resolvidos          │    140  │
│ 📥 Pendentes Receptivo │    102  │
│ 📤 Pendentes Ativo     │    701  │
│ ⚡ Prioridades         │      3  │
│ 📊 Análises do Dia     │      3  │
│ 📈 Total Análises      │     49  │
│ 💰 Quitados            │      9  │
│ ✨ Aprovados           │      2  │
│ 📞 Receptivo           │      0  │
└─────────────────────────┴─────────┘

🔵 Equipe Adriano/Leandro
┌─────────────────────────┬─────────┐
│ Métricas               │ Valores │
├─────────────────────────┼─────────┤
│ ✅ Resolvidos          │    130  │
│ 📥 Pendentes Receptivo │    161  │
│ 📤 Pendentes Ativo     │    482  │
│ ⚡ Prioridades         │      1  │
│ 📊 Análises do Dia     │     20  │
│ 📈 Total Análises      │     32  │
│ 💰 Quitados            │     16  │
│ ✨ Aprovados           │      5  │
│ 📞 Receptivo           │      1  │
└─────────────────────────┴─────────┘

🎯 Totalizadores
┌──────────────────────┬─────────┐
│ Métrica             │ Total   │
├──────────────────────┼─────────┤
│ 💰 Quitados         │     26  │
│ 👥 Quitados Cliente │      1  │
│ ✨ Quitado Aprovado │      0  │
│ ⭐ Aprovados        │     91  │
│ 🔄 Aprovados Duplos │      6  │
└──────────────────────┴─────────┘
```

## 🌟 Por Que Demand Count Sentinel?

Nossa solução transforma dados brutos em narrativas visuais poderosas, permitindo que equipes:

- 🎯 **Tomem Decisões Mais Rápidas**: Visualização clara e intuitiva de KPIs críticos
- 📊 **Identifiquem Tendências**: Análise temporal de demandas e resoluções
- 🤝 **Melhorem Colaboração**: Visibilidade em tempo real do status de cada equipe
- ⚡ **Aumentem Produtividade**: Priorização inteligente de tarefas

## 💡 Inspiração e Filosofia

O design do Demand Count Sentinel é fundamentado em princípios consagrados:

- **Simplicidade** (Dieter Rams): "Menos, porém melhor"
- **Clareza** (Edward Tufte): "A excelência gráfica é a apresentação bem pensada de dados interessantes"
- **Eficiência** (Jakob Nielsen): "A melhor interface é aquela que nem percebemos que existe"

## 🎨 Design Moderno e Intuitivo

- **Cores Significativas**: Paleta cromática cuidadosamente selecionada para comunicar status e prioridades.

- **Responsividade**: Adaptação perfeita a qualquer dispositivo ou tela

## Funcionalidades

- **Dashboard Interativo**: Visualização em tempo real de métricas e KPIs
- **Análise Detalhada**: Filtros avançados e análise granular de dados
- **Design Responsivo**: Interface adaptável para desktop e dispositivos móveis
- **Gráficos Dinâmicos**: Visualização de dados com Recharts
- **UI/UX Moderna**: Interface elegante usando Tailwind CSS e Radix UI

## 🚀 Demo

![Demo Screenshot](./screenshots/demo.png)

Acesse nossa [Demo Online](https://manfullwel.github.io/ddemandreport/demo.html) para ver o projeto em ação.

## Tecnologias

- **Frontend:**
  - React 18
  - TypeScript
  - Vite
  - TailwindCSS
  - Radix UI
  - Recharts
  - React Router DOM
  - Lucide React (ícones)

- **Desenvolvimento:**
  - ESLint
  - Prettier
  - Husky
  - TypeScript ESLint

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/manfullwel/ddemandreport.git
cd ddemandreport
```

2. Instale as dependências:
```bash
npm install
```

3. Inicie o servidor de desenvolvimento:
```bash
npm run dev
```

## Scripts Disponíveis

- `npm run dev`: Inicia o servidor de desenvolvimento
- `npm run build`: Gera a build de produção
- `npm run lint`: Executa a verificação de linting
- `npm run format`: Formata o código usando Prettier
- `npm run type-check`: Verifica os tipos TypeScript
- `npm run validate`: Executa todas as verificações (type-check, lint, format)

## Estrutura do Projeto

```
demand-count-sentinel/
├── src/
│   ├── components/     # Componentes React reutilizáveis
│   ├── pages/         # Páginas da aplicação
│   ├── types/         # Definições de tipos TypeScript
│   ├── utils/         # Utilitários e helpers
│   ├── lib/           # Bibliotecas e configurações
│   └── main.tsx       # Ponto de entrada da aplicação
├── public/            # Arquivos estáticos
└── ...                # Arquivos de configuração
```

## Roadmap

- [ ] Implementação de autenticação
- [ ] Integração com backend
- [ ] Exportação de relatórios em PDF
- [ ] Modo dark/light
- [ ] Mais opções de visualização de dados
- [ ] Notificações em tempo real

## Contribuindo

1. Fork o projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Autores

- **Manfullwel** - *Desenvolvedor Principal* - [@manfullwel](https://github.com/manfullwel)

## Agradecimentos

- Equipe de design pela inspiração
- Contribuidores e testadores
- Comunidade open source

---
Desenvolvido com por [Manfullwel](https://github.com/manfullwel)